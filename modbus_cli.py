import time
import sys
from typing import List, Optional

from pyModbusTCP.client import ModbusClient
from pyModbusTCP.constants import EXP_DATA_VALUE, EXP_ILLEGAL_FUNCTION
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich import print as rprint

# --- CONFIGURATION ---
DEFAULT_IP = "0.0.0.0"
DEFAULT_PORT = 5020
UNIT_ID = 1
MAX_RETRIES = 5
RETRY_DELAY = 2  # Seconds


class ModbusApp:
    """A professional CLI application for Modbus TCP communication."""

    def __init__(self):
        self.console = Console()
        self.client: Optional[ModbusClient] = None
        self.server_ip = DEFAULT_IP
        self.server_port = DEFAULT_PORT

        # Map Modbus exceptions to user-friendly messages
        self.error_messages = {
            EXP_ILLEGAL_FUNCTION: "Illegal Function [01]: The server does not support this action.",
            EXP_DATA_VALUE: "Illegal Data Value [03]: The value is invalid.",
        }

    def display_header(self) -> None:
        """Clears the screen and shows the app header."""
        self.console.clear()
        header = Panel.fit(
            f"[bold cyan]Modbus TCP CLI Tool[/bold cyan]\n"
            f"[green]Status:[/green] [white]Connected to {self.server_ip}:{self.server_port}[/white]",
            border_style="blue",
            padding=(1, 2)
        )
        self.console.print(header)

    def setup_connection(self) -> bool:
        """Prompts for server details and establishes a connection."""
        self.console.clear()
        try:
            self.server_ip = Prompt.ask("[bold blue]Modbus Server IP / DNS[/bold blue]", default=DEFAULT_IP)
            self.server_port = IntPrompt.ask("[bold blue]Modbus Server Port[/bold blue]", default=DEFAULT_PORT)
            
            self.client = ModbusClient(
                host=self.server_ip, 
                port=self.server_port, 
                unit_id=UNIT_ID, 
                auto_open=True
            )

            with self.console.status("[bold yellow]Connecting to Modbus Server...") as status:
                for attempt in range(1, MAX_RETRIES + 1):
                    if self.client.open():
                        return True
                    
                    self.console.print(f"[yellow]⚠ Connection failed. Attempt {attempt}/{MAX_RETRIES}...[/yellow]")
                    time.sleep(RETRY_DELAY)
            
            rprint(f"[bold red]✘ Error:[/bold red] Could not connect to {self.server_ip} after {MAX_RETRIES} attempts.")
            return False

        except KeyboardInterrupt:
            rprint("\n[bold red]Setup cancelled by user.[/bold red]")
            return False

    def handle_read(self) -> None:
        """Logic for reading and displaying holding registers."""
        addr = IntPrompt.ask("[blue]Start Address[/blue]")
        count = IntPrompt.ask("[blue]Number of Registers[/blue]", default=1)
        
        regs = self.client.read_holding_registers(addr, count)
        
        if regs:
            table = Table(title=f"Registers at Address {addr}", header_style="bold magenta")
            table.add_column("Offset", justify="center", style="dim")
            table.add_column("Address", style="cyan")
            table.add_column("Value (Dec)", style="green")
            table.add_column("Value (Hex)", style="yellow")

            for i, val in enumerate(regs):
                table.add_row(str(i), str(addr + i), str(val), f"0x{val:04X}")
            
            self.console.print(table)
        else:
            rprint("[bold red]✘ Read Error:[/bold red] The server returned no data or timed out.")

    def handle_write(self) -> None:
        """Logic for writing to a single register with error handling."""
        addr = IntPrompt.ask("[orange3]Target Register Address[/orange3]")
        val = IntPrompt.ask("[orange3]Value to Write[/orange3]")
        
        if self.client.write_single_register(addr, val):
            rprint(f"[bold green]✔ Success:[/bold green] Wrote [white]{val}[/white] to Register [white]{addr}[/white]")
        else:
            err_code = self.client.last_except
            msg = self.error_messages.get(err_code, f"Unknown Modbus Error (Code {err_code})")
            
            if err_code == 0:
                rprint("[bold red]✘ Connection Error:[/bold red] Server is unreachable.")
            else:
                rprint(f"[bold red]✘ Modbus Exception:[/bold red] {msg}")

    def run(self) -> None:
        """Main application loop."""
        if not self.setup_connection():
            return

        self.display_header()
        
        try:
            while True:
                choice = Prompt.ask(
                    prompt="\n[bold yellow]Menu[/bold yellow] -> [bold yellow]r[/bold yellow]ead, [bold yellow]w[/bold yellow]rite, [bold yellow]q[/bold yellow]uit",
                    choices=["r", "w", "q"],
                    default="r",
                    show_choices=False,
                ).lower()

                if choice in ["quit", "q"]:
                    rprint("[bold red]Disconnecting and exiting...[/bold red]")
                    break
                
                if choice in ["read", "r"]:
                    self.handle_read()
                elif choice in ["write", "w"]:
                    self.handle_write()

        except KeyboardInterrupt:
            rprint("\n[bold red]Session interrupted.[/bold red]")
        finally:
            if self.client:
                self.client.close()


if __name__ == "__main__":
    app = ModbusApp()
    app.run()