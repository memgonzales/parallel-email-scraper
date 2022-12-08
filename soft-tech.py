import multiprocessing
import time
import threading
import tracemalloc

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
# Set the delay to 60 seconds (1 minute).
DELAY = 50
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
    def __init__(self, personnel_queue, department_queue,url_queue,counters,thread_id = 1, delay = DELAY,mode = 1):
        multiprocessing.Process.__init__(self)
        self.id = thread_id
        self.personnel_queue = personnel_queue
        self.delay = delay
        self.pages_scraped = 0
        self.mode = mode
        self.department_queue = department_queue
        self.url_queue = url_queue
        self.notTerminated = counters[0]
        self.url_ctr = counters[1]
        self.email_ctr = counters[2]


    def run(self):
        print(f'Producer {self.id} starting')
        driver = DRIVER
        link = URL
        while self.notTerminated.value:
            if self.mode == 1:
                try:
                    dept = self.department_queue.get(timeout = 3)
                except Exception:
                    break
                link = dept_URL+dept
            personnels = None
            while self.notTerminated.value:
                try:
                    driver.get(link)
                    self.url_queue.put(link)
                    self.url_ctr.value+=1
                    curr =0
                    while self.notTerminated.value:
                        if self.mode == 3:
                            try:
                                personnels = WebDriverWait(driver, self.delay).until(EC.presence_of_all_elements_located((By.NAME, "personnel")))
                                try:
                                    loadmore = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".btn.btn-success.btn-lg.btn-block.text-capitalize")))
                                    driver.execute_script("arguments[0].scrollIntoView();", loadmore)
                                    loadmore.click()
                                except:
                                    break
                                
                                for personnel in personnels[curr:]:
                                    personnel_id = personnel.get_attribute('value')
                                    self.personnel_queue.put(personnel_id)
                                curr = len(personnels)
                            except Exception:
                                pass
                        else:
                            try:
                                loadmore = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".btn.btn-success.btn-lg.btn-block.text-capitalize")))
                                driver.execute_script("arguments[0].scrollIntoView();", loadmore)
                                loadmore.click()
                                if self.notTerminated.value != 1 and self.mode == 2:
                                    break
                            except:
                                break
                    if self.mode == 3:
                        break
                    if self.notTerminated.value==0:
                        self.personnel_queue.put(None)
                        for item in iter(self.personnel_queue.get, None):
                            a = 1
                        break
                    personnels = WebDriverWait(driver, self.delay).until(EC.presence_of_all_elements_located((By.NAME, "personnel")))
                    if self.notTerminated.value==0:
                        break
                    for personnel in personnels:
                        personnel_id = personnel.get_attribute('value')
                        self.personnel_queue.put(personnel_id)
                    self.pages_scraped = len(personnels)
                    break
                except TimeoutException:
                    self.delay += 1
                    print(f"Increasing timeout window to {self.delay} seconds")
            if self.mode != 1:
                break
        self.personnel_queue.close()

class PersonnelQueueConsumer(multiprocessing.Process):
    def __init__(self, personnel_queue,writing_queue, url_queue,counters,thread_id = 1, delay = DELAY):
        multiprocessing.Process.__init__(self)
        self.id = thread_id
        self.personnel_queue = personnel_queue
        self.writing_queue = writing_queue
        self.delay = delay
        self.url_queue = url_queue
        self.notTerminated = counters[0]
        self.url_ctr = counters[1]
        self.email_ctr = counters[2]

    def run(self):
        print(f'Consumer {self.id} starting')
        driver = DRIVER
        self.delay = 15
        while self.notTerminated.value:
            try:
                personnel_id = self.personnel_queue.get(timeout = 3)
            except:
                continue
            try:
                affiliation = ["",""]
                ctr = 0
                found = 1
                while self.notTerminated.value:
                    try:
                        driver.get(staff_URL+personnel_id)
                        if self.notTerminated.value == 0:
                            break
                        self.url_queue.put(staff_URL+personnel_id)
                        self.url_ctr.value+=1
                        pos = WebDriverWait(driver, self.delay).until(EC.visibility_of_element_located((By.CLASS_NAME, dept_position)))
                        if self.notTerminated.value == 0:
                            break
                        name = WebDriverWait(driver, self.delay).until(EC.visibility_of_element_located((By.TAG_NAME, 'h3')))
                        try:
                            email = driver.find_element(By.CSS_SELECTOR,email_class)
                            if "mailto" not in email.get_attribute('href'):
                                found = 0
                                break
                        except:
                            print(f'No email for {name.get_attribute("innerHTML")}')
                            found = 0
                            break
                        if self.notTerminated.value == 0:
                            break
                        items = pos.find_elements(By.TAG_NAME,'li')
                        break
                    except Exception:
                        pass
                if found:
                    if self.notTerminated.value == 0:
                        break
                    for item in items:
                        if "span" in item.get_attribute('innerHTML'):
                            affiliation[ctr]+=item.get_attribute('innerHTML')[6:-7]
                            ctr+=1
                    personnel_email = email.get_attribute('href')[7:]
                    personnel_name = name.get_attribute('innerHTML')
                    values = [personnel_email,personnel_name,affiliation]
                    self.writing_queue.put(values)
            except Exception:
                pass
        self.personnel_queue.close()

