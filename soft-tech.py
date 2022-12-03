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
staff_URL = "https://www.dlsu.edu.ph/staff-directory/?personnel="
email_class = '.btn.btn-sm.btn-block.text-capitalize'
dept_position = 'list-unstyled.text-capitalize.text-center'
name_class = '.col-lg-12.col-md-12.col-sm-12 col-xs-12'

# Set the delay to 300 seconds (5 minutes).
DELAY = 100

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
DRIVER = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)

class PersonnelQueueProducer(multiprocessing.Process):
    global DRIVER
    def __init__(self, personnel_queue, thread_id = 1, delay = DELAY):
        multiprocessing.Process.__init__(self)
        self.id = thread_id
        self.personnel_queue = personnel_queue
        self.delay = delay

        print("Hellooo")
    def run(self):
        print("Running")
        driver = DRIVER
        personnel = None
        while True:
            try:
                driver.get(URL)
                personnels = WebDriverWait(driver, self.delay).until(EC.presence_of_all_elements_located((By.NAME, "personnel")))
                for personnel in personnels:
                    personnel_id = personnel.get_attribute('value')
                    self.personnel_queue.put(personnel_id)
                break
            except TimeoutException:
                self.delay += 1
                print(f"Increasing timeout window to {self.delay} seconds")

class PersonnelQueueConsumer(multiprocessing.Process):
    global DRIVER
    def __init__(self, personnel_queue,writing_queue, thread_id = 1, delay = DELAY):
        multiprocessing.Process.__init__(self)
        self.id = thread_id
        self.personnel_queue = personnel_queue
        self.writing_queue = writing_queue
        self.delay = delay

    def run(self):
        driver = DRIVER
        personnel_id = self.personnel_queue.get()
        print(staff_URL+personnel_id)
        try:
            affiliation = ["",""]
            ctr = 0
            found = 1
            while True:
                try:
                    driver.get(staff_URL+personnel_id)
                    pos = WebDriverWait(driver, self.delay).until(EC.visibility_of_element_located((By.CLASS_NAME, dept_position)))
                    name = WebDriverWait(driver, self.delay).until(EC.visibility_of_element_located((By.TAG_NAME, 'h3')))
                    try:
                        email = driver.find_element(By.CSS_SELECTOR,email_class)
                    except:
                        print("No email")
                        found = 0
                        break
                    items = pos.find_elements(By.TAG_NAME,'li')
                    break
                except Exception:
                    print("ERROR")
                    print(Exception)
            if found:
                for item in items:
                    if "span" in item.get_attribute('innerHTML'):
                        affiliation[ctr]+=item.get_attribute('innerHTML')[6:-7]
                        ctr+=1
                print("Page is ready!")
                personnel_email = email.get_attribute('href')[7:]
                personnel_name = name.get_attribute('innerHTML')
                values = [personnel_email,personnel_name,affiliation]
                self.writing_queue.put(values)
        except TimeoutException:
            print("Loading took too much time!")

class WriterThread(multiprocessing.Process):
    global DRIVER
    def __init__(self, personnel_queue,writing_queue, thread_id = 1, delay = DELAY):
        multiprocessing.Process.__init__(self)
        self.id = thread_id
        self.personnel_queue = personnel_queue
        self.writing_queue = writing_queue
        self.delay = delay

    def run(self):
        print("Writing")
        with open("Scraped_Emails.txt", "a") as file:
            while True:
                values = self.writing_queue.get()
                output= f'{values[0]} : {values[1]} {values[2][1]} {values[2][0]}\n'
                print(output)
                file.write(output)
                print("Writing complete!")

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
    num_threads = 3
    consumers = []
    personnel_queue = multiprocessing.Queue()
    writing_queue = multiprocessing.Queue()
    personnel_queue_producer = PersonnelQueueProducer(personnel_queue)
    personnel_queue_producer.start()
    for i in range(num_threads):
        personnel_queue_consumer = PersonnelQueueConsumer(personnel_queue,writing_queue)
        consumers.append(personnel_queue_consumer)
        personnel_queue_consumer.start()    
    writer_thread = WriterThread(personnel_queue,writing_queue)
    writer_thread.start()
    personnel_queue_producer.join()
    for consumer in consumers:
        consumer.join()
    writer_thread.join()
    # main()

    

