from playwright.sync_api import  sync_playwright
from playwright_stealth import stealth_sync
import pandas as pd
import random

class webscraper:
    def __init__(self):
        self.data = []

    def Browser(self, product):
        self.product = product
        with sync_playwright() as p:
            user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
]
            browser =  p.chromium.launch(headless = True, args=["--disable-blink-features=AutomationControlled", "--disable-gpu"])
            page = browser.new_page()
            stealth_sync(page)
            page.set_extra_http_headers({
                "User-Agent": random.choice(user_agents),
                "Accept-Language": "en-US,en;q=0.9"
            })
            
            page.goto("https://www.amazon.in", timeout = 40000)
            page.screenshot(path = "debug.png")
            
            page.get_by_placeholder("Search Amazon.in").fill(f"{self.product}")
            page.wait_for_selector("input#nav-search-submit-button", timeout = 20000 )
            page.locator("input#nav-search-submit-button").click()
            page.wait_for_selector("//h2[contains(@class,'a-size-medium a-spacing-none a-color-base a-text-normal')]", timeout = 10000)
            
            page.evaluate("window.scrollBy(0, document.body.scrollHeight)")


            page.evaluate("window.scrollBy(0, document.body.scrollHeight)")

           

            products = page.locator("//div[contains(@class,'a-section a-spacing-small a-spacing-top-small')]").all()
            

            for product in products:
                product_name = product.locator("h2 span").text_content().strip() if product.locator("h2 span").count() > 0 else "N/A"
                price = product.locator(".a-price-whole").text_content().strip() if product.locator(".a-price-whole").count() > 0 else "N/A"
                rating = product.locator("span.a-icon-alt").text_content().strip() if product.locator("span.a-icon-alt").count() > 0 else "N/A"

                self.data.append({
                    "Product" : product_name,
                    "Price" : price,
                    "Ratings" : rating
                })


            page.evaluate("window.scrollBy(0, document.body.scrollHeight)")


            
            page.close()

    def Data_in_csv(self):

        df = pd.DataFrame(self.data)

        df.to_csv(f"{self.product}.csv", index = False)
        print(df)



if __name__ == "__main__":
    browser = webscraper()
    print(browser.Browser("Bags"))
    print(browser.Data_in_csv())


