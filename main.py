from job_scraper import scrape_linkedin_jobs, save_to_csv
from config import KEYWORDS, LOCATIONS, OUTPUT_FILE

def main():
    print("Scraping LinkedIn jobs...")
    jobs = scrape_linkedin_jobs(KEYWORDS, LOCATIONS)
    save_to_csv(jobs, OUTPUT_FILE)

if __name__ == "__main__":
    main()