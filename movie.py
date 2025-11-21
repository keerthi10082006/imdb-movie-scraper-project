from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Setup Chrome
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.imdb.com/chart/top/")
time.sleep(5)

data = []

# Select all movie rows
rows = driver.find_elements(By.XPATH, '//ul[contains(@class,"ipc-metadata-list")]/li')

print("Rows found:", len(rows))

for index, row in enumerate(rows, start=1):
    try:
        # Movie title
        title = row.find_element(By.XPATH, './/h3').text

        # Movie year
        year = row.find_element(By.XPATH, './/span[contains(text(),"(")]').text

        # Movie rating (star)
        rating = row.find_element(By.XPATH, './/span[contains(@class,"ipc-rating-star--rating")]').text

        data.append({
            "Rank": index,
            "Title": title,
            "Year": year,
            "Rating": rating
        })

    except Exception as e:
        print("Error:", e)
        continue

driver.quit()

df = pd.DataFrame(data)

df.to_csv("imdb_top250.csv", index=False)
print("CSV saved successfully!")