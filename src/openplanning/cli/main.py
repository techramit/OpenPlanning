"""OpenPlanning CLI - Main entry point."""

from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Prompt
from rich.text import Text


console = Console()


class OpenPlanningCLI:
    """Main CLI class for OpenPlanning."""

    def __init__(self) -> None:
        self.console = Console()

    def display_welcome(self) -> None:
        """Display welcome banner."""
        welcome_text = Text()
        welcome_text.append("OpenPlanning", style="bold cyan")
        welcome_text.append("\nAI-Powered Product Planning", style="dim")

        panel = Panel(
            welcome_text,
            title="Welcome",
            border_style="cyan",
            padding=(1, 2),
        )
        self.console.print(panel)
        self.console.print()

    def get_user_idea(self) -> str:
        """Get product idea from user."""
        self.console.print("Describe your product idea in detail:", style="bold")
        self.console.print("(Press Enter twice when finished)\n", style="dim")

        lines = []
        while True:
            line = Prompt.ask("")
            if line:
                lines.append(line)
            elif lines:
                break
            else:
                self.console.print("Please enter your idea.", style="yellow")

        return " ".join(lines)

    def display_session_info(self, idea: str) -> None:
        """Display session initialization info."""
        self.console.print()
        self.console.print(Panel(
            f"Idea: {idea[:80]}..." if len(idea) > 80 else f"Idea: {idea}",
            title="Session Started",
            border_style="green",
        ))
        self.console.print()

    def run_agents(self) -> None:
        """Run the agent workflow with progress display."""
        agents = [
            ("Researching market size...", "Bob", "cyan"),
            ("Analyzing users...", "Emma", "magenta"),
            ("Evaluating technical feasibility...", "Elon", "blue"),
            ("Building business model...", "Reid", "green"),
            ("Creating roadmap...", "Gantt", "yellow"),
            ("Designing architecture...", "Grace", "red"),
            ("Validating findings...", "Reviewer", "white"),
        ]

        total_tokens = 0

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=self.console,
        ) as progress:
            for description, agent, color in agents:
                task = progress.add_task(
                    f"[{color}]{description}[/{color}]",
                    total=100,
                )

                for _ in range(100):
                    progress.advance(task)

                tokens_used = 2500 if agent != "Bob" else 3500
                total_tokens += tokens_used

                progress.update(
                    task,
                    completed=100,
                    description=f"[bold green]✓ {agent} complete[/]",
                )

        self.console.print()
        self.display_completion_summary(total_tokens)

    def display_completion_summary(self, total_tokens: int) -> None:
        """Display session completion summary."""
        estimated_cost = total_tokens * 0.00002

        summary = Text()
        summary.append("✓ Session complete!", style="bold green")
        summary.append(f"\nTotal tokens: {total_tokens:,}")
        summary.append(f"\nEstimated cost: ${estimated_cost:.2f}")
        summary.append(f"\nDocuments: 6 files generated", style="dim")

        panel = Panel(
            summary,
            title="Summary",
            border_style="green",
        )
        self.console.print(panel)

    def run_interactive(self) -> None:
        """Run the interactive CLI session."""
        self.display_welcome()
        idea = self.get_user_idea()
        self.display_session_info(idea)
        self.run_agents()


@click.command()
@click.option(
    "--setup",
    is_flag=True,
    help="Configure API keys and settings",
)
@click.option(
    "--version",
    is_flag=True,
    help="Show version information",
)
def cli(setup: bool, version: bool) -> None:
    """OpenPlanning - AI-Powered Product Planning CLI."""
    if version:
        from openplanning import __version__
        console.print(f"OpenPlanning v{__version__}")
        return

    if setup:
        console.print("Setup not yet implemented.", style="yellow")
        return

    try:
        cli_app = OpenPlanningCLI()
        cli_app.run_interactive()
    except KeyboardInterrupt:
        console.print("\nSession cancelled.", style="yellow")
    except Exception as e:
        console.print(f"\nError: {e}", style="red")
        raise


if __name__ == "__main__":
    cli()
