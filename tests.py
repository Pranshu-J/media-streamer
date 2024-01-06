from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup

def run(playwright):
    browser = playwright.chromium.launch()
    context = browser.new_context()
    # Open new page
    page = context.new_page()
    # Go to website
    page.goto("https://goku.sx/series/watch-south-park-39503")
    # Get page content
    page_content = page.content()
    # Close page
    page.close()
    # Shutdown browser
    browser.close()

    # Use BeautifulSoup to parse the page content
    soup = BeautifulSoup(page_content, 'html.parser')

    # Find the div with the class "seasons"
    seasons_div = soup.findAll('a', {'class': 'dropdown-item ss-item'})

    if seasons_div is not None:
        for i in range(len(seasons_div)):
            print("Season {}".format(i+1))
            url = "https://goku.sx/ajax/movie/season/episodes/"+seasons_div[i].get('data-id')
            divs = BeautifulSoup(requests.get(url).text, 'html.parser').find_all('div', class_='item')
            for div in divs:
                print(div.get_text(strip=True))
                print("goku.sx"+div.find('a', class_='btn-onair ep-item')['href'])
        try:
            print("Season {}".format(i+2))
            for j in soup.findAll('a', {'class': 'btn-onair ep-item'}):
                print(j.get_text(strip=True))
                print("goku.sx"+j.get('href'))
        except:
            print("Season 1")
            for j in soup.findAll('a', {'class': 'btn-onair ep-item'}):
                print(j.get_text(strip=True))
                print("goku.sx"+j.get('href'))
    else:
        print("No div with class 'seasons' found.")

# Run the playwright code
with sync_playwright() as p:
    run(p)