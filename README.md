# literature_review
Toolset to retrieve search results from ACM Digital Library, PubMed and Web of Science

This project provides Python scripts to automate the retrieval of research articles and bibliographic parsing from different sources. The scripts included are:

- `wos.py`: For querying and retrieving research articles from the Web of Science (WoS) database.
- `pubmed.py`: For querying and retrieving research articles from the PubMed database.
- `bibparser.py`: For parsing bibliographic data from ACM Digital Library exports.


## wos.py
This script queries the Web of Science (WoS) database and retrieves research articles based on a provided search query and optional date range.
An api key is needed for access but a free version is available for application, found here: https://developer.clarivate.com/apis/wos-starter.
The specific database within Web of Science can be indicated, i.e. 'WOS': Web of Science Core Collection, 'WOK': represents all databases.

#### Usage:
```sh
python wos.py
```

#### Parameters:
* 'query': The search query string.
* 'start_date': The start date for the search range (YYYY-MM-DD).
* 'end_date': The end date for the search range (YYYY-MM-DD).
* 'count': The number of results to fetch (optional, default and maximum is 100).
* 'first_record': Specific record, if any, within the result set to return. Cannot be less than 1 and greater than 100000.

#### Example
```sh
Enter the start date (YYYY-MM-DD) or press Enter to skip: 2021-01-01
Enter the end date (YYYY-MM-DD) or press Enter to skip: 2021-06-30
```

The results will be exported to a CSV file named lit_{Database}_{start_date}_{end_date}.csv in a literature directory.

#### Additional WOS Starter/Lite API information can be found here:
- [Swagger UI](https://api.clarivate.com/swagger-ui/?apikey=none&url=https%3A%2F%2Fdeveloper.clarivate.com%2Fapis%2Fwoslite%2Fswagger)
- [API Documentation](https://api.clarivate.com/swagger-ui/?apikey=f1cab570b679ce889a915d389e5cb12c2bdb6962&url=https%3A%2F%2Fdeveloper.clarivate.com%2Fapis%2Fwos-starter%2Fswagger%3FforUser%3D350b7776826fdd8e4c2d2ecd2cefb91dd5e04df4)
- [Advanced Examples](https://images.webofknowledge.com//WOKRS529AR7/help/WOS/hp_advanced_examples.html)


## pubmed.py
This script queries the PubMed database and retrieves research articles based on a provided search query and a date range.

Usage
```sh
python pubmed.py
```

The results will be exported to a CSV file named lit_pubmed_{start_date}_{end_date}.csv in a literature directory.

## bibparser.py
This script parses bibliographic data from ACM Digital Library exports. ACM does not have any official API and it is difficult to access otherwise. You can conduct the search on the official website and select all to export all results, which has a maximum of 1000. If results exceed 1000, it is best to break the exports into parts. 

You can use [bibtex-tools](https://pypi.org/project/bibtextools/#:~:text=isbn%20literature.bib-,Combining%20Bib%20Files,occur%20after%20merging%20the%20files) to combine multiple bib files into one. 

The results will be exported to a CSV file named lit_acm_{start_date}_{end_date}.csv in a literature directory.