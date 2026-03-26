#!/usr/bin/env python3
"""测试 DevMate 是否能正常运行"""

import sys
from pathlib import Path

def test_imports():
    """测试必要的依赖是否已安装"""
    print("1. 检查 Python 依赖...")
    try:
        import typer
        import jinja2
        from pathlib import Path
        print("   ✓ 必要依赖已安装")
        return True
    except ImportError as e:
        print(f"   ✗ 缺少依赖：{e}")
        print("\n请运行：pip install -r requirements.txt")
        return False

def test_template_files():
    """检查模板文件是否完整"""
    print("\n2. 检查模板文件...")
    
    required_files = [
        "templates/.gitignore",
        "templates/frontend/index.html",
        "templates/frontend/src/main.jsx",
        "templates/frontend/src/App.jsx",
        "templates/frontend/src/index.css",
        "templates/frontend/tailwind.config.js",
        "templates/backend/main.py",
        "templates/backend/config.py",
    ]
    
    missing = []
    for file_path in required_files:
        if not (Path(__file__).parent / file_path).exists():
            missing.append(file_path)
    
    if missing:
        print(f"   ✗ 缺少文件：{', '.join(missing)}")
        return False
    else:
        print("   ✓ 模板文件完整")
        return True

def test_agent_module():
    """测试 agent 模块能否导入"""
    print("\n3. 检查 agent 模块...")
    try:
        from devmate.agent import parse_app_spec, generate_project
        print("   ✓ agent 模块可正常导入")
        
        # 测试 parse_app_spec 函数
        spec = parse_app_spec("A todo app with login")
        if "app_name" in spec and "features" in spec:
            print("   ✓ parse_app_spec 函数正常")
            return True
        else:
            print("   ✗ parse_app_spec 返回值异常")
            return False
    except Exception as e:
        print(f"   ✗ agent 模块导入失败：{e}")
        return False

def test_cli_module():
    """测试 cli 模块能否导入"""
    print("\n4. 检查 cli 模块...")
    try:
        from devmate.cli import app
        print("   ✓ cli 模块可正常导入")
        return True
    except Exception as e:
        print(f"   ✗ cli 模块导入失败：{e}")
        return False

def main():
    print("=" * 60)
    print("DevMate 运行环境检查")
    print("=" * 60)
    
    results = []
    results.append(test_imports())
    results.append(test_template_files())
    results.append(test_agent_module())
    results.append(test_cli_module())
    
    print("\n" + "=" * 60)
    if all(results):
        print("✓ 所有检查通过！项目可以正常运行")
        print("\n使用方法:")
        print("  1. pip install -e .")
        print("  2. devmate create \"你的应用描述\"")
        sys.exit(0)
    else:
        print("✗ 部分检查未通过，请先修复问题")
        sys.exit(1)

if __name__ == "__main__":
    main()
