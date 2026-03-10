#!/usr/bin/env python3
# HormigasAIS - Panel de Control Air City v1.0
import os
import time
import subprocess
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live

# Configuración de Rutas
CASTA_DIR = os.path.expanduser("~/HormigasAIS-Nodo-Escuela/INCUBADORA_AIR_CITY")
NODOS = [f"CASTA_{i}" for i in range(1, 8)]
LOG_FILE = os.path.join(CASTA_DIR, "bus_consenso.log")

console = Console()

def get_battery():
    """Obtiene la batería real en Termux o devuelve 100 por defecto."""
    try:
        res = subprocess.run(["termux-battery-status"], capture_output=True, text=True, timeout=1)
        if res.returncode == 0:
            import json
            data = json.loads(res.stdout)
            return int(data.get("percentage", 100))
    except:
        pass
    return 100

def leer_estado_nodos():
    estados = {}
    for nodo in NODOS:
        # Buscamos el rastro de feromona digital (voto.tmp)
        voto_path = os.path.join(CASTA_DIR, nodo, "voto.tmp")
        estados[nodo] = "🟢 ACTIVO" if os.path.exists(voto_path) else "🔴 INACTIVO"
    return estados

def generar_dashboard():
    estados = leer_estado_nodos()
    votos = sum(1 for v in estados.values() if "ACTIVO" in v)
    bateria_real = get_battery()
    
    # Crear Tabla de Nodos
    table = Table(show_header=True, header_style="bold magenta", expand=True, box=None)
    table.add_column("UNIDAD", justify="left")
    table.add_column("ESTADO", justify="right")
    
    for nodo, estado in estados.items():
        table.add_row(f"🐜 {nodo}", estado)

    # Lógica de Color para Consenso
    status_color = "bold green" if votos >= 4 else "bold red"
    status_text = "SOBERANÍA CONFIRMADA" if votos >= 4 else "ALERTA: CONSENSO INSUFICIENTE"

    # Panel Principal con rastro de feromonas digitales
    main_content = Panel(
        table,
        title="[bold yellow]• • • FEROMONAS DIGITALES • • •[/bold yellow]",
        subtitle=f"[{status_color}]{status_text}[/{status_color}]",
        border_style="cyan"
    )

    return main_content, votos, bateria_real

def run():
    try:
        with Live(console=console, screen=True, refresh_per_second=1) as live:
            while True:
                panel, votos, bat = generar_dashboard()
                
                # Construcción de la pantalla
                grid = Table.grid(expand=True)
                grid.add_column()
                
                # Encabezado con rastro de puntos
                grid.add_row(Panel(f"[bold white]HormigasAIS[/bold white] [dim]v1.0 - San Miguel, SV[/dim]\n[yellow]· · · · · · · · · · · · · · · · · · · · · · ·[/yellow]", style="blue"))
                
                # Cuerpo central
                grid.add_row(panel)
                
                # Barra de Energía
                prog = f"[bold white]Energía Crítica: {bat}%[/bold white]" if bat < 25 else f"Energía: {bat}%"
                grid.add_row(Panel(f"{prog} [cyan]{'▮' * (bat // 5)}{'▯' * (20 - (bat // 5))}[/cyan]", border_style="dim"))
                
                live.update(grid)
                time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n[bold red]Terminando monitoreo de la colonia...[/bold red] 🐜")

if __name__ == "__main__":
    run()

