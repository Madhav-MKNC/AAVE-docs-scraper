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

from time import time as now 
def makeDir(dname):
    now = str(int(now()))
    if os.path.exists(dname): 
        print(f"[-] '{dname}' directory already Exists, creating and saving all the data in '{dname} {now}/' directory")
        dname = f"{dname} {now}"
    else:
        print(f"[+] Creating directory '{dname}'")
        os.mkdir(dname)

# for saving the data
def saveData(fname, data):
    with open(fname,'w',encoding="utf-8") as file:
        file.write(str(data))

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


def crawl(url,content_class,root_dir):
    makeDir(root_dir)
    
    fetch_data(url,url,content_class,dirName=root_dir)
    print(f"[+] Scraping all the links found on - {url}\n")

    try:
        print(get_paths(url))
        print(url)
        for path in get_paths(url):
            print(1)
            try:
                for link in get_paths(path):
                    print("[+] Scraping",link)
                    fetch_data(url,link, data_class,dirName='data')
            except Exception as e:
                print("[!] Failed to fetch",link)
                print("[=]",e)
    except KeyboardInterrupt:
        print("[-] KeyBoard interrupted")
        print("[-] Exiting...")

    
if __name__ == "__main__":
    clearScreen()
    print("AAVE's Docs Scraper\n")

    root_dir = input("[=] Enter a root directory name: ")
    print(f"[+] Data will saved in '{root_dir}' in the currect directory")

    
    url = "https://docs.aave.com/hub/"
    if 'http' not in url: 
        print('[!] Enter full url, for eg. https://example.xyz/')
        exit()

    data_class = "css-175oi2r r-bnwqim"
    crawl(url,data_class,root_dir)
