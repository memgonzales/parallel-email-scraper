import threading

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

DEPARTMENT = 'ST'
URL = f'https://www.dlsu.edu.ph/staff-directory/?search&filter=department&category={DEPARTMENT}'
DELAY = 30

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)

driver.get(URL)

personnels = None
while True:
    try:
        personnels = WebDriverWait(driver, DELAY).until(EC.presence_of_all_elements_located((By.NAME, "personnel")))
        break
    except TimeoutException:
        print("Increasing timeout window")
        DELAY += 5

print("Page is ready!")
#print(myElem)
for personnel in personnels:
    print(personnel.get_attribute('value'))
    print(personnel.get_attribute('innerHTML'))
    print()

driver.find_element(By.CSS_SELECTOR, ".btn.btn-success.btn-lg.btn-block.text-capitalize").click()

personnels = None
while True:
    try:
        personnels = WebDriverWait(driver, DELAY).until(EC.presence_of_all_elements_located((By.NAME, "personnel")))
        break
    except TimeoutException:
        print("Increasing timeout window")
        DELAY += 5



# emails = []
# found = False
# for a in soup.find_all('a',href=True):
#    test_em = a['href']
#    if test_em[:6] == "mailto":
#        emails.append(a['href'][7:])
#        found = True





class Crawler(threading.Thread):
    def __init__(self,base_url, links_to_crawl,have_visited, error_links,url_lock):
       
        threading.Thread.__init__(self)
        print(f"Web Crawler worker {threading.current_thread()} has Started")
        self.base_url = base_url
        self.links_to_crawl = links_to_crawl
        self.have_visited = have_visited
        self.error_links = error_links
        self.url_lock = url_lock

    

