#py-stock
#Valver-Dev - Manu Valverde
#December 2021

from typing import Optional
import typer 
from rich.console import Console
from rich.table import Table
from model import Item
from database import insert_item, get_stock, get_filtered_stock, update_item, delete_item

console = Console()

app = typer.Typer()

def get_color_category(category: str):
    COLORS = {'Herramientas': 'cyan', 'Material': 'magenta', 'Menaje': 'green'}
    if category in COLORS:
        return COLORS[category]
    return 'white'


def get_color_uds(uds: int):
    if uds <= 10:
        return 'red'
    elif uds <= 25:
        return 'yellow'
    else:
        return 'white'


def draw_table(stock: []):
    console.print("[bold magenta]Stock[/bold magenta]")
    
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#",style="dim",width=6)
    table.add_column("Item",min_width=20)
    table.add_column("Category",min_width=12)
    table.add_column("Uds",min_width=10, justify="right")
    
    for item in stock:
        colorCat = get_color_category(item.category)
        colorUds = get_color_uds(item.uds)
        table.add_row(str(item.id), item.name, f'[bold {colorCat}]{item.category}[/bold {colorCat}]', f'[bold {colorUds}]{str(item.uds)}[/bold {colorUds}]')
    
    console.print(table)
        

@app.command(short_help='New item in stock')
def new(name: str, category: str, uds: int):
    it = Item(0, name, category, uds)
    insert_item(it)
    typer.echo(f"Adding {uds} {name} in {category}")
    show()

@app.command(short_help='Add uds to item')
def add(id: int, uds: int):
    update_item(id,None,uds)
    typer.echo(f"Adding {uds} uds to {id}")
    show()

@app.command(short_help='Subtract uds from item')
def sub(id: int, uds: int):
    update_item(id, None,uds * -1)
    typer.echo(f"Subtracting {uds} uds from {id}")
    show()

@app.command(short_help='Delete item')
def delete(id: int):
    delete_item(id)
    typer.echo(f"Deleting item: {id} from stock")
    show()

@app.command(short_help='Show Stock')
def show():
    stock = get_stock()
    
    draw_table(stock)

@app.command(short_help='Show Stock Filtered by Name')
def show_filtered(filter: str, crit: str):
    if filter == 'item':
        stock = get_filtered_stock(filter, Item(None,crit,None,None))
    elif filter == 'category':
        stock = get_filtered_stock(filter, Item(None,None,crit,None))
    else:       
        stock = []

    draw_table(stock)

if __name__ == '__main__':
    app()