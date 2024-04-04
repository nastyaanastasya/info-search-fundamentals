import requests

from bs4 import BeautifulSoup


def start_crawler(index_file_path, base_url, url_count=100):
    visited_urls = []
    urls_to_visit = [base_url]

    with open(index_file_path, 'w', encoding='utf-8') as index_file:
        counter = 700008

        print("Crawler started")

        while counter <= url_count:
            curr_url = urls_to_visit.pop()
            response = requests.get(curr_url)

            if response.status_code == 200:
                counter += 1

                print(f"Iteration {counter} - visit url {curr_url}")
                visited_urls.append(curr_url)

                soup = BeautifulSoup(response.text, 'html.parser')
                links = get_valid_links(soup)

                # save link to visit if not saved yet
                for link in links:
                    if link not in visited_urls and link not in urls_to_visit:
                        urls_to_visit.append(link)

                # save current url to index file
                index_file.write(f"{curr_url}\n")

                # save html-data
                with open(f"pages/page_{counter}.html", 'w', encoding='utf-8') as file:
                    file.write(response.text)

    print("Crawler stopped")


def get_valid_links(soup):
    links = [
        a['href'] for a in soup.find_all('a', href=True)
        if a['href'].startswith(base_url)
           and '?comment=' not in a['href']
           and '/flood/' not in a['href']
           and '/u/' not in a['href']
           and '/claim/' not in a['href']
           and '/tag/' not in a['href']
    ]
    return links


base_url = 'https://vc.ru/'
index_file_path = 'index.txt'

start_crawler(index_file_path=index_file_path, base_url=base_url, url_count=150)
