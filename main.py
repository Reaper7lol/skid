import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we get a valid response
    console.print("[bold green]HTML Content:[/bold green]")
    console.print(response.text)

def fetch_css(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    css_links = [link['href'] for link in soup.find_all('link', rel='stylesheet')]
    if css_links:
        console.print("[bold green]CSS Files Found:[/bold green]")
        for css_link in css_links:
            console.print(css_link)
    else:
        console.print("[bold red]No CSS files found.[/bold red]")

def fetch_js(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    js_links = [script['src'] for script in soup.find_all('script') if script.get('src')]
    if js_links:
        console.print("[bold green]JavaScript Files Found:[/bold green]")
        for js_link in js_links:
            console.print(js_link)
    else:
        console.print("[bold red]No JavaScript files found.[/bold red]")

def extract_links(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    links = [a['href'] for a in soup.find_all('a', href=True)]
    console.print("[bold green]Links Found:[/bold green]")
    for link in links:
        console.print(link)

def extract_images(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    images = [img['src'] for img in soup.find_all('img', src=True)]
    console.print("[bold green]Images Found:[/bold green]")
    for img in images:
        console.print(img)

def extract_meta_tags(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    meta_tags = {meta.get('name'): meta.get('content') for meta in soup.find_all('meta') if meta.get('name')}
    console.print("[bold green]Meta Tags Found:[/bold green]")
    for name, content in meta_tags.items():
        console.print(f"{name}: {content}")

def download_html_structure(url):
    response = requests.get(url)
    response.raise_for_status()
    with open("downloaded_structure.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    console.print("[bold green]HTML structure downloaded to 'downloaded_structure.html'.[/bold green]")

def download_css_files(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    css_links = [link['href'] for link in soup.find_all('link', rel='stylesheet')]
    for css_link in css_links:
        css_response = requests.get(css_link if css_link.startswith("http") else url + css_link)
        with open(css_link.split("/")[-1], "w", encoding="utf-8") as file:
            file.write(css_response.text)
    console.print("[bold green]CSS files downloaded.[/bold green]")

def download_js_files(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    js_links = [script['src'] for script in soup.find_all('script') if script.get('src')]
    for js_link in js_links:
        js_response = requests.get(js_link if js_link.startswith("http") else url + js_link)
        with open(js_link.split("/")[-1], "w", encoding="utf-8") as file:
            file.write(js_response.text)
    console.print("[bold green]JavaScript files downloaded.[/bold green]")

# User interface to display options
def display_menu():
    console.print("[bold red]SKID TOOL[/bold red]", justify="center")
    console.print("tierhof.xyz", justify="center")
    console.print()

    table = Table(show_header=False, box=None)
    table.add_column("")

    network_scraper_table = Table(show_header=False, box=None)
    network_scraper_table.add_row("[01] Fetch HTML Content")
    network_scraper_table.add_row("[02] Fetch CSS Content")
    network_scraper_table.add_row("[03] Fetch JavaScript Content")
    network_scraper_table.add_row("[04] Extract Links")
    network_scraper_table.add_row("[05] Extract Images")
    network_scraper_table.add_row("[06] Extract Meta Tags")

    table.add_row(
        Panel(
            network_scraper_table,
            title="[bold red]Network Scraper[/bold red]",
            border_style="red",
        )
    )

    script_collector_table = Table(show_header=False, box=None)
    script_collector_table.add_row("[07] Download HTML Structure")
    script_collector_table.add_row("[08] Download CSS Files")
    script_collector_table.add_row("[09] Download JS Files")

    table.add_row(
        Panel(
            script_collector_table,
            title="[bold red]Script Collector[/bold red]",
            border_style="red",
        )
    )

    console.print(table)
    console.print("[bold]Choose an option (e.g., 01) and enter a URL when prompted.[/bold]")

def main():
    display_menu()
    choice = console.input("[bold red]$ [/bold red]").strip()
    url = console.input("Enter the website URL: ").strip()

    # Execute the selected function based on user input
    if choice == "01":
        fetch_html(url)
    elif choice == "02":
        fetch_css(url)
    elif choice == "03":
        fetch_js(url)
    elif choice == "04":
        extract_links(url)
    elif choice == "05":
        extract_images(url)
    elif choice == "06":
        extract_meta_tags(url)
    elif choice == "07":
        download_html_structure(url)
    elif choice == "08":
        download_css_files(url)
    elif choice == "09":
        download_js_files(url)
    else:
        console.print("[bold red]Invalid option. Please try again.[/bold red]")

if __name__ == "__main__":
    main()

