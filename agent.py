# devmate/agent.py
import re
import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def parse_app_spec(prompt: str) -> dict:
    """
    Extract basic info from prompt.
    
    Future enhancement: use LLM for better semantic understanding.
    """
    # Simple heuristic for app name
    words = prompt.strip().split()
    app_name = " ".join(words[:min(4, len(words))]).title()
    if not app_name:
        app_name = "My App"

    # Slugify
    project_slug = re.sub(r"[^a-z0-9]+", "-", prompt.lower())
    project_slug = project_slug.strip("-")[:30]
    if not project_slug:
        project_slug = "my-app"
    
    # Detect features (MVP: keyword-based, future: LLM-based)
    features = []
    prompt_lower = prompt.lower()
    if any(word in prompt_lower for word in ['login', 'auth', 'user', 'register']):
        features.append('authentication')
    if any(word in prompt_lower for word in ['todo', 'task', 'list']):
        features.append('crud')
    if any(word in prompt_lower for word in ['blog', 'post', 'article', 'markdown']):
        features.append('content')
    if any(word in prompt_lower for word in ['chat', 'message', 'realtime']):
        features.append('realtime')
    if any(word in prompt_lower for word in ['upload', 'file', 'image']):
        features.append('file_upload')

    return {
        "app_name": app_name,
        "project_slug": project_slug,
        "prompt": prompt,
        "features": features,
        "tech_stack": {
            "frontend": "react",
            "backend": "fastapi",
            "database": "sqlite"
        }
    }


def generate_project(prompt: str, output_dir: Path):
    """Generate a full-stack web application from a natural language prompt."""
    spec = parse_app_spec(prompt)
    proj_path = output_dir / spec["project_slug"]
    
    print(f"Generating project: {spec['app_name']}")
    print(f"Location: {proj_path}")
    print(f"Detected features: {', '.join(spec['features']) if spec['features'] else 'basic CRUD'}")

    # Create directories
    (proj_path / "frontend" / "src").mkdir(parents=True, exist_ok=True)
    (proj_path / "backend").mkdir(parents=True, exist_ok=True)

    # Jinja2 env
    template_dir = Path(__file__).parent / "templates"
    env = Environment(loader=FileSystemLoader(template_dir))

    # --- Frontend ---
    # index.html
    (proj_path / "frontend" / "index.html").write_text(
        env.get_template("frontend/index.html").render(spec)
    )

    # main.jsx
    (proj_path / "frontend" / "src" / "main.jsx").write_text(
        env.get_template("frontend/src/main.jsx").render(spec)
    )

    # App.jsx
    (proj_path / "frontend" / "src" / "App.jsx").write_text(
        env.get_template("frontend/src/App.jsx").render(spec)
    )

    # package.json
    pkg_json = {
        "name": spec["project_slug"],
        "private": True,
        "version": "0.1.0",
        "type": "module",
        "scripts": {
            "dev": "vite",
            "build": "vite build",
            "preview": "vite preview"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0"
        },
        "devDependencies": {
            "@vitejs/plugin-react": "^4.2.0",
            "vite": "^5.0.0",
            "tailwindcss": "^3.4.0",
            "autoprefixer": "^10.4.0",
            "postcss": "^8.4.0"
        }
    }
    (proj_path / "frontend" / "package.json").write_text(json.dumps(pkg_json, indent=2))

    # vite.config.js
    vite_config = '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: { 
    port: 3000,
    proxy: {
      '/api': {
        target: import.meta.env.VITE_API_URL || 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})'''
    (proj_path / "frontend" / "vite.config.js").write_text(vite_config)
    
    # .env.example for frontend
    frontend_env = f'''# Frontend Environment Variables
VITE_API_URL=http://localhost:8000
VITE_APP_NAME={spec["app_name"]}
VITE_DEBUG=true
'''
    (proj_path / "frontend" / ".env.example").write_text(frontend_env)
    
    # Create empty .env file for frontend
    (proj_path / "frontend" / ".env").write_text(f"# Frontend Environment Variables\nVITE_API_URL=http://localhost:8000\nVITE_APP_NAME={spec['app_name']}\n")
    
    # postcss.config.js
    postcss_config = '''export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}'''
    (proj_path / "frontend" / "postcss.config.js").write_text(postcss_config)

    # --- Backend ---
    (proj_path / "backend" / "main.py").write_text(
        env.get_template("backend/main.py").render(spec)
    )

    # requirements.txt
    reqs = "fastapi>=0.115.0\nuvicorn[standard]>=0.32.0\nsqlalchemy>=2.0.0\npython-dotenv>=1.0.0\npydantic>=2.0.0\npydantic-settings>=2.0.0"
    (proj_path / "backend" / "requirements.txt").write_text(reqs)

    # .env.example for backend
    env_example = '''# Application Settings
