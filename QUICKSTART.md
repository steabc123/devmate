# DevMate 快速开始指南

## 安装步骤

### 方法 1：开发模式安装（推荐）

```bash
# 进入项目目录
cd G:\devmate

# 安装依赖
pip install -r requirements.txt

# 开发模式安装
pip install -e .

# 验证安装
devmate --help
```

### 方法 2：直接运行

```bash
# 进入项目目录
cd G:\devmate

# 直接使用 Python 运行
python cli.py create "A todo app with user login"
```

---

## 使用示例

### 基础用法

```bash
# 创建待办应用
devmate create "A todo app with user login and data persistence"

# 创建博客平台
devmate create "Blog platform with markdown editor and comments"

# 创建聊天应用
devmate create "Real-time chat application with file sharing"

# 创建电商后台
devmate create "E-commerce dashboard with analytics"
```

### 指定输出目录

```bash
# 输出到当前目录
devmate create "My App" -o ./my-app

# 输出到其他位置
devmate create "My App" -o C:\Projects\my-app
```

---

## 运行生成的项目

假设我们创建了 `todo-app`：

### Windows PowerShell

```powershell
# 终端 1 - 启动前端
cd todo-app\frontend
npm install
npm run dev

# 终端 2 - 启动后端
cd ..\backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### macOS/Linux

```bash
# 终端 1 - 启动前端
cd todo-app/frontend
npm install
npm run dev

# 终端 2 - 启动后端
cd ../backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 访问应用

- **前端界面**: http://localhost:3000
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs (Swagger UI)

---

## CLI 命令帮助

### 查看所有命令

```bash
devmate --help
```

输出：
```
DevMate: Generate full-stack web applications from natural language descriptions.

Usage: devmate [OPTIONS] COMMAND [ARGS]...

Commands:
  create          Generate a full-stack web application
  version         Show version information
  list-templates  List available project templates
```

### 查看 create 命令帮助

```bash
devmate create --help
```

输出：
```
Usage: devmate create [OPTIONS] PROMPT

  Generate a full-stack web application from a natural language description.

  Examples:

      devmate create "A blog with markdown editor and user authentication"

      devmate create "Task management app with drag-and-drop interface" -o ./my-app

Arguments:
  PROMPT  Describe your app in one sentence (e.g., 'A todo app with user login and data persistence')

Options:
  -o, --output TEXT  Output directory
  --help             Show this message and exit.
```

---

## 功能检测演示

DevMate 会自动识别以下功能需求：

### 1. 认证系统

```bash
devmate create "App with user login and registration"
# 检测到：authentication
```

### 2. CRUD 操作

```bash
devmate create "Task management app"
# 检测到：crud
```

### 3. 内容管理

```bash
devmate create "Blog with articles and comments"
# 检测到：content
```

### 4. 实时通讯

```bash
devmate create "Chat app with real-time messaging"
# 检测到：realtime
```

### 5. 文件处理

```bash
devmate create "File upload service"
# 检测到：file_upload
```

---

## 项目结构说明

生成的项目结构如下：

```
todo-app/
├── frontend/                 # React 前端
│   ├── node_modules/        # 依赖包（npm install 后生成）
│   ├── public/              # 静态资源
│   ├── src/
│   │   ├── App.jsx          # 主组件（精美 UI）
│   │   ├── main.jsx         # 入口文件
│   │   └── index.css        # Tailwind 样式
│   ├── index.html           # HTML 模板
│   ├── package.json         # 依赖配置
│   ├── vite.config.js       # Vite 配置（含 API 代理）
│   ├── tailwind.config.js   # Tailwind 配置
│   └── postcss.config.js    # PostCSS 配置
│
├── backend/                  # FastAPI 后端
│   ├── __pycache__/         # Python 缓存
│   ├── app.db               # SQLite 数据库（运行时生成）
│   ├── main.py              # API 服务
│   └── requirements.txt     # Python 依赖
│
├── .gitignore               # Git 忽略配置
└── README.md                # 项目说明文档
```

---

## 自定义生成的代码

### 修改前端样式

编辑 `frontend/src/App.jsx`：

```jsx
// 修改主题色
<div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-100">
  // ...
</div>
```

### 添加新的 API 端点

编辑 `backend/main.py`：

```python
@app.get("/api/custom")
def custom_endpoint():
    return {"message": "Custom API"}
```

### 修改数据库模型

编辑 `backend/main.py`：

```python
class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    priority = Column(Integer)  # 新增字段
```

---

## 常见问题

### Q1: npm install 失败？

**解决方案**：
```bash
# 清理缓存
npm cache clean --force

# 使用淘宝镜像
npm config set registry https://registry.npmmirror.com

# 重新安装
npm install
```

### Q2: 前端无法连接后端 API？

**检查**：
1. 后端是否启动在 8000 端口
2. `vite.config.js` 中的代理配置是否正确
3. 浏览器控制台是否有 CORS 错误

**解决方案**：
```python
# backend/main.py 添加 CORS
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Q3: 数据库文件在哪里？

SQLite 数据库文件在 `backend/app.db`，可以使用 DB Browser for SQLite 查看。

### Q4: 如何升级到 PostgreSQL？

修改 `backend/main.py`：

```python
# 替换 DATABASE_URL
DATABASE_URL = "postgresql://user:password@localhost:5432/mydb"

# 安装驱动
pip install psycopg2-binary
```

---

## 下一步

1. **尝试不同 Prompt**
   ```bash
   devmate create "Portfolio website with project gallery"
   devmate create "Recipe manager with shopping list"
   ```

2. **学习源码**
   - 阅读 `agent.py` 了解生成逻辑
   - 研究 `examples/todo-app` 完整示例

3. **参与贡献**
   - Fork 项目
   - 添加新模板
   - 改进特征检测

4. **分享反馈**
   - GitHub Issues 提建议
   - 社交媒体分享作品

---

## 技术支持

- 📖 完整文档：README.md
- 💬 讨论区：GitHub Discussions
- 🐛 问题反馈：GitHub Issues

祝你使用愉快！
