create extension if not exists pgcrypto;

create table if not exists public.app_users (
  id uuid primary key default gen_random_uuid(),
  email text not null,
  display_name text,
  password_hash text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  last_login_at timestamptz,
  constraint app_users_email_normalized_unique unique (email),
  constraint app_users_email_format check (position('@' in email) > 1),
  constraint app_users_password_hash_not_blank check (length(password_hash) > 20)
);

create table if not exists public.app_auth_sessions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.app_users(id) on delete cascade,
  token_hash text not null unique,
  user_agent text,
  ip_address text,
  created_at timestamptz not null default now(),
  expires_at timestamptz not null,
  revoked_at timestamptz
);

create index if not exists app_auth_sessions_user_id_idx
  on public.app_auth_sessions(user_id);

create index if not exists app_auth_sessions_active_idx
  on public.app_auth_sessions(token_hash, expires_at)
  where revoked_at is null;

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists app_users_set_updated_at on public.app_users;
create trigger app_users_set_updated_at
before update on public.app_users
for each row
execute function public.set_updated_at();

alter table public.app_users enable row level security;
alter table public.app_auth_sessions enable row level security;
