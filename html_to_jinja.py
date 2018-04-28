import glob
from bs4 import BeautifulSoup
import re

"""
This script will help take a creative-tim theme, and convert it to a jinja2 template that can be used in a Flask
application.

It essentially takes all of the href to files, and wraps them in a url_for to the static directory.

It may not get everything, but it does a decent job of getting a lot of the links setup for jinja2 and Flask.
"""


regex = r".*url\(\'(.*)\'\)"

#href="{{ url_for('static', filename='assets/img/apple-icon.png') }}
#tim_files = './app/static/pk2-free-v2/**/*.html'
tim_files = './creative-tim/junk3/**/*.html'
opening_braces = '{{'
closing_braces = '}}'

updated_files = []

for filename in glob.iglob(tim_files, recursive=True):
    print(f'************File: {filename}')
    changed_file = False
    # guarantee unique hrefs to replace
    href_dict = {}
    img_dict = {}
    script_dict = {}
    style_dict = {}
    with open(filename, 'r') as f:
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
                if href not in href_dict:
                    # print(f"\t{href}")
                    replacement_href = f"{opening_braces} url_for('static', filename='{href}') {closing_braces}"
                    # print(f"\t\t{replacement_href}")
                    html_doc = html_doc.replace(href, replacement_href)
                    changed_file = True
                    href_dict[href]=href

        imgs = soup.findAll('img', src=True)
        for img in list(set(imgs)):
            if not img['src'].startswith('http') and not img['src'].startswith('{{'):
                original_src = img['src']
                if original_src not in img_dict:
                    replacement_src = f"{opening_braces} url_for('static', filename='{original_src}') {closing_braces}"
                    html_doc = html_doc.replace(original_src, replacement_src)
                    changed_file = True
                    img_dict[original_src]=original_src


        scripts = soup.findAll('script', src=True)
        for script in list(set(scripts)):
            if not script['src'].startswith('http') and not script['src'].startswith('{{'):
                original_src = script['src']
                if original_src not in script_dict:
                    replacement_src = f"{opening_braces} url_for('static', filename='{original_src}') {closing_braces}"
                    html_doc = html_doc.replace(original_src, replacement_src)
                    changed_file = True
                    script_dict[original_src]=original_src

        style_background_images = soup.findAll('div', style=True)
        for style_background_image in list(set(style_background_images)):
            if style_background_image['style'].startswith('background-image:'):
                original_style = style_background_image['style']
                if original_style not in style_dict:
                    try:
                        file_path = re.match(regex, original_style).group(1)
                        replacement_style = f"background-image: url({opening_braces} url_for('static', filename='{file_path}', _external=True) {closing_braces})"
                        html_doc = html_doc.replace(original_style, replacement_style)
                        changed_file = True
                        style_dict[original_style]=original_style
                    except:
                        pass

        updated_files.append((filename, html_doc))



# update the files
if changed_file and updated_files:
    for filename, content in updated_files:
        with open(filename, "w") as f:
            print(f"Update file: {filename}")
            f.write(content)