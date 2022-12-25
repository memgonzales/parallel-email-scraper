# Multiprocesses Email Address Scraper

This project is a **multiprocess email address scraper** for the De La Salle University website staff directory. 

This is the major course output in an advanced operating systems class for master's students under Mr. Gregory G. Cu of the Department of Software Technology, College of Computer Studies. The task is to create an email address scraper that employs parallel programming techniques.

- **Complete Technical Paper:** [Technical Paper](https://github.com/memgonzales/parallel-email-scraper/blob/master/Technical%20Paper.pdf)
- **Video Demonstration:** https://www.youtube.com/watch?v=zYA5TIbF9UE

## Approach
Combining both functional and data decomposition, our proposed approach models the scraping task as a **multiple producer – multiple consumer problem**:
- The set of personnel IDs in the staff directory is divided by department, and multiple producers are mapped to different department directories. Each producer retrieves the personnel IDs from its assigned department directory and stores them in a synchronized queue. 
- Concurrently, the IDs are dequeued by consumer subprocesses, which use them to visit the staff members' individual web pages, scrape pertinent information (names, email addresses, and departments) from there, and store these details in another queue. 
- A dedicated subprocess gets the details from this queue and writes them on the output file.

Running our proposed approach with five threads achieves a 7.22&times; superlinear speedup compared to serial execution. Further experiments show that it achieves better scalability and performance than baseline parallel programming approaches that scrape from the root directory.

## Project Structure

## Running the Scraper
Install the necessary [dependencies](), and run the following command on the terminal:
```
python scraper.py
```

The following output files will be produced once the program is finished running:
- `Scraped_Emails.csv` - A text file containing the scraped details (names, email addresses, and departments)
- `Website_Statistics.txt` - A text file containing the number of pages scraped, the number of email addresses found, and the URLs scraped

## Dependencies


## Built Using

## Authors
- <b>Mark Edward M. Gonzales</b> <br/>
  mark_gonzales@dlsu.edu.ph <br/>
  gonzales.markedward@gmail.com <br/>
  
- <b>Hans Oswald A. Ibrahim</b> <br/>
  hans_oswald_ibrahim@dlsu.edu.ph <br/>
  hans.ibrahim2001@gmail.com
