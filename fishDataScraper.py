from bs4 import BeautifulSoup
import requests

nevada_stock_url = "https://www.ndow.org/get-outside/fishing/fishing-stocking-reports/database/?region=all&show_all=true"

##response = requests.get(nevada_stock_url)

##soup = BeautifulSoup(response.text, 'html.parser')

lake = input("Enter the lake name: ")


## Find the lake based on user input sends call to extract stocking updates if found
def lake_finder(input_lake, nevada_stock_url):
    link_next = nevada_stock_url
    while(True):
        response = requests.get(link_next)

        soup = BeautifulSoup(response.text, 'html.parser')
        
        grids = soup.find_all("div", class_="grid__item")

        for grid in grids:
            print("Checking lake...")
            ## Handles two different card styles on the page
            if grid.find_next("h6").get("class") == ["job-cart__title"]: 
                name = grid.find_next("h6", class_="job-cart__title").get_text(strip=True) 
                if name == input_lake:
                    link = grid.find("a")["href"]
                    extract_stocking_updates(link)
                    return 
            elif grid.find_next("h6").get("class") == ["database-card__title"]:
                name = grid.find_next("h6", class_="database-card__title").get_text(strip=True) 
                if name == input_lake:
                    link = grid.find("a")["href"]
                    extract_stocking_updates(link)
                    return 
        link_next = check_next_page(link_next)
    print("Lake not found.")
    return False


def extract_stocking_updates(url_of_page):
    response = requests.get(url_of_page)
    soup = BeautifulSoup(response.text, 'html.parser')
    

    header = soup.find("h4", class_= "tac", string = "Stocking Updates")

    if header:
        table = header.find_next("table")

        if table:
            rows = table.find_all("tr")
            for row in rows:
                cells = [cell.get_text(strip=True) for cell in row.find_all(["td", "th"])]
                print(cells)
        else:
            print("No table found after the 'Stocking Updates' header.")
    else:
        print("Header 'Stocking Updates' not found.")


## function to find next page link
def check_next_page(url_of_page):
    response = requests.get(url_of_page)
    soup = BeautifulSoup(response.text, 'html.parser')
    header = soup.find("li", class_ = "active")

    if header:
        link = header.find_next("a")["href"]
        print(link)
        return link
    else:
        print("No next page found.")
        return None
    

lake_finder(lake, nevada_stock_url)



    