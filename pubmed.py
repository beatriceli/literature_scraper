import csv
import os
from Bio import Entrez, Medline
from dotenv import load_dotenv

load_dotenv()

def search_pubmed(query, start_date=None, end_date=None):
    # Provide your email to NCBI Entrez
    Entrez.email = "blx2wj@virginia.edu"
    
    # Add date range to the query if provided
    if start_date and end_date:
        query += f" AND ({start_date}[dp] : {end_date}[dp])"
    
    print(f"Search query: {query}")
    
    # Perform the search on PubMed to get the total number of results
    search_handle = Entrez.esearch(db="pubmed", term=query, retmax=0)
    search_results = Entrez.read(search_handle)
    search_handle.close()
    
    total_results = int(search_results["Count"])
    print(f"Total number of search results: {total_results}")
    
    if total_results == 0:
        return []
    
    # Fetch all the results
    id_list = []
    batch_size = 1000
    for start in range(0, total_results, batch_size):
        end = min(total_results, start + batch_size)
        search_handle = Entrez.esearch(db="pubmed", term=query, retstart=start, retmax=batch_size)
        search_results = Entrez.read(search_handle)
        search_handle.close()
        id_list.extend(search_results["IdList"])
    
    print(f"Total number of IDs fetched: {len(id_list)}")
    
    # Fetch the details for each PMID
    fetch_handle = Entrez.efetch(db="pubmed", id=id_list, rettype="medline", retmode="text")
    fetch_results = Medline.parse(fetch_handle)
    
    return list(fetch_results)

def parse_pubmed_results(fetch_results):
    results = []
    for record in fetch_results:
        results.append({
            'Title': record.get('TI', 'N/A'),
            'Abstract': record.get('AB', 'N/A'),
            'Authors': ', '.join(record.get('AU', [])),
            'Publication Type': ', '.join(record.get('PT', ['N/A'])),
            'SourceTitle': record.get('JT', 'N/A'),
            'Publication Year': record.get('DP', 'N/A').split()[0] if 'DP' in record else 'N/A',
            'Keywords': ', '.join(record.get('OT', [])),
            'PMID': record.get('PMID', 'N/A'),
            'DOI': record.get('LID', 'N/A').split()[0] if 'LID' in record else 'N/A',
            'URL': f"https://pubmed.ncbi.nlm.nih.gov/{record.get('PMID', 'N/A')}"
        })
    
    return results

def export_to_csv(results, filename):
    # Define the CSV headers
    headers = ['Title', 'Abstract', 'Authors', 'Publication Type', 'SourceTitle', 'Publication Year', 'Keywords', 'PMID', 'URL', 'DOI']

    # Write the results to a CSV file
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

if __name__ == "__main__":
    query = os.getenv("PUBMED_QUERY")

    if query is None:
        query = input("Enter your query: ")
    
    start_date = input("Enter the start date (YYYY/MM/DD) or press Enter to skip: ")
    end_date = input("Enter the end date (YYYY/MM/DD) or press Enter to skip: ")
    
    start_date = start_date if start_date else None
    end_date = end_date if end_date else None

    fetch_results = search_pubmed(query, start_date, end_date)
    # print(fetch_results)

    if not fetch_results:
        print("No results found.")
    else:
        results = parse_pubmed_results(fetch_results)
        
        # Specify the filename in the current directory, include date range if providedm, MMYY_MMYY
        filename = f"lit_pubmed_{start_date.replace('/', '')}_{end_date.replace('/', '')}.csv" if start_date and end_date else "lit_pubmed.csv"

        # write to directory of literature, check if directory exists
        if not os.path.exists("literature"):
            os.makedirs("literature")
        filename = os.path.join("literature", filename)
        export_to_csv(results, filename)
