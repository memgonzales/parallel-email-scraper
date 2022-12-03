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
dept = "IT"
URL = f'https://www.dlsu.edu.ph/staff-directory/'
staff_URL = "https://www.dlsu.edu.ph/staff-directory/?personnel="
email_class = '.btn.btn-sm.btn-block.text-capitalize'
dept_position = 'list-unstyled.text-capitalize.text-center'
name_class = '.col-lg-12.col-md-12.col-sm-12 col-xs-12'
dept_URL = "https://www.dlsu.edu.ph/staff-directory/?search&filter=department&category="
# Set the delay to 300 seconds (5 minutes).
DELAY = 60

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
DRIVER = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)
departments = ['IT', 'CT', 'ST', 'CEPD', 'ELMD', 'DEAL', 'PE', 'SED', 'ACCTY', 'COMLAW', 'DSI', 'FMD', 'MOD', 'ADVERT', 'BSD', 'COMM', 'FIL', 'HIST', 'IS', 'LIT', 
'PHILO', 'POLSCI', 'PSYC', 'TRED', 'BIO', 'CHEM', 'PHY', 'MATH', 'SOE', 'CHE', 'CE', 'ECE', 'ME', 'IE', 'MEM', 'COL', 'ASIST', 'ADRIC', 'AAA', 'AKI', 'AKIEBS', 
'AMO', 'AVCAS', 'AVCCD', 'AVCCS', 'AVCFM', 'AVPCD', 'AVPES', 'AVPFM', 'BNSCWRC', 'SHORE', 'BGM', 'CSO', 'CBRD', 'CESDR', 'CELL', 'CENSER', 'CPDB', 'COSCA', 'CEC', 
'CAO', 'DITO', 'DIPO', 'DLSUPH', 'ELMD', 'ESH', 'ERIO', 'ERI', 'FACILITIES', 'FA', 'ITS', 'ITEO', 'JMRIG', 'LSPO', 'MEWO', 'NFO', 'OASIS', 'OAS', 'OCCS', 'OPM', 'OSD', 
'CHANCELLOR', 'OP', 'OUR', 'PHYLAB', 'PROCUREMENT', 'QAO', 'ROTC', 'RMCA', 'SED', 'SECURITY', 'SDRC', 'STRATCOM', 'SDFO', 'SLIFE', 'SM', 'MUSEUM', 'LIBRARY', 'URCO', 
'UREO', 'SAFETY', 'VCA', 'VCRI', 'VPLM']
department_queue = multiprocessing.Queue()
#Get Departments
# while True:
#     try:
#         DRIVER.get(dept_URL+dept)
#         option_box = WebDriverWait(DRIVER,DELAY).until(EC.visibility_of_element_located((By.ID,"select-department")))
#         departments = option_box.find_elements(By.TAG_NAME,"option")
#         break
#     except:
#         print("Reload Departments")
# for department in departments:
#     valid = department.get_attribute('innerHTML')
#     value = department.get_attribute('value')
#     if valid[0] == ' ':
#         continue
#     dpts.append(value)
#     department_queue.put(value)
class PersonnelQueueProducer(multiprocessing.Process):
    global DRIVER
    def __init__(self, personnel_queue, department_queue,thread_id = 1, delay = DELAY,mode = 1):
        multiprocessing.Process.__init__(self)
        self.id = thread_id
        self.personnel_queue = personnel_queue
        self.delay = delay
        self.pages_scraped = 0
        self.mode = mode
        self.department_queue = department_queue

    def run(self):
        print("Producing")
        driver = DRIVER
        link = URL
        while True:
            if self.mode == 2:
                dept = self.department_queue.get()
                link = dept_URL+dept
                print(link)
            personnel = None
            while True:
                try:
                    driver.get(link)
                    while True:
                        try:
                            loadmore = WebDriverWait(driver, DELAY).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".btn.btn-success.btn-lg.btn-block.text-capitalize")))
                            driver.execute_script("arguments[0].scrollIntoView();", loadmore)
                            loadmore.click()
                        except:
                            print("ERROR load")
                            break
                    try:
                        loadmore = WebDriverWait(driver, DELAY).until(EC.visibility_of_element_located((By.CSS_SELECTOR,".btn.btn-success.btn-lg.btn-block.text-capitalize")))
                    except:
                        print("No load more")
                    personnels = WebDriverWait(driver, self.delay).until(EC.presence_of_all_elements_located((By.NAME, "personnel")))
                    for personnel in personnels:
                        personnel_id = personnel.get_attribute('value')
                        self.personnel_queue.put(personnel_id)
                    self.pages_scraped = len(personnels)
                    break
                except TimeoutException:
                    self.delay += 1
                    print(f"Increasing timeout window to {self.delay} seconds")
            if self.mode == 1:
                break

class PersonnelQueueConsumer(multiprocessing.Process):
    global DRIVER
    def __init__(self, personnel_queue,writing_queue, thread_id = 1, delay = DELAY):
        multiprocessing.Process.__init__(self)
        self.id = thread_id
        self.personnel_queue = personnel_queue
        self.writing_queue = writing_queue
        self.delay = delay

    def run(self):
        print("Consuming")
        driver = DRIVER
        while True:
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
        with open("Scraped_Emails.txt", "a",1) as file:
            while True:
                values = self.writing_queue.get()
                output= f'{values[0]} : {values[1]} {values[2][1]} {values[2][0]}\n'
                print(output)
                file.write(output)
                print("Writing complete!")


if __name__ == "__main__":
    num_consumers = 4
    num_producers = 2
    mode = 2
    if mode == 2:
        for department in departments:
            department_queue.put(department)
        print("Got departments")
    consumers = []
    producers = []
    personnel_queue = multiprocessing.Queue()
    writing_queue = multiprocessing.Queue()
    for i in range(num_producers):
        personnel_queue_producer = PersonnelQueueProducer(personnel_queue,department_queue,mode = mode)
        producers.append(personnel_queue_producer)
        personnel_queue_producer.start()
    for i in range(num_consumers):
        personnel_queue_consumer = PersonnelQueueConsumer(personnel_queue,writing_queue)
        consumers.append(personnel_queue_consumer)
        personnel_queue_consumer.start()    
    writer_thread = WriterThread(personnel_queue,writing_queue)
    writer_thread.start()
    for producer in producers:
        producer.join()
    for consumer in consumers:
        consumer.join()
    
    writer_thread.join()
    # main()