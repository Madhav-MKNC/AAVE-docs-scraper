#!/usr/bin/env python3
# Title:    AAVE's Docs Scraper
# Author:   MKNC (https://github.com/Madhav-MKNC)
# created:  10-01-2023 19:30 IST

# imports
import os
from platform import uname
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# scraping links
def get_paths(url):
    # url = "https://docs.aave.com/hub/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        path = link.get('href')
        if not path.startswith('/'):
            path = urljoin(url,path)
        if path.startswith('https://docs.aave.com/') and '#' not in path: 
            urls.append(path)
    return list(set(urls))

# page content
def fetch_data(url,content_class,write_to_file=True,dirName='data'):
    response = requests.get(url)
    data = BeautifulSoup(response.text, 'html.parser')
    title = data.find('title').text
    data = data.find_all(class_=content_class)[1:]      # skips the first element

    content = f"[{title}]\n"
    content += f"[{url}]]\n"
    for i in data:
        content+='\n'+i.text.strip()+'\n'

    if write_to_file:
        fileName = f"{dirName}/{title}.txt"
        with open(fileName,'w',encoding="utf-8") as file:
            file.write(str(content))
    else: print(content)
    return content

if __name__ == "__main__":
    os.system('cls' if 'win' in uname().system.lower() else 'clear')
    print("AAVE's Docs Scraper\n")
    print("[+] Data will saved in 'data/' in the currect directory")
    if os.path.exists('data'): 
        print("[-] 'data/' directory already Exists, saving all the data here")
    else:
        print("[+] Creating directory 'data/'")
        os.mkdir('data')
    
    data_class = "css-175oi2r r-bnwqim"
    url = "https://docs.aave.com/hub/"
    fetch_data(url,data_class,write_to_file=True,dirName='data')

    print(f"[+] Scraping all the links found on - {url}\n")
    try:
        for url in get_paths(url):
            try:
                print("[+] Scraping",url)
                fetch_data(url, data_class, write_to_file=True,dirName='data')
            except Exception as e:
                print("[!] Failed to fetch",url)
                print("[=]",e)
    except KeyboardInterrupt:
        print("[-] KeyBoard interrupted")
        print("[-] Exiting...")





"""
# # ignore this
chapters_class = "css-1rynq56 r-1ro0kt6 r-16y2uox r-1wbh5a2 r-oyd9sg r-gg6oyi r-1b43r93 r-16dba41 r-hbpseb r-1bnj018"
headings_class = "css-1rynq56 r-1nf4jbm r-fdjqy7 r-1xnzce8"
only_data_class = "css-1rynq56 r-gg6oyi r-ubezar r-16dba41 r-135wba7 r-1nf4jbm r-fdjqy7 r-1xnzce8"
heading_data_class = "r-fdjqy7"
"""
