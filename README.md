# Web Scraping Ecommerce Website

The web scraper is a Python-based tool designed for scraping product data from eMag's website, covering various categories and pages. The script utilizes Selenium for web scraping, ensuring accurate and up-to-date information is captured directly from the web pages.

## Features

- Scrape product data across multiple categories.
- Configurable to scrape multiple pages per category.
- Data includes product ID, name, price, category, extraction date, and more.
- Saves scraped data to a CSV file for easy use and analysis.

## Usage

To use the eMag Scraper, follow these steps:

1. Import the EMagScraper class from the script.

```bash
from EcommerceScraper import EcommerceScraper
```
2. Create an instance of the EcommerceScraper class, specifying the categories and number of pages to scrape per each category.

```bash
categories_to_scrape = ["desktop-pc", "laptopuri"]
nr_pages = 5
scraper = EMagScraper(categories_to_scrape, nr_pages)
```

3. Call the scrape_categories method to start the scraping process.
  
```bash
scraper.scrape_categories()
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