APP_NAME=''' + spec["app_name"] + '''
APP_VERSION=0.1.0
DEBUG=True

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Database Configuration
DATABASE_URL=sqlite:///./data/app.db
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10

# CORS Settings
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CORS_ALLOW_CREDENTIALS=True
CORS_ALLOW_METHODS=GET,POST,PUT,DELETE
CORS_ALLOW_HEADERS=*

# Security
SECRET_KEY=''' + spec["project_slug"] + '''-secret-key-change-in-production
API_PREFIX=/api

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
'''
    (proj_path / "backend" / ".env.example").write_text(env_example)
    
    # Create empty .env file for user to fill in
    (proj_path / "backend" / ".env").write_text("# Copy settings from .env.example and customize as needed\n")

    # .gitignore
    gitignore = env.get_template(".gitignore").render()
    (proj_path / ".gitignore").write_text(gitignore)

    # README.md for generated project
    readme = f'''# {spec["app_name"]}

Generated by [DevMate](https://github.com/yourname/devmate) 🚀

## Description

{spec["prompt"]}

## Features

{chr(10).join(['- ' + feature for feature in spec['features']]) if spec['features'] else '- Basic CRUD operations'}

## Configuration

### Backend Configuration

1. Navigate to the `backend` directory
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` file and customize settings as needed

Key settings:
- `DATABASE_URL`: Database connection string
- `PORT`: Backend server port (default: 8000)
- `CORS_ORIGINS`: Allowed origins for CORS
- `SECRET_KEY`: Change this in production!

### Frontend Configuration

1. Navigate to the `frontend` directory
2. Create or edit `.env` file:
   ```bash
   VITE_API_URL=http://localhost:8000
   VITE_APP_NAME={spec["app_name"]}
   ```

## Quick Start

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:3000

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The backend API will be available at http://localhost:8000

## Project Structure

```
{spec["project_slug"]}/
├── frontend/           # React + Vite + Tailwind CSS
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── .env.example    # Frontend environment variables template
├── backend/            # FastAPI + SQLAlchemy
│   ├── main.py
│   ├── config.py       # Configuration management
│   ├── requirements.txt
│   └── .env.example    # Backend environment variables template
└── README.md
```

## Tech Stack

- **Frontend**: React 18, Vite, Tailwind CSS
- **Backend**: FastAPI, SQLAlchemy
- **Database**: SQLite (can be upgraded to PostgreSQL)
- **Configuration**: Environment variables via python-dotenv

## Environment Variables

### Backend

| Variable | Default | Description |
|----------|---------|-------------|
| APP_NAME | DevMate App | Application name |
| DATABASE_URL | sqlite:///./data/app.db | Database connection |
| PORT | 8000 | Server port |
| CORS_ORIGINS | http://localhost:3000 | Allowed CORS origins |
| SECRET_KEY | change-me | Secret key for security |
| LOG_LEVEL | INFO | Logging level |

### Frontend

| Variable | Default | Description |
|----------|---------|-------------|
| VITE_API_URL | http://localhost:8000 | Backend API URL |
| VITE_APP_NAME | DevMate App | Application name |

## Next Steps

1. Customize the generated code to fit your needs
2. Add authentication if needed
3. Update environment variables for production
4. Deploy to production (Vercel for frontend, Render for backend)

## Security Notes

⚠️ **Important for Production**:
- Change `SECRET_KEY` in `.env` file
- Set `DEBUG=False`
- Configure proper CORS origins
- Use environment variables for sensitive data
- Don't commit `.env` files to version control

## License

MIT
'''
    (proj_path / "README.md").write_text(readme)
    
    print(f"\nProject generated successfully!")
    print(f"\nNext steps:")
    print(f"   cd {proj_path.name}")
    print(f"   cd frontend && npm install && npm run dev")
    print(f"   cd ../backend && pip install -r requirements.txt && uvicorn main:app --reload")
    print(f"\nOpen http://localhost:3000 to see your app!\n")