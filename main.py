from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
URL = "https://ads.tiktok.com/business/creativecenter/top-products/pc/en"
CHROME_PATH = "D:\Development\chromedriver.exe"
REGION = ["VN", "MX", "ID", "PH", "US", "TH", "GB", "BR", "TR"]

driver_service = Service(executable_path=CHROME_PATH)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")
driver = webdriver.Chrome(options=options, service=driver_service)
wait = WebDriverWait(driver, 30)

categories = []
subcategories = []
popularities = []
popularities_change = []
ctr_s = []
cvr_s = []
cpa_s = []
costs = []
likes = []
shares = []
comments = []
impressions = []
view_rate_6s_s = []
Country = []
countries = [8, 22, 33, 41, 46, 54, 55, 57, 58, 60]
driver.get(URL)
time.sleep(3)

for i in countries:

    country = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='CategoryFilterRegion']/span/div/div/div")))
    driver.execute_script("arguments[0].click();", country)
    choose_country = wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[3]/div/div/div/div/div[2]/div[{i}]/div/div/span/div")))
    driver.execute_script("arguments[0].click();", choose_country)
    time.sleep(3)
    for j in range(1, 26):
        bsoup = BeautifulSoup(driver.page_source, "html.parser")
        list_products = bsoup.find_all("tr", {"class": "byted-Table-Row"})

        for product in list_products[1:]:
            values = product.find_all("td")

            category_name = values[0].find("div", {"class": "creative-component-single-line categoryName--xLgfj categoryName--xLgfj"})
            categories.append(category_name.text)

            subcategory_name = values[0].find("div", {
                "class": "creative-component-single-line categoryLevel--vTn4o categoryLevel--vTn4o"})
            subcategories.append(subcategory_name.text)

            cost = values[6].text
            costs.append(cost)

            popularity_change = values[2].text
            popularities_change.append(popularity_change)

            ctr = values[3].text
            ctr_s.append(ctr)

            cvr = values[4].text
            cvr_s.append(cvr)

            cpa = values[5].text
            cpa_s.append(cpa)

            popularity = values[1].text
            popularities.append(popularity)
            like = values[7].text
            likes.append(like)

            share = values[8].text
            shares.append(share)

            comment = values[9].text
            comments.append(comment)

            impression = values[10].text
            impressions.append(impression)

            view_rate_6s = values[11].text
            view_rate_6s_s.append(view_rate_6s)

            Country.append(i)
        time.sleep(2)
        next_page = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='ccContentContainer']/div[2]/div/div[3]/div[4]/button[2]")))
        next_page.click()
    time.sleep(3)


data = pd.DataFrame({"Category": categories, "Subcategory": subcategories, "Country": Country, "Popularity": popularities,
                     "Popularity change": popularities_change, "CTR": ctr_s, "CVR": cvr_s, "CPA": cpa_s, "Cost": costs,
                     "Likes": likes, "Shares": shares, "Comments": comments, "Impressions": impressions, "6s View Rate":
                    view_rate_6s_s})

data.to_csv("my_data.xlsx", index=False)


