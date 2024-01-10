import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from rich import print


# the category for which we seek reviews
CATEGORY = "kfc"
# the location
LOCATION = "karachi"
# google's main URL
URL = "https://www.google.com/maps"


if __name__ == '__main__':
    with sync_playwright() as pw:
        # creates an instance of the Chromium browser and launches it
        browser = pw.chromium.launch(headless=True)
        # creates a new browser page (tab) within the browser instance
        page = browser.new_page()
        # go to url with Playwright page element
        page.goto(URL)
        time.sleep(15)
        # deal with cookies page
        # write what you're looking for
        page.fill("input", "kababjees")
        # press enter
        page.keyboard.press('Enter')
        # change to english
        time.sleep(4)
        # scrolling

            # tackle the body element
        html = page.inner_html('body')
        # create beautiful soup element
        soup = BeautifulSoup(html, 'html.parser')


        


        # get links of all categories after scroll
        links = [item.get('href') for item in soup.select('.hfpxzc')]
        # print(links)

 
            # go to subject link
        page.goto(links[1])
        time.sleep(4)
        # load all reviews
        page.locator("text='Reviews'").first.click()
        time.sleep(4)
        # create new soup
        prev_review_count = 0
        while True:
            # Scroll down
            page.mouse.wheel(0, 10000)
            
            # Wait for new reviews to load
            time.sleep(5)

            # Create new soup
            html = page.inner_html('body')
            # Create beautiful soup element
            soup = BeautifulSoup(html, 'html.parser')
            
            # Scrape reviews
            reviews = soup.select('.MyEned')
            current_review_count = len(reviews)

            # Check if no new reviews were loaded
            if current_review_count == prev_review_count:
                break
            prev_review_count = current_review_count
        review_texts = [review.find('span', class_='wiI7pd').text for review in reviews if review.find('span', class_='wiI7pd')]
        # Print the final count of reviews
        print(review_texts)
