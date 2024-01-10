import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from rich import print

# The category for which we seek reviews
CATEGORY = "kfc"
# The location
LOCATION = "karachi"
# Google's main URL
URL = "https://www.google.com/maps"

if __name__ == '__main__':
    with sync_playwright() as pw:
        # Creates an instance of the Chromium browser and launches it in headless mode
        browser = pw.chromium.launch(headless=True)
        # Creates a new browser page (tab) within the browser instance
        page = browser.new_page()

        # Go to URL with Playwright page element
        page.goto(URL, wait_until="networkidle")

        # Fill in the search query and press Enter
        page.fill("input[aria-label='Search Google Maps']", CATEGORY + " " + LOCATION)
        page.keyboard.press('Enter')

        # Wait for the search results to load
        page.wait_for_selector('.hfpxzc', timeout=60000)

        # Get links of all categories after the search
        links = page.eval_on_selector_all('.hfpxzc', 'elements => elements.map(e => e.href)')

        # Go to the specific link (assuming the first link is the desired one)
        page.goto(links[1], wait_until="networkidle")

        # Load all reviews by clicking the 'Reviews' button
        page.locator("text='Reviews'").first.click()

        # Initialize variables for review scraping loop
        prev_review_count = 0
        reviews = []

        while True:
            # Scroll down to load more reviews
            page.mouse.wheel(0, 5000)  # Smaller scroll increment for more controlled loading
            time.sleep(3)  # Allow time for new reviews to load

            # Extract reviews using BeautifulSoup
            html = page.inner_html('body')
            soup = BeautifulSoup(html, 'html.parser')
            current_reviews = soup.select('.MyEned')
            current_review_count = len(current_reviews)

            # Check if no new reviews were loaded
            if current_review_count == prev_review_count:
                break
            else:
                reviews.extend(current_reviews)
                prev_review_count = current_review_count

        # Extract review texts
        review_texts = [review.find('span', class_='wiI7pd').text for review in reviews if review.find('span', class_='wiI7pd')]

        # Print the final count of reviews
        print(review_texts)
