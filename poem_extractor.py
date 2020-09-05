import requests
import urllib
import time
from bs4 import BeautifulSoup

start_time = time.time()
main_url = "https://www.samakalinsahitya.com"
base_url = "https://www.samakalinsahitya.com/index.php?page=0&show=category&cat_id=3"
base_page = requests.get(base_url)

soup = BeautifulSoup(base_page.content, 'lxml')
last_page_url = soup.find(text="Last").parent["href"]
parsed = urllib.parse.urlparse(last_page_url)
last_page_number = int(urllib.parse.parse_qs(parsed.query)['page'][0])

all_pages_url = [base_url]

for i in range(1, last_page_number+1):
    param, newvalue = 'page', i
    parsed = urllib.parse.urlsplit(base_url)
    query_dict = urllib.parse.parse_qs(parsed.query)
    query_dict[param][0] = newvalue
    query_new = urllib.parse.urlencode(query_dict, doseq=True)
    parsed = parsed._replace(query=query_new)
    url_new = (parsed.geturl())
    all_pages_url.append(url_new)

all_poems = []

for url in all_pages_url:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    unordered_list = soup.find(
            'div', {'class': 'col-md-6 content'}
            ).find("ul").find_all("li")

    for each in unordered_list:
        all_poems.append(each.find("a")["href"])

# print(all_poems)

f = open("poems.txt", "w")
for each in all_poems:
    page = requests.get(main_url+each)
    soup = BeautifulSoup(page.content, 'lxml')
    content = soup.find(
                'div', {'class': 'col-md-6 content'}
            )
    for ul in content.find_all('div', {'class': 'comment'}):
        ul.decompose()
    try:
        text = ""
        text += content.find("h2").text
        text += "\n"
        text += content.find("h4").text
        text += "\n"
        text += content.find("p").text
        text += "\n"
        text += "\n"
        text += "\n"
        text += "*" * 79
        text += "\n"
        f.write(text)
    except:
        pass
f.close()

end_time = time.time()
print(f'Total_time taken for script to execute: {(end_time - start_time)/60 } minutes')
