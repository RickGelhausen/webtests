import argparse
import bibtexparser
import re
from jinja2 import Template

template_string = '''
<div class="publication" data-author="{{ authors_data }}" data-journal="{{ journal }}" data-year="{{ year }}">
    <div class="title" name="{{ id }}">
        <a href="{{ href }}">{{ title }}</a>
    </div>
    <div class="authors">
        {{ authors }}
    </div>
    <div class="journal">
        {{ journal }}, {{ year }}
    </div>
    {%- if link %}
    <div class="link">
        <a href="{{ href }}">{{ link }}</a>
    </div>
    {%- endif %}
</div>
'''

template = Template(template_string)

def format_authors(authors):
    # Replace newlines with space and collapse multiple spaces into one
    authors = re.sub(r'\s+', ' ', authors)

    author_list = authors.split(' and ')
    authors_list = []
    for author in author_list:
        parts = [part.strip() for part in author.split(',')]
        last_name = parts[0]
        first_name = " ".join(parts[1:])  # first name includes all parts except the last
        authors_list.append(f'{first_name} {last_name}')

    if len(authors_list) > 1:
        last_author = authors_list.pop()
        authors_formatted = ', '.join(authors_list) + ' and ' + last_author
    else:
        authors_formatted = authors_list[0]

    authors_data = ";".join(authors_list)
    return authors_formatted, authors_data

def format_title(title):
    return re.sub(r'\{(.+?)\}', r'\1', title)

def create_html_page(bib_entries, output_file):
    html_string = ''

    # Sort entries by year (descending) and first author's name
    bib_entries.sort(key=lambda e: (-int(e.get('year', '0')), e.get('author', '').split(' and ')[0].split(',')[0]))

    for entry in bib_entries:
        id = entry.get('ID', '')
        authors, authors_data = format_authors(entry.get('author', ''))
        journal = entry.get('journal', '')
        year = entry.get('year', '')
        title = format_title(entry.get('title', '').replace("\n", ""))
        link = entry.get('doi', entry.get('url', ''))
        href = f"https://doi.org/{link}" if not link.startswith(('http', 'www')) else link

        html_string += template.render(id=id, authors_data=authors_data, authors=authors, journal=journal, year=year, title=title, link=link, href=href)

    with open(output_file, 'w') as f:
        f.write(html_string)

def main():
    parser = argparse.ArgumentParser(description='Convert a .bib file into an HTML page')
    parser.add_argument('-i', '--input', help='The .bib file to parse', required=True)
    parser.add_argument('-o', '--output', help='The output HTML file name', required=True)

    args = parser.parse_args()

    with open(args.input) as bibtex_file:
        bibtex_str = bibtex_file.read()

    bib_database = bibtexparser.loads(bibtex_str)
    create_html_page(bib_database.entries, args.output)

if __name__ == '__main__':
    main()