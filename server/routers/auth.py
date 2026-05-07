import base64
import hashlib
import hmac
import re
import secrets
from datetime import datetime, timedelta, timezone

import asyncpg
from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel

from db import get_db_pool


router = APIRouter()

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PBKDF2_ITERATIONS = 210_000
SESSION_DAYS = 7


class RegisterPayload(BaseModel):
    email: str
    password: str
    display_name: str | None = None


class LoginPayload(BaseModel):
    email: str
    password: str


def normalize_email(email: str) -> str:
    return email.strip().lower()


def clean_display_name(display_name: str | None) -> str | None:
    if display_name is None:
        return None
    cleaned = display_name.strip()
    return cleaned or None


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )
    return "pbkdf2_sha256${}${}${}".format(
        PBKDF2_ITERATIONS,
        base64.b64encode(salt).decode("ascii"),
        base64.b64encode(digest).decode("ascii"),
    )


def verify_password(password: str, password_hash: str) -> bool:
    try:
        scheme, iterations, salt_b64, digest_b64 = password_hash.split("$", 3)
        if scheme != "pbkdf2_sha256":
            return False
        salt = base64.b64decode(salt_b64.encode("ascii"))
        expected = base64.b64decode(digest_b64.encode("ascii"))
        actual = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            int(iterations),
        )
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def public_user(row) -> dict:
    return {
        "id": str(row["id"]),
        "email": row["email"],
        "display_name": row["display_name"],
        "created_at": row["created_at"].isoformat(),
        "last_login_at": row["last_login_at"].isoformat() if row["last_login_at"] else None,
    }


def validate_credentials(email: str, password: str):
    normalized = normalize_email(email)
    if not EMAIL_RE.match(normalized):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "邮箱格式不正确")
    if len(password) < 8:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "密码至少需要 8 位")
    return normalized


async def create_session(pool, user_id, request: Request):
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(days=SESSION_DAYS)
    user_agent = request.headers.get("user-agent")
    forwarded_for = request.headers.get("x-forwarded-for")
    ip_address = forwarded_for.split(",", 1)[0].strip() if forwarded_for else None
    if not ip_address and request.client:
        ip_address = request.client.host

    await pool.execute(
        """
        insert into public.app_auth_sessions
          (user_id, token_hash, user_agent, ip_address, expires_at)
        values ($1, $2, $3, $4, $5)
        """,
        user_id,
        hash_token(token),
        user_agent,
        ip_address,
        expires_at,
    )
    return token, expires_at


async def require_user(request: Request):
    auth_header = request.headers.get("authorization", "")
    scheme, _, token = auth_header.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "请先登录")

    pool = get_db_pool(request)
    if pool is None:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "数据库连接未配置")

    row = await pool.fetchrow(
        """
        select u.id, u.email, u.display_name, u.created_at, u.last_login_at
        from public.app_auth_sessions s
        join public.app_users u on u.id = s.user_id
        where s.token_hash = $1
          and s.revoked_at is null
          and s.expires_at > now()
        """,
        hash_token(token),
    )
    if row is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "登录已过期")
    return row


@router.post("/register")
async def register(payload: RegisterPayload, request: Request):
    pool = get_db_pool(request)
    if pool is None:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "数据库连接未配置")

    email = validate_credentials(payload.email, payload.password)
    display_name = clean_display_name(payload.display_name)

    try:
        async with pool.acquire() as conn:
            async with conn.transaction():
                user = await conn.fetchrow(
                    """
                    insert into public.app_users (email, display_name, password_hash)
                    values ($1, $2, $3)
                    returning id, email, display_name, created_at, last_login_at
                    """,
                    email,
                    display_name,
                    hash_password(payload.password),
                )
                token, expires_at = await create_session(conn, user["id"], request)
    except asyncpg.UniqueViolationError:
        raise HTTPException(status.HTTP_409_CONFLICT, "这个邮箱已经注册过")

    return {
        "user": public_user(user),
        "token": token,
        "expires_at": expires_at.isoformat(),
    }


@router.post("/login")
async def login(payload: LoginPayload, request: Request):
    pool = get_db_pool(request)
    if pool is None:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "数据库连接未配置")

    email = validate_credentials(payload.email, payload.password)
    async with pool.acquire() as conn:
        user = await conn.fetchrow(
            """
            select id, email, display_name, password_hash, created_at, last_login_at
            from public.app_users
            where email = $1
            """,
            email,
        )
        if user is None or not verify_password(payload.password, user["password_hash"]):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "邮箱或密码不正确")

        async with conn.transaction():
            token, expires_at = await create_session(conn, user["id"], request)
            user = await conn.fetchrow(
                """
                update public.app_users
                set last_login_at = now()
                where id = $1
                returning id, email, display_name, created_at, last_login_at
                """,
                user["id"],
            )

    return {
        "user": public_user(user),
        "token": token,
        "expires_at": expires_at.isoformat(),
    }


@router.get("/me")
async def me(request: Request):
    user = await require_user(request)
    return {"user": public_user(user)}


@router.post("/logout")
async def logout(request: Request):
    pool = get_db_pool(request)
    if pool is None:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "数据库连接未配置")

    auth_header = request.headers.get("authorization", "")
    _, _, token = auth_header.partition(" ")
    if token:
        await pool.execute(
            """
            update public.app_auth_sessions
            set revoked_at = now()
            where token_hash = $1 and revoked_at is null
            """,
            hash_token(token),
        )
    return {"ok": True}