class WriterThread(multiprocessing.Process):
    def __init__(self, personnel_queue,writing_queue, url_queue,counters,thread_id = 1, delay = DELAY):
        multiprocessing.Process.__init__(self)
        self.id = thread_id
        self.personnel_queue = personnel_queue
        self.writing_queue = writing_queue
        self.delay = delay
        self.url_queue = url_queue
        self.notTerminated = counters[0]
        self.url_ctr = counters[1]
        self.email_ctr = counters[2]

    def run(self):
        print(f'Writer {self.id} starting')
        with open("Scraped_Emails.csv", "w",1) as file:
            while self.notTerminated.value:
                try:
                    values = self.writing_queue.get(timeout = 3)
                except:
                    continue
                output= f'{values[0]},{values[1]},{values[2][1]}\n'
                print("Personnel: ",output)
                file.write(output)
                self.email_ctr.value+=1
        with open("Website_Statistics.txt","w",1) as file:
            file.write(f'URLs Scraped: {self.url_ctr.value}\n')
            file.write(f'Emails Found: {self.email_ctr.value}\n')
            file.write("URLs Found:\n")
            for i in range(self.url_ctr.value):
                file.write(self.url_queue.get()+"\n")
        print("Writing Complete")
        DRIVER.quit()

class TimerThread(multiprocessing.Process):
    def __init__(self, duration,terminate):
        multiprocessing.Process.__init__(self)
        self.duration = duration
        self.terminated = terminate
    def run(self):
        time.sleep(self.duration/2)
        self.terminated.value = 0.5
        time.sleep(self.duration/2)
        self.terminated.value = 0
        print("Scraping duration ended!")

def program_start():
    print("Welcome to the DLSU Faculty Email Web Scraper!")
    print("Press Enter to have a certain parameter set to its default")
    print("Note: Default Scraping mode is 1")
    mode = input("Enter Scraping mode(1-3): ")
    duration = int(input("Enter Scraping duration in minutes: "))
    threads = int(input("Enter number of threads: "))
    duration = int(duration*60)
    if len(mode) == 0:
        mode = 1
    if threads == 1:
        return mode, duration,1,0
    if mode == 1:
        num_producers = int(input("Enter the number of producers: "))
        num_consumers = int(input("Enter the number of consumers: "))
    else:
        num_producers = 1
        num_consumers = threads-2
    
    return mode,duration,num_producers,num_consumers
            
if __name__ == "__main__":
    manager = multiprocessing.Manager()
    terminate = manager.Value('i',1)
    email_ctr = manager.Value('i',0)
    url_ctr = manager.Value('i',0)
    consumers = []
    producers = []
    personnel_queue = multiprocessing.Queue()
    writing_queue = multiprocessing.Queue()
    url_queue = multiprocessing.Queue()
    mode,duration,num_producers,num_consumers = program_start()
    timer_thread = TimerThread(duration,terminate)
    timer_thread.start()
    if mode == 1:
        for department in departments:
            department_queue.put(department)
    counters = [terminate,url_ctr,email_ctr]
    writer_thread = WriterThread(personnel_queue,writing_queue,url_queue,counters)
    writer_thread.start()
    if num_consumers !=0:
        for i in range(num_producers):
            personnel_queue_producer = PersonnelQueueProducer(personnel_queue,department_queue,url_queue,counters,thread_id=i,mode = mode)
            producers.append(personnel_queue_producer)
            personnel_queue_producer.start()
        for i in range(num_consumers):
            personnel_queue_consumer = PersonnelQueueConsumer(personnel_queue,writing_queue,url_queue,counters,thread_id=i)
            consumers.append(personnel_queue_consumer)
            personnel_queue_consumer.start()    
    else:
        personnel_queue_producer = PersonnelQueueProducer(personnel_queue,department_queue,url_queue,counters,mode = mode)
        producers.append(personnel_queue_producer)
        personnel_queue_producer.start()
        personnel_queue_producer.join()
        personnel_queue_consumer = PersonnelQueueConsumer(personnel_queue,writing_queue,url_queue,counters)
        consumers.append(personnel_queue_consumer)
        personnel_queue_consumer.start()    
        personnel_queue_consumer.join()
        
    for producer in producers:
        producer.join()
    for consumer in consumers:
        consumer.join()
    writer_thread.join()
    timer_thread.join()
    print("FINISHED")