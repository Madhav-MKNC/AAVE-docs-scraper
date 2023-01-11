#!/usr/bin/env python3

# Title:    AAVE's Docs Scraper
# Author:   MKNC
# created:  10-01-2023 19:30 IST
# version 1

# requests      --> for scraping html data from an url
# BeautifulSoup --> for parsing the html data in a tree like structure
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import os
from platform import uname
def clearScreen():
    os.system('cls' if 'win' in uname().system.lower() else 'clear')

# for saving the data
def saveData(fname, data):
    with open(fname,'w',encoding="utf-8") as file:
        file.write(str(fname))

# scraping links
def get_paths(domain, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    urls = [url]
    for link in soup.find_all('a'):
        path = link.get('href')
        if path.startswith('/'):
            path = urljoin(url,path)
        if path.startswith(domain) and '#' not in path: 
            urls.append(path)

    return list(set(urls))

# page content
def fetch_data(url, content_class, dirName='data'):
    try:
        print("[+] Scraping",url)
        response = requests.get(url)
        data = BeautifulSoup(response.text, 'html.parser')
        title = data.find('title').text
        data = data.find_all(class_=content_class)[1:]      # skips the first element
    except Exception as e:
        print("[!] Failed to fetch",url)
        print("[ERROR:]",e)
        return

    # saving data
    fileName = f"{dirName}/{title}.txt"
    content = f"[{title}]\n"
    content += f"[{url}]]\n"
    for i in data:
        content+='\n'+i.text.strip()+'\n'
    saveData(fileName, content)

if __name__ == "__main__":
    clearScreen()
    print("AAVE's Docs Scraper\n")
    print("[+] Data will saved in 'data/' in the currect directory")

    if os.path.exists('data'): 
        print("[-] 'data/' directory already Exists, saving all the data here")
    else:
        print("[+] Creating directory 'data/'")
        os.mkdir('data')
    
    # input
    data_class = "css-175oi2r r-bnwqim"
    url = "https://docs.aave.com/hub/"
    domain = '/'.join(url.split('/')[0:3])+'/'
    
    # output
    try:
        for path in get_paths(domain=domain, url=url):
            fetch_data(path, content_class=data_class, dirName='data')
    except KeyboardInterrupt:
        print("[-] KeyBoard interrupted")
        print("[-] Exiting...")

