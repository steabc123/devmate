from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="devmate",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Your AI-Powered Full-Stack Developer Agent - Generate complete web apps from natural language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourname/devmate",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "typer>=0.12.0",
        "jinja2>=3.1.0",
        "fastapi>=0.115.0",
        "uvicorn[standard]>=0.32.0",
        "sqlalchemy>=2.0.0",
        "pydantic>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "devmate=cli:app",
        ],
    },
    include_package_data=True,
    package_data={
        "devmate": ["templates/**/*"],
    },
)
