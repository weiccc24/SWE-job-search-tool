import requests
from bs4 import BeautifulSoup
import pandas as pd
from config import LINKEDIN_URL, HEADERS

def scrape_linkedin_jobs(keywords, location):
    url = LINKEDIN_URL.format('+'.join(keywords), location)
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    jobs = []
    job_cards = soup.find_all('div', class_='base-card')
    
    for card in job_cards:
        title = card.find('h3', class_='base-search-card__title')
        company = card.find('h4', class_='base-search-card__subtitle')
        location = card.find('span', class_='job-search-card__location')
        link = card.find('a', class_='base-card__full-link')
        
        if title and company and location and link:
            jobs.append({
                'Title': title.text.strip(),
                'Company': company.text.strip(),
                'Location': location.text.strip(),
                'Link': link['href']
            })
    
    return jobs

def save_to_csv(jobs, filename):
    df = pd.DataFrame(jobs)
    df.to_csv(filename, index=False)
    print(f"Saved {len(jobs)} jobs to {filename}")