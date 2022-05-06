from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time


# Chrome Driver func
def web_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("no-sandbox")
    options.add_argument('--dns-prefetch-disable')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--disable-extensions")
    return webdriver.Chrome(executable_path='./chromedriver.exe')

# Data Scraper from listings
def scraper():
    driver = web_driver()
    all_data = []
    with open('links.txt') as links_file:
        links = links_file.readlines()
        for url in links:
            driver.get(url)
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source,'html.parser')  
            try:
                price = soup.find('div',{'class':'_1jo4hgw'}).text
            except:
                pass
            try:
                toGetHost = soup.find_all('h2',{'class':'hnwb2pb dir dir-ltr'})
                hosted = toGetHost[4].text
                print(hosted)
            except:
                pass    
            data_dict ={
                "Listing Url":url,
                "Price" : price,
                "Hosted By": hosted
            }

            all_data.append(data_dict)
            df = pd.DataFrame(all_data)
            df.to_csv('listings.csv',index=False)
    
if __name__=="__main__":
    scraper()

