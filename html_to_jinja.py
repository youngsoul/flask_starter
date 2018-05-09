import glob
from bs4 import BeautifulSoup
import re

"""
This script will help take a creative-tim theme, and convert it to a jinja2 template that can be used in a Flask
application.

It essentially takes all of the href to files, and wraps them in a url_for to the static directory.

It may not get everything, but it does a decent job of getting a lot of the links setup for jinja2 and Flask.
"""

# relative path to the html files to process into jinja2 Flask templates
tim_files = './app/static/pk2-free-v2/**/*.html'


regex = r".*url\(\'(.*)\'\)"

opening_braces = '{{'
closing_braces = '}}'

updated_files = []


def process_html(html_doc, filename='Internal'):
    """
    This method can take just an html_doc string, and the name of the file associated with the html_doc string
    and process the string.  This is handy if you have just a snippet of html to process.  The filename in that case
    can be anything.
    :param html_doc: String of html to process
    :param filename: The name of the file where it came from
    :return:
    """
    changed_file = False
    # guarantee unique hrefs to replace
    href_dict = {}
    img_dict = {}
    script_dict = {}
    style_dict = {}

    soup = BeautifulSoup(html_doc, 'html.parser')
    anchors = soup.findAll('a', href=True)
    links = soup.findAll('link', href=True)
    elements_with_hrefs = []
    elements_with_hrefs.extend(list(anchors))
    elements_with_hrefs.extend(list(links))
    for anchor in list(set(elements_with_hrefs)):
        if not anchor['href'].startswith('#') and not anchor['href'].startswith('http') and not anchor[
            'href'].startswith('{{'):
            href = anchor['href']
            if href not in href_dict:
                # print(f"\t{href}")
                replacement_href = f"{opening_braces} url_for('static', filename='{href}') {closing_braces}"
                # print(f"\t\t{replacement_href}")
                html_doc = html_doc.replace(href, replacement_href)
                changed_file = True
                href_dict[href] = href
    imgs = soup.findAll('img', src=True)
    for img in list(set(imgs)):
        if not img['src'].startswith('http') and not img['src'].startswith('{{'):
            original_src = img['src']
            if original_src not in img_dict:
                replacement_src = f"{opening_braces} url_for('static', filename='{original_src}') {closing_braces}"
                html_doc = html_doc.replace(original_src, replacement_src)
                changed_file = True
                img_dict[original_src] = original_src
    scripts = soup.findAll('script', src=True)
    for script in list(set(scripts)):
        if not script['src'].startswith('http') and not script['src'].startswith('{{'):
            original_src = script['src']
            if original_src not in script_dict:
                replacement_src = f"{opening_braces} url_for('static', filename='{original_src}') {closing_braces}"
                html_doc = html_doc.replace(original_src, replacement_src)
                changed_file = True
                script_dict[original_src] = original_src
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
                    style_dict[original_style] = original_style
                except:
                    pass
    updated_files.append((filename, html_doc))

    return changed_file, updated_files


def process_all_files(html_files_path):
    """
    Process all of the files in the directory, AND ALL SUBDIRECTORIES, from the specified root.
    :param html_files_path:
    :return: changed_file (True if files were changed, False if no files were changed), updated_files tuple of filename, and changed html_doc string
    """
    for filename in glob.iglob(html_files_path, recursive=True):
        print(f'************File: {filename}')
        with open(filename, 'r') as f:
            html_doc = f.read()
            changed_file, updated_files = process_html(html_doc, filename)

    # update the files
    if changed_file and updated_files:
        for filename, content in updated_files:
            with open(filename, "w") as f:
                print(f"Update file: {filename}")
                f.write(content)


if __name__ == '__main__':

    # process_all_files(tim_files)

    changed_file, updated_files = process_html("""
                    <div class="nav-tabs-navigation">
                    <div class="nav-tabs-wrapper">
                        <ul class="nav nav-tabs" role="tablist">
                            <li class="nav-item">
                                <a class="nav-link active" data-toggle="tab" href="#follows" role="tab">Follows</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" data-toggle="tab" href="#following" role="tab">Following</a>
                            </li>
                        </ul>
                    </div>
                </div>
                <!-- Tab panes -->
                <div class="tab-content following">
                    <div class="tab-pane active" id="follows" role="tabpanel">
                        <div class="row">
                            <div class="col-md-6 ml-auto mr-auto">
                                <ul class="list-unstyled follows">
                                    <li>
                                        <div class="row">
                                            <div class="col-md-2 col-sm-2 ml-auto mr-auto">
                                                <img src="../assets/img/faces/clem-onojeghuo-2.jpg" alt="Circle Image" class="img-circle img-no-padding img-responsive">
                                            </div>
                                            <div class="col-md-7 col-sm-4  ml-auto mr-auto">
                                                <h6>Flume<br/><small>Musical Producer</small></h6>
                                            </div>
                                            <div class="col-md-3 col-sm-2  ml-auto mr-auto">
												<div class="form-check">
					                                <label class="form-check-label">
					                                    <input class="form-check-input" type="checkbox" value="" checked>
					                                    <span class="form-check-sign"></span>
					                                </label>
					                            </div>
                                            </div>
                                        </div>
                                    </li>
                                    <hr />
                                    <li>
                                        <div class="row">
                                            <div class="col-md-2 ml-auto mr-auto ">
                                                <img src="../assets/img/faces/ayo-ogunseinde-2.jpg" alt="Circle Image" class="img-circle img-no-padding img-responsive">
                                            </div>
                                            <div class="col-md-7 col-sm-4">
                                                <h6>Banks<br /><small>Singer</small></h6>
                                            </div>
                                            <div class="col-md-3 col-sm-2">
												<div class="form-check">
					                                <label class="form-check-label">
					                                    <input class="form-check-input" type="checkbox" value="">
					                                    <span class="form-check-sign"></span>
					                                </label>
					                            </div>
                                            </div>
                                        </div>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="tab-pane text-center" id="following" role="tabpanel">
                        <h3 class="text-muted">Not following anyone yet :(</h3>
                        <button class="btn btn-warning btn-round">Find artists</button>
                    </div>
                </div>""")


    print(updated_files[0][1])