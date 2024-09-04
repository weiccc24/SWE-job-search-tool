import requests # For making HTTP requests
from bs4 import BeautifulSoup # For parsing HTML
import pandas as pd # For data manipulation and CSV creation
from datetime import datetime, timedelta # For date handling
from config import LINKEDIN_URL, HEADERS
import re # For regular expressions
import time # For adding delays

def scrape_linkedin_jobs(keywords, location):
    url = LINKEDIN_URL.format('+'.join(keywords), location)

    # Make an HTTP GET request to the URL with error handling
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"An error has occurred: {e}")
        return []
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all job cards on the page
    jobs = []
    job_cards = soup.find_all('div', class_='base-card')

    print(f"Found {len(job_cards)} job cards")
    
    # Iterate through each job card: extract job title, company, location, link and date
    for i, card in enumerate(job_cards, 1):
        title = card.find('h3', class_='base-search-card__title')
        company = card.find('h4', class_='base-search-card__subtitle')
        location = card.find('span', class_='job-search-card__location')
        link = card.find('a', class_='base-card__full-link')
        
        # Date extraction using 'parse_date' function
        date_element = card.find('time', class_='job-search-card__listdate')
        
        if title and company and location and link and date_element:
            date_str = date_element.get('datetime') or date_element.text.strip()
            post_date = parse_date(date_str)

            if post_date and post_date >= datetime.now() - timedelta(days=7):
                jobs.append({
                    'Title': title.text.strip(),
                    'Company': company.text.strip(),
                    'Location': location.text.strip(),
                    'Link': link['href'] if link else 'N/A', # Check if link is not None
                    'Date Posted': post_date.strftime('%Y-%m-%d')
                })
        print(f"Processed job {i}/{len(job_cards)}")
        time.sleep(2) # Add a 2-second delay between processing each job
    return jobs

def parse_date(date_str):
    today = datetime.now()

    # Check for "X days/weeks/months ago" format
    if 'ago' in date_str.lower():
        number = int(re.search(r'\d+', date_str).group())
        if 'day' in date_str.lower():
            return today - timedelta(days=number)
        elif 'week' in date_str.lower():
            return today - timedelta(weeks=number)
        elif 'month' in date_str.lower():
            return today - timedelta(days=number*30) # Approximation
        elif 'hour' in date_str.lower() or 'minute' in date_str.lower():
            return today
    # Check for "Today" or "Just now"
    elif 'today' in date_str.lower() or 'just now' in date_str.lower():
        return today
    
    # Check for "Yesterday"
    elif 'yesterday' in date_str.lower():
        return today - timedelta(days=1)
    
    # Try parsing exact date formats
    else:
        # Try look for different date formats
        for fmt in ['%B %d, %Y', '%Y-%m-%d', '%d %b %Y']:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        # If all parsing attempts fail, return None
        return None



def save_to_csv(jobs, filename):
    df = pd.DataFrame(jobs)
    df.to_csv(filename, index=False)
    print(f"Saved {len(jobs)} jobs to {filename}")