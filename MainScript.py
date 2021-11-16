from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import os


def scrape_page(pages):
    for page_name in pages:
        #Creating the empty lists in which we will place data
        ids= []
        products = []
        prices = []
        categories = []
        page_number = []

        #Creating the folder in which we will place the html files
        dir = f"html_{str(pd.to_datetime('today').day)}th"
        if not os.path.exists(dir):
            os.makedirs(dir)  

        # To get over the deprecation warning, create a service object   
        service = Service(ChromeDriverManager().install())

        # Create new driver instance
        wd = webdriver.Chrome(service=service)

        #Getting the html code of the page and saving it in a list
        wd.get(f"https://www.emag.ro/{page_name}/p1/c")
        soup = BeautifulSoup(wd.page_source, 'html.parser')
        raw_html = list(soup.find_all(class_ = "hidden-xs hidden-sm"))

        #Getting the total number of pages to be able to iterate automatically through them
        nr_pages = []
        for i in raw_html:  
            try:
                nr_pages.append(str(i).split("data-page=")[1].split("href")[0].replace("\'","").replace("\"","").replace(" ", ""))
            except IndexError:
                nr_pages.append("0")
        nr_pages = [int(x) for x in nr_pages]

        #Scraping each page and writing it to a html file
        for i in range(1,int(max(nr_pages))+1): 
            wd.get(f"https://www.emag.ro/{page_name}/p{i}/c")
            time.sleep(5)
            with open(f"html_{str(pd.to_datetime('today').day)}th/emag_source_{page_name}{i}.html", "w",encoding='utf-8') as file:
                file.write(wd.page_source)


        #Next, we will iterate through each html file and append the items we are interested in to each list
        for p in range(1,int(max(nr_pages))+1):
            with open(f"html_{str(pd.to_datetime('today').day)}th/emag_source_{page_name}{p}.html", "r", encoding='utf-8') as f:
                html_text = f.read()
                soup = BeautifulSoup(html_text, 'html.parser')
                raw_html = list(soup.find_all(class_ = "card-v2-toolbox"))
                for i in raw_html:
                    try:
                        ids.append(str(i).split("data-productid=")[1].split("data")[0].replace("\"",""))
                    except IndexError:
                        ids.append("No ID Available")
                    try:
                        products.append(str(i).split("product_name\"")[1].split(",\"options")[0].replace(":","").replace("u00ae", "").replace("\"",""))
                    except IndexError:
                        products.append("No name Available")
                    try:
                        prices.append(str(i).split("price\"")[1].split(",\"cate")[0].replace(":",""))
                    except IndexError:
                        prices.append("No price Available")
                    try:
                        categories.append(str(i).split("category_trail\":\"")[1].split("\",\"scm")[0].replace("&amp; ","").replace("/",""))
                    except IndexError:
                        categories.append("No Category Available")
                    try:
                        page_number.append(str(p))
                    except IndexError:
                        page_number.append("No page nr available")
            print (f"{page_name} is done.")

        #Create the dataframe and export it  
        df = pd.DataFrame(data = {"Id": ids, "Products" : products, "Price" : prices, "Category" : categories, 'ExtractionDate': pd.to_datetime('today'), 'Page_Number' : page_number})
        df.to_csv(f"day_{str(pd.to_datetime('today').day)}th_{page_name}.csv")


to_scrap = ["desktop-pc"]  #just an example of category
scrape_page(to_scrap)