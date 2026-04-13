"""OpenPlanning CLI - Main entry point."""

import os
import sys
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.prompt import Prompt
from rich.text import Text

console = Console()

# UI Constants for scalability
TITLE_ASCII = """

░█████╗░██████╗░███████╗███╗░░██╗
██╔══██╗██╔══██╗██╔════╝████╗░██║
██║░░██║██████╔╝█████╗░░██╔██╗██║
██║░░██║██╔═══╝░██╔══╝░░██║╚████║
╚█████╔╝██║░░░░░███████╗██║░╚███║
░╚════╝░╚═╝░░░░░╚══════╝╚═╝░░╚══╝
██████╗░██╗░░░░░░█████╗░███╗░░██╗███╗░░██╗██╗███╗░░██╗░██████╗░
██╔══██╗██║░░░░░██╔══██╗████╗░██║████╗░██║██║████╗░██║██╔════╝░
██████╔╝██║░░░░░███████║██╔██╗██║██╔██╗██║██║██╔██╗██║██║░░██╗░
██╔═══╝░██║░░░░░██╔══██║██║╚████║██║╚████║██║██║╚████║██║░░╚██╗
██║░░░░░███████╗██║░░██║██║░╚███║██║░╚███║██║██║░╚███║╚██████╔╝
╚═╝░░░░░╚══════╝╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚══╝╚═╝╚═╝░░╚══╝░╚═════╝░
"""

TITLE_STYLE = "bold bright_cyan"
SUBTITLE_STYLE = "#FFA500"
INPUT_PROMPT = "> "


class OpenPlanningCLI:
    """Main CLI class for OpenPlanning."""

    def __init__(self) -> None:
        self.console = Console()
        self.console.clear()

    def display_welcome(self) -> None:
        """Display welcome banner with ASCII art."""
        self.console.print(Text(TITLE_ASCII, style=TITLE_STYLE))
        self.console.print(Text("AI-Powered Product Planning\n", style=SUBTITLE_STYLE))

    def get_user_idea(self) -> str:
        """Get product idea from user."""
        self.console.print("Describe your product idea:", style="bold cyan")
        self.console.print("(Press Enter twice when finished)\n", style="dim")

        lines = []
        while True:
            line = Prompt.ask("> ",
                console=self.console,
                show_default=False,
            )
            if line:
                lines.append(line)
            elif lines:
                break
            else:
                self.console.print("Please enter your idea:", style="yellow")

        return " ".join(lines)

    def display_session_info(self, idea: str) -> None:
        """Display session initialization info."""
        truncated = idea[:77] + "..." if len(idea) > 80 else idea
        info_text = Text()
        info_text.append("Idea: ", style="dim")
        info_text.append(truncated, style="italic")

        panel = Panel(
            info_text,
            title=r"[Session Started]",
            border_style="bright_green",
            expand=False,
        )
        self.console.print(panel, justify="center")
        self.console.print()

    def run_agents(self) -> None:
        """Run the agent workflow with progress display."""
        agents = [
            ("Market Research", "Bob", "cyan", "Researching market size and competitors..."),
            ("User Research", "Emma", "magenta", "Creating personas and user stories..."),
            ("Technical Analysis", "Elon", "blue", "Evaluating technical feasibility..."),
            ("Business Model", "Reid", "green", "Building business model..."),
            ("Roadmap Planning", "Gantt", "yellow", "Creating implementation roadmap..."),
            ("Architecture", "Grace", "red", "Designing system architecture..."),
            ("Validation", "Reviewer", "bright_white", "Cross-checking all findings..."),
        ]

        total_tokens = 0

        with Progress(
            SpinnerColumn(finished_text="✓"),
            TextColumn("[progress.description]{task.description}", style="bright_black"),
            BarColumn(complete_style="bright_cyan", finished_style="bright_green"),
            console=self.console,
            expand=True,
        ) as progress:
            for name, agent, color, description in agents:
                task = progress.add_task(
                    f"[{color}]{description}",
                    total=100,
                )

                progress.update(task, advance=0)
                for _ in range(100):
                    progress.advance(task)

                tokens_used = 2500 if agent != "Bob" else 3500
                total_tokens += tokens_used

                progress.update(
                    task,
                    completed=100,
                    description=f"[bold green]✓ {agent} ({name})[/]",
                )

        self.console.print()
        self.display_completion_summary(total_tokens)

    def display_completion_summary(self, total_tokens: int) -> None:
        """Display session completion summary."""
        estimated_cost = total_tokens * 0.00001

        summary = Text()
        summary.append("✓ Session complete!\n", style="bold bright_green")
        summary.append(f"[{total_tokens:,} tokens] ", style="cyan")
        summary.append(f"[${estimated_cost:.2f}] ", style="green")
        summary.append("[6 docs]", style="dim")

        panel = Panel(
            summary,
            title=r"[Summary]",
            border_style="bright_green",
            expand=False,
        )
        self.console.print(panel, justify="center")

    def run_interactive(self) -> None:
        """Run the interactive CLI session."""
        self.display_welcome()
        self.console.print()
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
@click.option(
    "--effort",
    type=click.Choice(["low", "medium", "high", "max"], case_sensitive=False),
    default="medium",
    help="Research depth level",
)
def cli(setup: bool, version: bool, effort: str) -> None:
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
        sys.exit(1)
    except Exception as e:
        console.print(f"\nError: {e}", style="red")
        sys.exit(1)


if __name__ == "__main__":
    cli()
