import glob
from bs4 import BeautifulSoup

#href="{{ url_for('static', filename='assets/img/apple-icon.png') }}
tim_files = './app/static/pk2-free-v2/**/*.html'
opening_braces = '{{'
closing_braces = '}}'

for filename in glob.iglob(tim_files, recursive=True):
    print(f'************File: {filename}')
    with open(filename, 'r+') as f:
        html_doc = f.read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        anchors = soup.findAll('a', href=True)
        links = soup.findAll('link', href=True)
        elements_with_hrefs = []
        elements_with_hrefs.extend(list(anchors))
        elements_with_hrefs.extend(list(links))

        for anchor in list(set(elements_with_hrefs)):
            if not anchor['href'].startswith('#') and not anchor['href'].startswith('http') and not anchor['href'].startswith('{{'):
                href = anchor['href']
                print(f"\t{href}")
                replacement_href = f"{opening_braces} url_for('static', filename='{href}') {closing_braces}"
                print(f"\t\t{replacement_href}")
                html_doc = html_doc.replace(href, replacement_href)

        imgs = soup.findAll('img', src=True)
        for img in list(set(imgs)):
            if not img['src'].startswith('http') and not anchor['href'].startswith('{{'):
                original_src = img['src']
                replacement_src = f"{opening_braces} url_for('static', filename='{original_src}') {closing_braces}"
                html_doc = html_doc.replace(original_src, replacement_src)

        scripts = soup.findAll('script', src=True)
        for script in list(set(scripts)):
            if not script['src'].startswith('http') and not anchor['href'].startswith('{{'):
                original_src = script['src']
                replacement_src = f"{opening_braces} url_for('static', filename='{original_src}') {closing_braces}"
                html_doc = html_doc.replace(original_src, replacement_src)

        print(html_doc)
        f.write(html_doc)

        break