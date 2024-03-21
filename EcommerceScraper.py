import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

class EcommerceScraper:
    """
    A class to scrape product data from Romania's largest ecommerce website, eMag.
    
    Attributes:
        categories (list): List of categories to scrape.
        nr_pages (int): Number of pages to scrape per category.
    """
    
    def __init__(self, categories, nr_pages):
        """
        Initializes the EcommerceScraper with categories and number of pages.
        
        Args:
            categories (list): Categories to scrape.
            nr_pages (int): Number of pages to scrape.
        """
        self.categories = categories
        self.nr_pages = nr_pages
        self.scraped_data = pd.DataFrame()
    
    def scrape_categories(self):
        """
        Main method to orchestrate scraping of specified categories and pages.
        """
        for category in self.categories:
            self._scrape_category(category)
        self._save_data_to_csv()
        
    def _scrape_category(self, category):
        """
        Scrapes data for a single category.
        
        Args:
            category (str): The category to scrape.
        """
        ids, products, prices, categories, page_numbers = [], [], [], [], []
        driver = self._create_webdriver_instance()
        
        for page in range(1, self.nr_pages + 1):
            driver.get(f"https://www.emag.ro/{category}/p{page}/c")
            time.sleep(5)  # Sleep to allow page to load
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            self._extract_data(soup, ids, products, prices, categories, page_numbers, page)
        
        driver.quit()
        print(f"Category '{category}' has been scraped successfully.")
        self._append_to_scraped_data(ids, products, prices, categories, page_numbers, category)
    
    def _create_webdriver_instance(self):
        """
        Creates and returns a new instance of a Selenium WebDriver.
        
        Returns:
            WebDriver instance.
        """
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service)
    
    def _extract_data(self, soup, ids, products, prices, categories, page_numbers, page):
        """
        Extracts data from a BeautifulSoup object and appends it to the provided lists.
        
        Args:
            soup (BeautifulSoup): BeautifulSoup object containing the page source.
            ids (list): List to append extracted product IDs.
            products (list): List to append extracted product names.
            prices (list): List to append extracted product prices.
            categories (list): List to append extracted product categories.
            page_numbers (list): List to append page numbers for tracking.
            page (int): Current page number being scraped.
        """
        raw_html = list(soup.find_all(class_="card-v2-toolbox"))
        for p in raw_html:
            # Extracting and appending data using exception handling to manage missing values
            # Each try-except block attempts to extract specific data; on failure, appends a placeholder
            try:
                ids.append(str(p).split("data-productid=")[1].split("data")[0].replace("\"",""))
            except IndexError:
                ids.append("No ID Available")
            try:
                products.append(str(p).split("product_name\"")[1].split(",\"options")[0].replace(":","").replace("u00ae", "").replace("\"",""))
            except IndexError:
                products.append("No name Available")

            try:
                prices.append(str(p).split("price\"")[1].split(",\"cate")[0].replace(":",""))
            except IndexError:
                prices.append("No price Available")

            try:
                categories.append(str(p).split("category_trail\":\"")[1].split("\",\"scm")[0].replace("&amp; ","").replace("/",""))
            except IndexError:
                categories.append("No Category Available")

            # Append the current page number
            page_numbers.append(page)
    
    def _append_to_scraped_data(self, ids, products, prices, categories, page_numbers, category):
        """
        Appends extracted data to the class's main DataFrame.
        
        Args:
            ids (list): List of product IDs.
            products (list): List of product names.
            prices (list): List of product prices.
            categories (list): List of product categories/subcategories.
            page_numbers (list): List of page numbers corresponding to each product.
            category (str): The main category for the products.
        """
        category_df = pd.DataFrame({
            "ProductID": ids,
            "Category": category,
            "Subcategory": categories,
            "Products": products,
            "Price": prices,
            'ExtractionDate': pd.to_datetime('today'),
            'PageNumber': page_numbers
        })
        self.scraped_data = pd.concat([self.scraped_data, category_df])
    
    def _save_data_to_csv(self):
        """
        Saves the scraped data to a CSV file.
        """
        filename = f"Scrape_eMag_day_{pd.to_datetime('today').strftime('%Y-%m-%d')}.csv"
        self.scraped_data.to_csv(filename, index=False)
        print(f"Data saved to {filename}")