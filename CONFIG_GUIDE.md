# DevMate 配置管理指南

## 概述

DevMate 使用环境变量实现灵活的配置，支持多环境部署。

## 配置层次

配置的优先级从高到低：
1. 系统环境变量
2. `.env` 文件中的配置
3. 代码中的默认值

## 后端配置

### 文件结构

```
backend/
├── config.py          # 配置管理类
├── .env.example       # 配置模板
├── .env              # 实际配置（不提交到 Git）
└── main.py           # 使用配置的应用
```

### 配置项说明

#### 应用配置
- `APP_NAME`: 应用名称
- `APP_VERSION`: 应用版本
- `DEBUG`: 调试模式开关

#### 服务器配置
- `HOST`: 服务器监听地址
- `PORT`: 服务器端口号

#### 数据库配置
- `DATABASE_URL`: 数据库连接字符串
- `DATABASE_POOL_SIZE`: 数据库连接池大小
- `DATABASE_MAX_OVERFLOW`: 最大溢出连接数

#### CORS 配置
- `CORS_ORIGINS`: 允许的源（逗号分隔）
- `CORS_ALLOW_CREDENTIALS`: 是否允许凭证
- `CORS_ALLOW_METHODS`: 允许的 HTTP 方法
- `CORS_ALLOW_HEADERS`: 允许的请求头

#### 安全配置
- `SECRET_KEY`: 加密密钥（生产环境必须修改）
- `API_PREFIX`: API 路由前缀

#### 日志配置
- `LOG_LEVEL`: 日志级别（DEBUG/INFO/WARNING/ERROR/CRITICAL）
- `LOG_FORMAT`: 日志格式（json/text）

### 使用方法

1. 复制配置模板：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，根据需要修改配置：
```bash
# 生产环境示例
APP_NAME=My Production App
DEBUG=False
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
PORT=8000
CORS_ORIGINS=https://myapp.com
SECRET_KEY=super-secret-key-change-this
```

3. 在代码中使用配置：
```python
from config import get_settings

settings = get_settings()

# 访问配置项
print(settings.app_name)
print(settings.database_url)
print(settings.cors_origins_list)
```

## 前端配置

### 文件结构

```
frontend/
├── .env.example       # 配置模板
├── .env              # 实际配置（不提交到 Git）
└── vite.config.js    # Vite 配置
```

### 配置项说明

#### Vite 环境变量
- `VITE_API_URL`: 后端 API 地址
- `VITE_APP_NAME`: 应用名称
- `VITE_DEBUG`: 调试模式开关

### 使用方法

1. 创建 `.env` 文件：
```bash
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=My App
VITE_DEBUG=true
```

2. 在代码中使用：
```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const APP_NAME = import.meta.env.VITE_APP_NAME || 'My App'
```

## 环境特定配置

### 开发环境 (.env.development)

```bash
DEBUG=True
DATABASE_URL=sqlite:///./dev.db
LOG_LEVEL=DEBUG
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

### 生产环境 (.env.production)

```bash
DEBUG=False
DATABASE_URL=postgresql://user:pass@prod-host:5432/proddb
LOG_LEVEL=ERROR
CORS_ORIGINS=https://myapp.com
SECRET_KEY=production-secret-key
```

### 测试环境 (.env.test)

```bash
DEBUG=True
DATABASE_URL=sqlite:///./test.db
LOG_LEVEL=WARNING
```

## 最佳实践

### 推荐做法

1. **使用环境变量管理敏感信息**
   - 数据库密码
   - API 密钥
   - 加密密钥

2. **为不同环境创建不同的配置文件**
   - `.env.development`
   - `.env.production`
   - `.env.test`

3. **在 README 中记录所有配置项**
   - 提供清晰的说明
   - 包含默认值
   - 标注必填项

4. **使用强密钥**
   ```bash
   # 生成随机密钥
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

5. **定期更新依赖版本**
   ```bash
   pip install --upgrade pydantic-settings python-dotenv
   ```

### 避免的做法

1. **不要提交 `.env` 文件到 Git**
   - 已添加到 `.gitignore`
   - 只提交 `.env.example` 模板

2. **不要在代码中硬编码配置**
   ```python
   # 错误
   DATABASE_URL = "sqlite:///./app.db"
   
   # 正确
   from config import get_settings
   settings = get_settings()
   DATABASE_URL = settings.database_url
   ```

3. **不要在生产环境使用默认密钥**
   ```python
   # 危险
   SECRET_KEY = "change-me"
   
   # 安全
   SECRET_KEY = os.getenv("SECRET_KEY", generate_secret())
   ```

4. **不要忽略 CORS 配置**
   - 明确指定允许的源
   - 避免在生产环境使用 `*`

## 配置验证

启动应用前，验证配置是否正确：

### 后端验证

```python
# 测试配置加载
cd backend
python -c "from config import get_settings; s = get_settings(); print(f'App: {s.app_name}, DB: {s.database_url}')"
```

### 前端验证

```javascript
// 在浏览器控制台检查
console.log('API URL:', import.meta.env.VITE_API_URL)
console.log('App Name:', import.meta.env.VITE_APP_NAME)
```

## 常见问题

### Q: 配置不生效怎么办？

A: 检查以下几点：
1. `.env` 文件是否在正确的目录
2. 是否重启了应用
3. 环境变量名是否正确（区分大小写）
4. 是否有拼写错误

### Q: 如何在 Docker 中使用配置？

A: 通过 Docker 环境变量传递：
```dockerfile
ENV DATABASE_URL=postgresql://...
ENV SECRET_KEY=docker-secret-key
```

或使用 docker-compose：
```yaml
environment:
  - DATABASE_URL=${DATABASE_URL}
  - SECRET_KEY=${SECRET_KEY}
```

### Q: 如何管理多个环境的配置？

A: 使用不同的 `.env` 文件：
```bash
# 开发环境
cp .env.development .env

# 生产环境
cp .env.production .env
```

或在代码中根据环境变量切换：
```python
class Settings(BaseSettings):
    class Config:
        env_file = f".env.{os.getenv('ENVIRONMENT', 'development')}"
```

## 故障排除

### 问题：找不到 .env 文件

**解决方案：**
```python
import os
from pathlib import Path

# 在 config.py 中添加调试信息
env_path = Path('.') / '.env'
if not env_path.exists():
    print(f"Warning: .env file not found at {env_path}")
```

### 问题：配置项类型错误

**解决方案：**
确保类型注解正确：
```python
port: int = 8000  # ✅ 整数
debug: bool = True  # ✅ 布尔值
database_url: str = "sqlite:///app.db"  # ✅ 字符串
```

### 问题：CORS 不工作

**解决方案：**
1. 检查 `CORS_ORIGINS` 格式（逗号分隔，无空格）
2. 确保中间件已添加
3. 检查前端请求的 Origin 头

## 总结

良好的配置管理可以：
- 提高代码安全性
- 简化部署流程
- 支持多环境部署
- 便于团队协作
- 减少配置错误

遵循本指南的最佳实践，确保你的 DevMate 项目配置管理规范、安全、可维护。
