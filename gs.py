import csv
from scholarly import scholarly

def search_google_scholar(query, num_results=10):
    # Perform the search on Google Scholar
    search_query = scholarly.search_pubs(query)
    
    # Collect the results
    results = []
    for i in range(num_results):
        try:
            result = next(search_query)
            results.append(result)
        except StopIteration:
            break

    return results

def export_to_csv(results, filename):
    # Define the CSV headers
    headers = ['Title', 'Authors', 'Abstract', 'URL', 'Citations', 'Year']

    # Write the results to a CSV file
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for result in results:
            writer.writerow({
                'Title': result.get('bib', {}).get('title', 'N/A'),
                'Authors': ', '.join(result.get('bib', {}).get('author', [])),
                'Abstract': result.get('bib', {}).get('abstract', 'N/A'),
                'URL': result.get('eprint_url', 'N/A'),
                'Citations': result.get('num_citations', 'N/A'),
                'Year': result.get('bib', {}).get('pub_year', 'N/A')
            })

if __name__ == "__main__":
    query = input("Enter the search query: ")
    num_results = int(input("Enter the number of results to fetch: "))
    results = search_google_scholar(query, num_results)
    export_to_csv(results, 'scholar_results.csv')
    print(f"Results have been exported to scholar_results.csv")