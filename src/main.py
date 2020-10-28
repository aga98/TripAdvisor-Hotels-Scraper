from scraper import scrape
from hotels_to_csv import hotels_to_csv
import time


if __name__ == "__main__":
    start = time.time()
    hotels = scrape()
    hotels_to_csv(hotels)
    end = time.time()
    print("Elapsed time:", end - start)
