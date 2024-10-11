import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def search_acm(query, start_date, end_date):
    url = 'https://dl.acm.org/action/doSearch'
    params = {
        'AllField': query,
        'AfterYear': start_date[:4],
        'AfterMonth': start_date[5:7],
        'AfterDay': start_date[8:10],
        'BeforeYear': end_date[:4],
        'BeforeMonth': end_date[5:7],
        'BeforeDay': end_date[8:10],
        'ContentItemType': 'research-article',
        'pageSize': 50,
        'startPage': 0
    }

    results = []
    while True:
        response = requests.get(url, params=params)
        response.raise_for_status()
        html = response.text

        new_results, has_next_page = parse_results(html)
        results.extend(new_results)

        if not has_next_page:
            break
        
        params['startPage'] += 1
        time.sleep(1)  # Add a delay of 1 second between requests

    return results

def parse_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    for item in soup.find_all('div', class_='issue-item'):
        title_tag = item.find('span', class_='hlFld-Title')
        title = title_tag.text.strip() if title_tag else 'N/A'
        
        authors = []
        author_tags = item.find_all('span', class_='hlFld-ContribAuthor')
        for author in author_tags:
            authors.append(author.text.strip())
        
        journal_tag = item.find('span', class_='epub-section__title')
        journal = journal_tag.text.strip() if journal_tag else 'N/A'
        
        year_tag = item.find('span', class_='epub-section__date')
        year = year_tag.text.strip() if year_tag else 'N/A'

        link_tag = item.find('a', class_='issue-item__title')
        link = 'https://dl.acm.org' + link_tag['href'] if link_tag else 'N/A'

        results.append({
            'Title': title,
            'Authors': ', '.join(authors),
            'Journal': journal,
            'Year': year,
            'Link': link
        })

    # export results to a file
    with open('fetch_results.txt', 'w') as f:
        for item in results:
            f.write("%s\n" % item)
    next_page_tag = soup.find('a', class_='pagination__btn--next')
    has_next_page = bool(next_page_tag)
    
    return results, has_next_page

def save_to_csv(results, filename):
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)
    print(f'Results saved to {filename}')

if __name__ == '__main__':
    query = '(Ubiquitous OR Pervasive OR mobile OR Smart OR Digital OR Environmental) AND (Sensing OR Sensor) AND (health OR well-being*) AND (Indoor)'
    
    start_date = input('Enter start date (YYYY-MM-DD): ')
    end_date = input('Enter end date (YYYY-MM-DD): ')
    
    results = search_acm(query, start_date, end_date)
    # print results to a file
    with open('fetch_results.txt', 'w') as f:
        for item in results:
            f.write("%s\n" % item)
    filename = f'lit_acm_{start_date}_{end_date}.csv'
    save_to_csv(results, filename)
