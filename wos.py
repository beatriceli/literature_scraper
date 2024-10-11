import requests
import csv
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_wos_data(start_date, end_date, query, count=100, first_record=1, output_file='lit_wos.csv'):
    """
    Fetch data from the World of Science database and export it to a CSV file.
    
    Parameters:
    - start_date (str): The start date for the query in YYYY-MM-DD format.
    - end_date (str): The end date for the query in YYYY-MM-DD format.
    - query (str): The search query for the database. Default is 'TS=(machine learning)'.
    - count (int): The number of records to fetch. Default is 100.
    - first_record (int): The first record to start fetching from. Default is 1.
    - output_file (str): The name of the output CSV file. Default is 'wos_results.csv'.
    """
    
    # API endpoint and API key
    endpoint = 'https://api.clarivate.com/api/woslite/'
    api_key = os.getenv('WOS_API_KEY')

    if api_key is None:
        api_key = input("Enter your WOS API key: ")

    # Headers for the API request
    headers = {
        'X-ApiKey': api_key,
        'Content-Type': 'application/json'
    }
    
    db = 'WOK'
    # store all records before writing to CSV
    all_records = []

    while True:
        # Parameters for the API request
        params = {
            'databaseId': db,
            'usrQuery': query,
            'count': count,
            'firstRecord': first_record,
            'publishTimeSpan': f'{start_date}+{end_date}'
        }

        # Make the API request
        response = requests.get(endpoint, headers=headers, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            # store the records
            all_records.extend(data['Data'])

            # check if there is a next page
            next_page_url = response.headers.get('x-paginate-by-query-id')
            if next_page_url:
                print("Fetching next page...")
                # extract first record from the next page url
                first_record = int(next_page_url.split('firstRecord=')[1].split('&')[0])
                print(f"Total records:{data['QueryResult']['RecordsFound']}; First record: {first_record}")
                response = requests.get(next_page_url, headers=headers)
            else:
                break
        else:
            print(f"Error: Unable to fetch data. HTTP Status code: {response.status_code}")
    
    # Write the data to a CSV file
    export_to_csv(all_records, db, start_date, end_date, output_file)


def export_to_csv(data, db, start_date, end_date, output_file):
    """
    Write data to a CSV file.
    
    Parameters:
    - data (dict): The data fetched from the API.
    - start_date (str): The start date for the query in YYYY-MM-DD format.
    - end_date (str): The end date for the query in YYYY-MM-DD format.
    - output_file (str): The name of the output CSV file.
    """
    # Specify the filename in the current directory, include date range if provided, MMYY_MMYY
    filename = f"lit_{db}_{start_date}_{end_date}.csv" if start_date and end_date else output_file

    # Write to the directory of literature, check if directory exists
    if not os.path.exists("literature"):
        os.makedirs("literature")
    filename = os.path.join("literature", filename)

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write the headers
        headers = ['Title', 'Authors', 'Publication Type', 'SourceTitle', 'Publication Year', 'Keywords', 'UT', 'DOI', 'ISSN']
        csvwriter.writerow(headers)
        # traverse the data to get the records
        for item in data:
            title = item['Title']['Title'][0]
            authors = '; '.join(item['Author'].get('Authors', []))
            doctype = item['Doctype'].get('Doctype',[None])[0]
            source_title = item['Source'].get('SourceTitle', [None])[0]
            year = item['Source'].get('Published.BiblioYear', [None])[0]
            keywords = ', '.join(item['Keyword'].get('Keywords', []))
            doi = item['Other'].get('Identifier.Doi', [None])[0]
            issn = item['Other'].get('Identifier.Issn', [None])[0]
            ut = item['UT'].split(':')[0]
            csvwriter.writerow([title, authors, doctype, source_title, year, keywords, ut, doi, issn])
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    query = os.getenv('WOS_QUERY')

    if query is None:
        query = input("Enter your WOS query: ")


    start_date = input("Enter the start date (YYYY-MM-DD) or press Enter to skip: ")
    end_date = input("Enter the end date (YYYY-MM-DD) or press Enter to skip: ")
    
    start_date = start_date if start_date else None
    end_date = end_date if end_date else None

    fetch_wos_data(start_date, end_date, query)
