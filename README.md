# DevMate

通过自然语言描述，DevMate 自动生成可运行的完整 Web 应用（前端 + 后端 + 数据库）。

只需输入你的想法，剩下的交给 DevMate。

---

## 使用场景

传统开发需要经历需求分析、技术选型、搭建项目、编码、联调测试到部署上线，整个过程大约需要 21 小时。

使用 DevMate，输入需求后约 6 分钟就能得到可运行的应用。

---

## 快速开始

### 安装

```bash
pip install -e .
```

### 使用

```bash
# 创建一个待办事项应用
devmate create "A todo app with user login and data persistence"

# 创建一个博客系统
devmate create "A blog with markdown editor, user auth, and comment system"

# 创建一个聊天应用
devmate create "Real-time chat application with file sharing"

# 指定输出目录
devmate create "E-commerce dashboard" -o ./my-shop
```

### 运行生成的项目

```bash
# 进入项目目录
cd todo-app

# 启动前端 (终端 1)
cd frontend
npm install
npm run dev

# 启动后端 (终端 2)
cd ../backend
pip install -r requirements.txt
uvicorn main:app --reload
```

访问 http://localhost:3000 查看你的应用！

---

## 功能

DevMate 能自动识别以下功能需求：

- 认证系统：login, auth, user, register
- CRUD 操作：todo, task, list, manage
- 内容管理：blog, post, article, markdown
- 实时通讯：chat, message, realtime
- 文件处理：upload, file, image

技术栈：
- 前端：React 18 + Vite 5 + Tailwind CSS 3
- 后端：FastAPI + SQLAlchemy 2 + SQLite
- API 文档：Swagger UI 自动生成

---

## 示例

创建一个待办事项应用：

```bash
devmate create "A todo app with user login and data persistence"
```

生成的项目包含完整的 CRUD 操作、任务状态切换、数据持久化和响应式 UI。

其他示例：

```bash
# 博客系统
devmate create "Blog platform with markdown editor and comments"

# 项目管理工具
devmate create "Project management tool with team collaboration"

# 个人记账本
devmate create "Personal finance tracker with charts"
```

---

## CLI 命令

```bash
# 创建新项目
devmate create "<描述>"

# 查看版本
devmate version

# 查看可用模板
devmate list-templates
```

---

## 开发计划

v0.1.0 (当前版本)
- 基础项目生成
- React + FastAPI 模板
- 特征检测（MVP 版）
- Tailwind CSS 集成

v0.2.0
- LLM 驱动的需求分析（Ollama/OpenAI）
- 多模板支持（Next.js, SvelteKit, Vue）
- 插件系统（Supabase, Firebase 等）
- 一键部署脚本（Vercel, Render）

v0.3.0
- 多 Agent 协作架构
- 增量代码生成（迭代优化现有项目）
- 智能调试与修复
- 数据库迁移工具

---

## 贡献

欢迎贡献代码！

### 添加新模板

1. Fork 本项目
2. 在 `templates/` 目录下创建新模板
3. 提交 PR 并说明用途

### 改进特征检测

当前的特征检测基于关键词匹配，可以改进为：
- LLM 语义理解
- 更精准的功能识别
- 自动化测试用例

---

## 安全警告

**⚠️ 重要提示：使用 DevMate 生成的代码部署生产环境前，你必须完成以下安全配置。因未按本指南配置而导致的安全问题或损失，本项目作者不承担任何责任。**

### 1. 修改密钥

生成的项目包含默认的 `SECRET_KEY`，生产环境必须修改：

```bash
# 在 backend/.env 文件中修改
SECRET_KEY=你的强随机密钥

# 生成随机密钥
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. 关闭调试模式

生产环境必须设置 `DEBUG=False`：

```bash
# backend/.env
DEBUG=False
```

### 3. 配置 CORS

明确指定允许的源，避免使用通配符：

```bash
# backend/.env
CORS_ORIGINS=https://yourdomain.com
```

### 4. 数据库安全

- 不要使用默认的 SQLite 数据库文件路径
- 生产环境应使用 PostgreSQL 等数据库
- 数据库密码应通过环境变量传递，不要硬编码

### 5. 环境变量管理

- 不要将 `.env` 文件提交到 Git
- 使用密钥管理服务存储敏感信息
- 定期更新依赖包版本

### 6. 代码审查

DevMate 生成的是基础代码框架，上线前应该：

- 审查生成的代码
- 添加适当的输入验证
- 实现完整的错误处理
- 进行安全测试

### 7. 免责声明

**使用本工具即表示你同意：**

- DevMate 生成的代码仅供学习和快速原型开发使用
- 生产环境部署前必须进行完整的安全审查和测试
- 作者不对使用本工具生成的代码承担任何安全责任
- 因使用或无法使用本工具造成的任何直接或间接损失，作者概不负责
- 用户应自行评估生成代码的风险并承担全部责任

**如果你不打算或不具备能力进行必要的安全加固，请勿将生成的代码用于生产环境。**

---

## 常见问题



**Q: 生成的代码可以商用吗？**

可以，但建议仅用于学习和教育用途。DevMate 生成的代码采用 Apache License 2.0，你可以自由使用、修改和分发。

**注意**：生成的代码是基础框架，生产环境使用前请务必进行完整的安全审查、测试和加固。

可以。DevMate 输出的是标准代码，不是黑盒，你可以自由修改和扩展。

**Q: 支持其他数据库吗？**

当前默认 SQLite，可以轻松升级到 PostgreSQL/MySQL。修改 `main.py` 中的 `DATABASE_URL` 即可。

**Q: 如何添加用户认证？**

v0.2.0 将支持 `--auth` 参数自动生成认证模块。当前需手动添加 JWT 认证逻辑。

---

## 社区与反馈

- 报告问题：[GitHub Issues](https://github.com/steabc123/devmate/issues)
- 功能建议：[Discussions](https://github.com/steabc123/devmate/discussions)

## 许可证

Apache License 2.0 © 2026 xiaomao
