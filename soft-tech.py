import multiprocessing
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

URL = f'https://www.dlsu.edu.ph/staff-directory/'
staff_URL = f'https://www.dlsu.edu.ph/staff-directory/?personnel='
email_class = '.btn.btn-sm.btn-block.text-capitalize'
dept_position = 'dlsu-pvf-mt-1'
name_class = '.col-lg-12.col-md-12.col-sm-12 col-xs-12'

# Set the delay to 300 seconds (5 minutes).
DELAY = 300

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

DRIVER = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)

class PersonnelQueueProducer(multiprocessing.Process):
    def __init__(self, personnel_queue, thread_id = 1, delay = DELAY):
        multiprocessing.Process.__init__(self)
        self.id = thread_id
        self.driver = DRIVER

        self.personnel_queue = personnel_queue
        self.delay = delay

    def run(self):
        print("Running")
        # personnel = None
        # while True:
        #     try:
        #         personnels = WebDriverWait(driver, self.delay).until(EC.presence_of_all_elements_located((By.NAME, "personnel")))

        #         for personnel in personnels:
        #             personnel_ids = personnel.get_attribute('value')
        #             for personnel_id in personnel_ids:
        #                 self.queue.put(personnel_id)

        #         break

        #     except TimeoutException:
        #         self.delay += 10
        #         print(f"Increasing timeout window to {self.delay} seconds")

# def main():
#     driver.get(URL)

#     personnels = None
#     while True:
#         try:
#             new_personnels = WebDriverWait(driver, DELAY).until(EC.presence_of_all_elements_located((By.NAME, "personnel")))
#             break
#         except TimeoutException:
#             print("Increasing timeout window")
#             DELAY += 10

#     while True:
#         try:
#             loadmore = WebDriverWait(driver, DELAY).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".btn.btn-success.btn-lg.btn-block.text-capitalize")))
#             driver.execute_script("arguments[0].scrollIntoView();", loadmore)
#             loadmore.click()
#             time.sleep(100)
#         except TimeoutException:
#             DELAY+=10
#         except:
#             break
            

#     print("Page is ready!")
#     #print(myElem)
#     for personnel in personnels:
#         print(personnel.get_attribute('value'))
#         print(personnel.get_attribute('innerHTML'))
#         print()


#     # driver.find_element(By.CSS_SELECTOR, ".btn.btn-success.btn-lg.btn-block.text-capitalize").click()


#     print("Clicked")

if __name__ == "__main__":
    personnel_queue = multiprocessing.Queue()
    
    personnel_queue_producer = PersonnelQueueProducer(personnel_queue)
    personnel_queue_producer.start()
    personnel_queue_producer.join()
    # main()

    

