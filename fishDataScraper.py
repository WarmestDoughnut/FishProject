from bs4 import BeautifulSoup
import requests

nevada_stock_url = "https://www.ndow.org/get-outside/fishing/fishing-stocking-reports/database/?region=all&show_all=true"

response = requests.get(nevada_stock_url)

soup = BeautifulSoup(response.text, 'html.parser')

lake = input("Enter the lake name: ")

def lake_finder(input_lake):
    grids = soup.find_all("div", class_="grid__item")

    for grid in grids:
        print("Checking lake...")
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
        
    print("Lake not found.")
    return None



                    


    
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


lake_finder(lake)