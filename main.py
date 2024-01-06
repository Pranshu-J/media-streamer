import requests
import m3u8_To_MP4
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def get_m3u8():
    url = ""
    m3u8_To_MP4.multithread_download(url)

def search_results(query):
    # Set the website URL
    query = "+".join(query.split(" "))
    url = 'https://goku.sx/search?keyword={}'.format(query)

    # Launch the browser
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()

        # Create a new browser context
        context = browser.new_context()

        # Open a new page
        page = context.new_page()

        # Navigate to the website
        page.goto(url)

        # Extract image URLs and titles
        image_elements = page.query_selector_all('.ls-is-cached.lazyloaded')
        image_urls = [element.get_attribute('src') for element in image_elements]
        title_elements = page.query_selector_all('.movie-name')
        titles = [element.inner_text() for element in title_elements]
        redirect_elements = page.query_selector_all('.movie-link')
        redirect_urls = [element.get_attribute('href') for element in redirect_elements]

        # Print the results
        for i in range(len(image_urls)):
            print('Image URL:', image_urls[i])
            print('Title:', titles[i])
            redirect_urls[i] = "https://goku.sx"+redirect_urls[i]
            print('Movie Link: ',redirect_urls[i])

        # Close the browser context
        context.close()

        # Close the browser
        browser.close()

def load_media(url):
    def run(playwright, url):
        browser = playwright.chromium.launch()
        context = browser.new_context()
        # Open new page
        page = context.new_page()
        # Go to website
        page.goto(url)
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
    with sync_playwright() as p:
        run(p,url)

load_media("https://goku.sx/series/watch-crash-landing-on-you-60127")