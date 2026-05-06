# AGENTS.md

## 项目概览

这是一个媒体处理类全栈项目，当前定位是 **Vlade 媒体工作台**。项目面向前端/全栈开发岗展示，重点不是单纯复刻 Clideo，而是展示：

- Vue 3 组件化工作台 UI
- 视频、图片、音频三类媒体处理流程
- FastAPI 文件上传、处理、下载接口
- FFmpeg / Pillow 媒体处理能力
- 上传后的媒体体检卡、结果摘要和参数化处理

前端在 `src/`，后端在 `server/`。当前没有 Git 仓库信息，工作区里有生成产物和上传/输出文件，改动时不要误删用户文件。

## 技术栈

### 前端

- Vue 3
- Vite
- Vue Router
- `@iconify/vue`：统一图标库
- `gsap`：已安装，可用于高级动画
- CSS 方案：Vue SFC 内的 scoped CSS + `App.vue` 全局 CSS 变量

### 后端

- FastAPI
- Uvicorn
- `ffmpeg-python`
- Pillow
- `python-multipart`
- `aiofiles`

### 媒体能力

- 视频/音频处理依赖 FFmpeg
- 图片处理依赖 Pillow
- 上传文件保存在 `server/uploads/`
- 输出文件保存在 `server/outputs/`

## 常用命令

### 前端

```bash
npm.cmd run dev
npm.cmd run build
npm.cmd run preview
```

注意：在当前受限环境里，`npm.cmd run build` 可能因为 `esbuild spawn EPERM` 失败。这通常是沙盒/权限问题，不一定代表代码语法错误。可以先用 Vue SFC 静态检查确认模板和脚本。

### 后端

```bash
cd server
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Vite 已在 `vite.config.js` 中把 `/api` 代理到 `http://localhost:8000`。

## 目录结构

```text
.
├─ src/
│  ├─ App.vue
│  ├─ main.js
│  ├─ api/
│  │  └─ index.js
│  ├─ components/
│  │  ├─ AppFooter.vue
│  │  ├─ MediaVisual.vue
│  │  ├─ NavBar.vue
│  │  ├─ ProcessingWorkspace.vue
│  │  ├─ UploadZone.vue
│  │  └─ VideoTrimmer.vue
│  ├─ data/
│  │  └─ toolSuites.js
│  ├─ router/
│  │  └─ index.js
│  └─ views/
│     ├─ Home.vue
│     ├─ VideoView.vue
│     ├─ ImageView.vue
│     └─ AudioView.vue
├─ server/
│  ├─ main.py
│  ├─ utils.py
│  ├─ requirements.txt
│  ├─ routers/
│  │  ├─ analyze.py
│  │  ├─ video.py
│  │  ├─ image.py
│  │  └─ audio.py
│  └─ services/
│     ├─ ffmpeg.py
│     └─ image.py
└─ vite.config.js
```

## 前端架构

### 路由

路由在 `src/router/index.js`：

- `/`：首页
- `/video`：视频处理
- `/image`：图片处理
- `/audio`：音频处理

### 页面关系

`VideoView.vue`、`ImageView.vue`、`AudioView.vue` 都是轻量容器页，主要把对应的 suite 配置传给 `ProcessingWorkspace.vue`。

核心工作台逻辑集中在：

- `src/components/ProcessingWorkspace.vue`

上传区逻辑集中在：

- `src/components/UploadZone.vue`

三类工具配置集中在：

- `src/data/toolSuites.js`

视觉示意图层集中在：

- `src/components/MediaVisual.vue`

### 工具配置方式

`toolSuites.js` 定义视频、图片、音频三类 suite。每个 suite 包含：

- `key`
- `path`
- `title`
- `intro`
- `badge`
- `icon`
- `visual`
- `uploadKind`
- `accept`
- `stats`
- `tools`

每个工具通常包含：

- `id`
- `title`
- `action`
- `desc`
- `icon`
- `endpoint`
- `params`
- `controls`
- `tips`
- `multi`

新增工具时优先改 `toolSuites.js`，不要在页面里硬编码工具列表。

### 参数控件

当前 `ProcessingWorkspace.vue` 支持这些控件类型：

- `range`
- `chips`
- `select`
- `text`
- `number`

参数 chip 的交互规则：

- `.param-chip.active` 才是已选状态
- hover 只做边框/文字变化
- 不要让 hover 看起来像 active，避免“鼠标移回 MP4 还像选中了”的错觉

## 后端架构

### FastAPI 入口

入口文件：

- `server/main.py`

已挂载路由：

- `/api/video`
- `/api/image`
- `/api/audio`
- `/api/analyze`
- `/api/download/{filename}`
- `/api/health`

### 文件工具

`server/utils.py`：

- `save_upload(file)`：保存上传文件到 `server/uploads/`
- `output_filename(ext)`：生成输出文件路径和文件名
- `UPLOAD_DIR`
- `OUTPUT_DIR`

### 媒体分析

`server/routers/analyze.py`：

