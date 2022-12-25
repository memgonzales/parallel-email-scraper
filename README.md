# Multiprocesses Email Address Scraper

This project is a **multiprocess email address scraper** for the De La Salle University website staff directory. 

This is the major course output in an advanced operating systems class for master's students under Mr. Gregory G. Cu of the Department of Software Technology, College of Computer Studies. The task is to create an email address scraper that employs parallel programming techniques. The complete project specifications can be found in the document [`Project Specifications.pdf`](https://github.com/memgonzales/parallel-email-scraper/blob/master/Project%20Specifications.pdf).

- **Technical Paper:** [`Technical Paper.pdf`](https://github.com/memgonzales/parallel-email-scraper/blob/master/Technical%20Paper.pdf)
- **Video Demonstration:** https://www.youtube.com/watch?v=zYA5TIbF9UE

## Approach
Combining both functional and data decomposition, our proposed approach models the scraping task as a **multiple producer – multiple consumer problem**:
- The set of personnel IDs in the staff directory is divided by department, and multiple producers are mapped to different department directories. Each producer retrieves the personnel IDs from its assigned department directory and stores them in a synchronized queue. 
- Concurrently, the IDs are dequeued by consumer subprocesses, which use them to visit the staff members' individual web pages, scrape pertinent information (names, email addresses, and departments) from there, and store these details in another queue. 
- A dedicated subprocess gets the details from this queue and writes them on the output file.

Running our proposed approach with five threads achieves a **7.22&times; superlinear speedup** compared to serial execution. Further experiments show that it achieves better scalability and performance than baseline parallel programming approaches that scrape from the root directory.

<img src="https://github.com/memgonzales/parallel-email-scraper/blob/master/approach.png?raw=True" alt="App Screenshots" width = 500> 

## Running the Scraper
1. Create a copy of this repository:

    - If [git](https://git-scm.com/downloads) is installed, type the following command on the terminal:

        ```
        git clone https://github.com/memgonzales/parallel-email-scraper
        ```

    - If git is not installed, click the green `Code` button near the top right of the repository and choose [`Download ZIP`](https://github.com/memgonzales/parallel-email-scraper/archive/refs/heads/master.zip). Once the zipped folder has been downloaded, extract its contents.

2. Install [Google Chrome](https://www.google.com/chrome/?brand=BNSD&gclid=CjwKCAiAhqCdBhB0EiwAH8M_GvFEsHmcDe4zQm_t8izcLesJyq_GzCKoJp24grz8rve-lIxYYqmdxRoCX4oQAvD_BwE&gclsrc=aw.ds). It is recommended to retain the default installation directory.

3. Install the necessary [dependencies](https://github.com/memgonzales/parallel-email-scraper#built-using). All the dependencies can be installed via `pip`.

4. Run the following command on the terminal:
   ```
   python scraper.py
   ```

5. The following output files will be produced once the program is finished running:
   - `Scraped_Emails.csv` - A text file containing the scraped details (names, email addresses, and departments)
   - `Website_Statistics.txt` - A text file containing the number of pages scraped, the number of email addresses found, and the URLs scraped

   Sample [screenshots of the running program](https://github.com/memgonzales/parallel-email-scraper/tree/master/Sample%20Screenshots) and [output files](https://github.com/memgonzales/parallel-email-scraper/tree/master/Sample%20Output%20Files) are also provided in this repository.

## Built Using
This project was built using **Python 3.8**, with the following libraries and modules used:

Libraries/Modules | Description | License
--- | ---| ---
[Selenium 4.7.2](https://pypi.org/project/selenium/) | Provides functions for enabling web browser automation | Apache License 2.0
[Webdriver Manager 3.8.5](https://pypi.org/project/webdriver-manager/) | Simplifies management of binary drivers for different browsers | Apache License 2.0
[`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html) | Offers both local and remote concurrency, effectively side-stepping the Global Interpreter Lock | Python Software Foundation License
[`time`](https://docs.python.org/3/library/time.html) | Provides various time-related functions | Python Software Foundation License

*The descriptions are taken from their respective websites.*

## Authors
- <b>Mark Edward M. Gonzales</b> <br/>
  mark_gonzales@dlsu.edu.ph <br/>
  gonzales.markedward@gmail.com <br/>
  
- <b>Hans Oswald A. Ibrahim</b> <br/>
  hans_oswald_ibrahim@dlsu.edu.ph <br/>
  hans.ibrahim2001@gmail.com
