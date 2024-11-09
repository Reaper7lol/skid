import os
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import time
import sys

# Set up the console for rich formatting
console = Console()

# Install required libraries (if not already installed)
def install_requirements():
    required_libraries = ['requests', 'beautifulsoup4', 'rich']
    for lib in required_libraries:
        try:
            __import__(lib)
        except ImportError:
            console.print(f"[bold red]Installing {lib}...[/bold red]")
            os.system(f"pip install {lib}")
    console.print("[bold green]All dependencies installed![/bold green]")

# Auto-Bug Fixer: Tries to fix common errors
def auto_bug_fixer():
    try:
        install_requirements()
    except Exception as e:
        console.print(f"[bold red]Error occurred while installing dependencies: {e}[/bold red]")
        console.print("[bold green]Attempting to fix...[/bold green]")
        os.system("pip install --upgrade pip")
        os.system("pip install --upgrade requests beautifulsoup4 rich")
        console.print("[bold green]Attempted fix completed.[/bold green]")

# Helper function to create directory structure
def create_website_folder(url):
    # Normalize the URL to use as a folder name
    folder_name = url.replace("https://", "").replace("http://", "").replace("/", "_")
    if not os.path.exists(f"skids/{folder_name}"):
        os.makedirs(f"skids/{folder_name}")
    return folder_name

# Fetch HTML content
def fetch_html(url):
    try:
        folder_name = create_website_folder(url)
        response = requests.get(url)
        response.raise_for_status()
        html_file_path = f"skids/{folder_name}/index.html"
        with open(html_file_path, "w", encoding="utf-8") as file:
            file.write(response.text)
        console.print(f"[bold green]HTML Content saved to {html_file_path}[/bold green]")
    except requests.RequestException as e:
        console.print(f"[bold red]Error fetching HTML: {e}[/bold red]")

# Fetch CSS files
def fetch_css(url):
    try:
        folder_name = create_website_folder(url)
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        css_links = [link['href'] for link in soup.find_all('link', rel='stylesheet')]
        if css_links:
            console.print("[bold green]CSS Files Found:[/bold green]")
            for css_link in css_links:
                css_url = css_link if css_link.startswith("http") else url + css_link
                css_response = requests.get(css_url)
                css_file_name = os.path.basename(css_url)
                with open(f"skids/{folder_name}/{css_file_name}", "w", encoding="utf-8") as file:
                    file.write(css_response.text)
                console.print(f"[bold green]CSS file saved: {css_file_name}[/bold green]")
        else:
            console.print("[bold red]No CSS files found.[/bold red]")
    except requests.RequestException as e:
        console.print(f"[bold red]Error fetching CSS: {e}[/bold red]")

# Fetch JavaScript files
def fetch_js(url):
    try:
        folder_name = create_website_folder(url)
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        js_links = [script['src'] for script in soup.find_all('script') if script.get('src')]
        if js_links:
            console.print("[bold green]JavaScript Files Found:[/bold green]")
            for js_link in js_links:
                js_url = js_link if js_link.startswith("http") else url + js_link
                js_response = requests.get(js_url)
                js_file_name = os.path.basename(js_url)
                with open(f"skids/{folder_name}/{js_file_name}", "w", encoding="utf-8") as file:
                    file.write(js_response.text)
                console.print(f"[bold green]JavaScript file saved: {js_file_name}[/bold green]")
        else:
            console.print("[bold red]No JavaScript files found.[/bold red]")
    except requests.RequestException as e:
        console.print(f"[bold red]Error fetching JavaScript: {e}[/bold red]")

# Extract all links from the page
def extract_links(url):
    try:
        folder_name = create_website_folder(url)
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        links = [a['href'] for a in soup.find_all('a', href=True)]
        links_file_path = f"skids/{folder_name}/links.txt"
        with open(links_file_path, "w", encoding="utf-8") as file:
            for link in links:
                file.write(link + "\n")
        console.print(f"[bold green]Links saved to {links_file_path}[/bold green]")
    except requests.RequestException as e:
        console.print(f"[bold red]Error extracting links: {e}[/bold red]")

# Extract images from the page
def extract_images(url):
    try:
        folder_name = create_website_folder(url)
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        images = [img['src'] for img in soup.find_all('img', src=True)]
        images_file_path = f"skids/{folder_name}/images.txt"
        with open(images_file_path, "w", encoding="utf-8") as file:
            for img in images:
                file.write(img + "\n")
        console.print(f"[bold green]Images saved to {images_file_path}[/bold green]")
    except requests.RequestException as e:
        console.print(f"[bold red]Error extracting images: {e}[/bold red]")

# Extract meta tags from the page
def extract_meta_tags(url):
    try:
        folder_name = create_website_folder(url)
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        meta_tags = {meta.get('name'): meta.get('content') for meta in soup.find_all('meta') if meta.get('name')}
        meta_tags_file_path = f"skids/{folder_name}/meta_tags.txt"
        with open(meta_tags_file_path, "w", encoding="utf-8") as file:
            for name, content in meta_tags.items():
                file.write(f"{name}: {content}\n")
        console.print(f"[bold green]Meta tags saved to {meta_tags_file_path}[/bold green]")
    except requests.RequestException as e:
        console.print(f"[bold red]Error extracting meta tags: {e}[/bold red]")

# Create the main user interface
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

    console.print(table)
    console.print("[bold]Choose an option (e.g., 01) and enter a URL when prompted.[/bold]")

# Main function with auto-refresh feature
def main():
    auto_bug_fixer()  # Ensure requirements and bugs are handled first
    while True:
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
        else:
            console.print("[bold red]Invalid option. Please try again.[/bold red]")

        console.print("[bold green]Refreshing...[/bold green]")
        time.sleep(2)  # Pause before auto-refreshing
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console

if __name__ == "__main__":
    main()