- `POST /api/analyze`
- 入参：`file`
- 返回：`kind`、`filename`、`size`、`size_label`、`format`、`metadata`、`suggestions`

视频/音频使用 FFprobe 读取：

- 时长
- 码率
- 视频编码
- 音频编码
- 分辨率
- 采样率
- 声道数

图片使用 Pillow 读取：

- 格式
- 宽高
- 色彩模式
- 是否透明

分析失败时前端不应阻塞后续处理，只显示“暂时无法读取文件信息”。

### 视频接口

`server/routers/video.py`：

- `POST /api/video/compress`
- `POST /api/video/convert`
- `POST /api/video/trim`
- `POST /api/video/merge`
- `POST /api/video/extract-audio`
- `POST /api/video/subtitle`
- `POST /api/video/to-gif`

实际处理逻辑在 `server/services/ffmpeg.py`。

### 图片接口

`server/routers/image.py`：

- `POST /api/image/compress`
- `POST /api/image/convert`
- `POST /api/image/crop`
- `POST /api/image/resize`
- `POST /api/image/watermark`

实际处理逻辑在 `server/services/image.py`。

### 音频接口

`server/routers/audio.py`：

- `POST /api/audio/compress`
- `POST /api/audio/convert`
- `POST /api/audio/trim`
- `POST /api/audio/merge`
- `POST /api/audio/volume`
- `POST /api/audio/denoise`

实际处理逻辑在 `server/services/ffmpeg.py`。

## 当前产品功能

### 首页

`Home.vue` 是非传统 Hero + 三卡片结构，当前更偏“媒体工作台”视觉：

- 首屏左文案、右媒体预览
- 中段有左侧粘性图片实验台和右侧入口流
- 入口卡片使用 `MediaVisual` 展示视频/图片/音频的语义化视觉
- 使用 Picsum Photos 作为临时占位图

### 工作台

`ProcessingWorkspace.vue` 提供统一交互：

- 左侧工具列表
- 中间上传、体检卡、参数、预览、结果摘要
- 右侧视觉图、提示、日志

上传单文件后会调用 `/api/analyze` 生成体检卡。处理完成后会显示结果摘要和下载按钮。

### 上传区

`UploadZone.vue` 支持：

- 单文件/多文件选择
- 拖拽上传
- 处理中状态
- 完成/失败状态
- 重置

合并视频/音频工具使用 `multi: true`，前端会把字段名改成 `files`。

## 设计约束

用户明确提出过这些偏好，后续改动应尽量遵守：

- 不使用 Tailwind CSS
- 不引入 Tailwind 系组件库
- 图标统一使用 Iconify
- 不使用 Emoji 作为功能图标
- 临时占位图使用 Picsum Photos
- 避免紫色/靛蓝色渐变
- 避免纯平背景，大背景应有噪点、图片暗化层或暖色渐变
- 避免传统“居中 Hero + 三卡片”模板感
- 动画不要使用普通 `ease-in-out`，优先自定义 `cubic-bezier`
- 文案要直接，不要堆高深术语和空话

## 已知注意点

### 1. 编码/乱码问题

项目早期有较多中文乱码。核心文件近期已逐步修复，但如果发现 UI 文案乱码，优先检查：

- `src/data/toolSuites.js`
- `src/components/ProcessingWorkspace.vue`
- `src/components/UploadZone.vue`
- `src/views/Home.vue`

### 2. 构建环境问题

当前桌面沙盒中运行 `npm.cmd run build` 可能失败：

```text
Error: spawn EPERM
```

这通常发生在 Vite 调用 esbuild 子进程时。若遇到该问题，可先做 Vue SFC 静态检查；完整构建建议在正常本机权限下运行。

### 3. 输出/上传目录

`server/uploads/` 和 `server/outputs/` 里有测试和历史处理文件。不要随便递归删除这些目录，除非用户明确要求清理。

### 4. 多文件接口字段

普通处理接口字段名是 `file`。合并接口字段名是 `files`：

- `/api/video/merge`
- `/api/audio/merge`

前端 `src/api/index.js` 已通过 `options.multi` 处理该差异。

## 推荐后续增强方向

在不大转型的前提下，最适合面试展示的增强是：

1. 视频：提取封面、社媒尺寸预设、处理前后体积变化
2. 图片：压缩前后对比滑杆、头像/封面/网页图预设
3. 音频：波形预览、音量峰值分析、降噪前后说明
4. 通用：异步任务队列、任务状态轮询、处理日志、结果包导出

建议优先做“体检卡 + 结果摘要 + 对比体验”，因为最能体现工程完整度。

## 开发原则

- 优先复用 `ProcessingWorkspace.vue`，不要让三个处理页重新分叉。
- 新工具优先写进 `toolSuites.js`，再补后端 endpoint。
- 后端处理函数放在 `server/services/`，路由只负责收参、保存上传、调用服务、返回结果。
- 前端用户可见文案保持中文、简短、直白。
- 保持现有暖色深色视觉风格。
- 不要把临时生成文件或输出目录误当源码重构对象。
