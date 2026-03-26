# devmate/cli.py
import typer
from pathlib import Path
from .agent import generate_project

app = typer.Typer(
    name="devmate",
    help="DevMate: Generate full-stack web applications from natural language descriptions.",
    add_completion=False
)

@app.command()
def create(
    prompt: str = typer.Argument(..., help="Describe your app in one sentence (e.g., 'A todo app with user login and data persistence')"),
    output: str = typer.Option("./", "--output", "-o", help="Output directory"),
):
    """
    Generate a full-stack web application from a natural language description.
    
    Examples:
    
        devmate create "A blog with markdown editor and user authentication"
        
        devmate create "Task management app with drag-and-drop interface" -o ./my-app
    """
    output_path = Path(output).resolve()
    output_path.mkdir(parents=True, exist_ok=True)
    generate_project(prompt, output_path)

@app.command()
def version():
    """Show version information."""
    typer.echo("DevMate v0.1.0 (MVP)")

@app.command()
def list_templates():
    """List available project templates."""
    templates = [
        "react-fastapi (default) - React + Vite + Tailwind + FastAPI + SQLite",
        "nextjs-fastapi - Next.js + FastAPI (coming soon)",
        "sveltekit-hono - SvelteKit + Hono (coming soon)",
        "vue-express - Vue 3 + Express (coming soon)"
    ]
    typer.echo("\nAvailable Templates:\n")
    for template in templates:
        typer.echo(f"  - {template}")
    typer.echo("\nMore templates coming soon!\n")

if __name__ == "__main__":
    app()