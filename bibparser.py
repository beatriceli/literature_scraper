import bibtexparser
import os
import csv

# go into the literature/acm_parts folder and parse the bibtex file
os.chdir('literature')
bibfile = input("Enter the name of the bibtex file: ")

# open the bibtex file
library = bibtexparser.load(open(bibfile))
print(f"Found {len(library.entries)} entries")

# create a CSV file with the same name as the bibtex file but with lit_ prefix
# add prefix to the filename
output_file = ('lit_' + bibfile).replace('.bib', '.csv')

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Title', 'Abstract', 'Authors', 'Publication Type', 'SourceTitle', 'Publication Year', 'Keywords','DOI'])
    for entry in library.entries:
        writer.writerow([
            entry['title'],
            entry['abstract'] if 'abstract' in entry else '',
            entry['author'] if 'author' in entry else '',
            entry['ENTRYTYPE'] if 'ENTRYTYPE' in entry else '',
            entry['journal'] if 'journal' in entry else entry['booktitle'] if 'booktitle' in entry else '',
            entry['year'],
            entry['keywords'] if 'keywords' in entry else '',
            entry['doi'] if 'doi' in entry else entry['ID']
        ])