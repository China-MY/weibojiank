# 微博更新监控系统说明文档

## 1. 项目规划
### 1.1 目标定义
开发一个完整的微博更新监控系统，能够自动爬取指定微博账号的更新状态，并通过Web界面进行展示和管理。系统需具备定时监控、过期提醒、账号管理、数据可视化等功能。

### 1.2 资源分配
- **后端开发**: Python (FastAPI, SQLAlchemy, APScheduler/Celery, Requests/Scrapy)
- **前端开发**: React (Vite, Axios, Ant Design/Material UI)
- **数据库**: SQLite (初期)/MySQL (生产) — 已支持通过环境变量切换到 MySQL（异步驱动 aiomysql）
- **开发环境**: Windows 11

### 1.3 时间节点
- **阶段一**: 项目初始化与文档编写 (当前)
- **阶段二**: 后端核心功能开发 (API, 数据库模型, 爬虫逻辑)
- **阶段三**: 前端界面开发 (监控列表, 管理表单, 可视化)
- **阶段四**: 系统集成与测试 (联调, 自动化测试)
- **阶段五**: 文档完善与交付

### 1.4 风险预判
- **反爬虫机制**: 微博可能有严格的反爬措施。对策：使用代理IP池，设置合理的请求间隔（>30s），模拟User-Agent。
- **登录验证**: 部分内容可能需要登录可见。对策：支持Cookie管理或模拟登录（视情况而定，优先公开可见内容）。

## 2. 实施方案
### 2.1 技术选型
- **后端框架**: FastAPI (高性能，易于构建RESTful API)
- **ORM**: SQLAlchemy (成熟稳定)
- **爬虫**: Requests (轻量级) + APScheduler (定时任务)
- **前端框架**: React + Vite
- **UI组件库**: Ant Design (适合管理后台)
- **认证**: JWT (JSON Web Tokens)

### 2.2 架构设计
- **前后端分离**: Backend提供REST API，Frontend通过Axios调用。
- **数据模型**:
    - `User`: 管理员账户 (id, username, password_hash)
    - `WeiboAccount`: 监控账号 (id, uid, screen_name, last_update_time, status, check_interval, is_active)
    - `CrawlLog`: 爬取日志 (id, account_id, timestamp, status, message)

### 2.3 接口协议
- `GET /api/v1/weibo/list`: 获取监控列表
- `GET /api/v1/weibo/expired`: 获取过期账号
- `POST /api/v1/weibo/add`: 添加账号
- `DELETE /api/v1/weibo/remove/{id}`: 删除账号
- `POST /api/v1/auth/login`: 用户登录

## 3. 进度记录
### 3.1 每日任务完成情况
- [x] 项目初始化
- [x] 后端基础架构搭建 (FastAPI + SQLAlchemy)
- [x] 爬虫核心逻辑实现 (Requests + APScheduler)
- [x] 前端基础架构搭建 (React + Vite + Ant Design)
- [x] 前后端联调 (API Authentication verified)
- [x] UI 响应式优化 (PC端适配: 登录页, 仪表盘表格/统计卡片)
- [x] 全局布局修复 (修复 Flex 布局导致的内容截断问题，标准化字体与 Meta 标签)
- [x] 爬虫逻辑增强 (动态获取 container ID, 错误处理)
- [x] 增加异常账号刷新时的后端日志打印功能 (方便排查爬虫失败原因)
- [x] 修复超期天数计算逻辑 (精确到日期，避免因时间差导致少算一天)
- [x] 修复前端超期提醒显示“0天”的Bug (统一使用日期差计算)
- [ ] 测试与部署 (Pending proxy configuration for crawler)

### 3.2 问题追踪
- **Vite/Node Compatibility**: Node v18 environment requires Vite 5.x and React Router 6.x. Downgraded versions to ensure compatibility.
- **Pydantic V2**: Updated schemas to use `from_attributes` instead of `orm_mode`.
- **Weibo API 432 Error**: Crawler encounters 432 Client Error due to IP/User-Agent blocking.
  - **解决方案**: 需要配置有效的代理IP池 (PROXIES list in `backend/app/crawler/weibo_spider.py`).
  - **临时措施**: 增强了错误处理逻辑，防止系统崩溃。

### 3.3 变更说明
- **Frontend Port**: Running on 5173/5174.
- **Backend Port**: Running on 8000.
- **Default Admin**: username `boyueadmin`, password `boyue2025@123`.
- **UI Changes**: Dashboard Table now supports horizontal scrolling (`scroll={{ x: 'max-content' }}`) and responsive columns. Login card adapts to screen width.
 - **存储模式**: 新增 MySQL 支持，配置方式：在项目根目录创建 `.env`（不提交）并设置：
   - `DB_DRIVER=mysql`
   - `DB_HOST=ip`（请替换为您的 MySQL 服务器 IP）
   - `DB_PORT=port`（请替换为您的 MySQL 服务器端口，默认 3306）
   - `DB_NAME=weibopyjiank`（请替换为您的数据库名称）
   - `DB_USER=username`（请替换为您的 MySQL 用户名）
   - `DB_PASSWORD=******`（请使用您提供的密码，勿提交）
   - 安装依赖：`pip install -r backend/requirements.txt`
   - 启动后端自动建表：`uvicorn app.main:app --reload`
- **日志增强**: 在手动刷新 (`/check/{uid}`) 和定时任务 (`scheduler.py`) 中增加了对爬取失败的错误日志输出 (Log Level: ERROR)，包含账号名称、UID 和具体错误信息。
- **逻辑修复**: 修正了超期未更新天数的计算方式，统一采用 `(当前日期 - 最后更新日期).days`，忽略具体时间差异，解决“推送天数比实际少一天”的问题。
- **前端修复**: 同步修改了前端 `Dashboard.jsx` 中的状态判定与提示文案逻辑，使用 `dayjs().startOf('day')` 进行比较，解决了页面上出现“已超过0天”的显示异常。
