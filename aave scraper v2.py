#!/usr/bin/env python3

# Title:    AAVE's Docs Scraper
# Author:   MKNC
# created:  10-01-2023 19:30 IST
# version 1

# requests      --> for scraping html data from an url
# BeautifulSoup --> for parsing the html data in a tree like structure
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

import os
from platform import uname
def printScreen():
    os.system('cls' if 'win' in uname().system.lower() else 'clear')
    print("<"+"="*50+" AAVE's Docs Scraper "+"="*50+">\n")

# for unique directory names
def get_dirname(dname):
    if os.path.exists(dname):
        print(dname)
        dname += "1"
        print(dname)
        return get_dirname(dname)
    return dname

def makeDir(dname):
    os.mkdir(dname)
    # if os.path.exists(dname): 
    #     new_dname = get_dirname(dname)
    #     print(f"[-] '{dname}/' directory already Exists, creating and saving all the data in '{new_dname}/' directory")
    #     os.mkdir(new_dname)
    # else:
    #     print(f"[+] Creating directory '{dname}'")
    #     os.mkdir(dname)

# for saving the data
def saveData(fname, data):
    with open(fname,'w',encoding="utf-8") as file:
        file.write(str(data))

# links crawler class
class Crawler:
    def __init__(self, base_url, restricted_domain='', crawl_limit=20):
        self.urls = [base_url]
        self.links_found = []
        self.restricted_domain = restricted_domain
        self.crawl_limit = crawl_limit

    def fetch_all_links(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            if len(self.links_found)>self.crawl_limit: return

            path = link.get('href')
            if not path.startswith('http'): path = urljoin(url,path)

            if '#' in path: continue
            if urlparse(path).hostname != self.restricted_domain and self.restricted_domain!='': continue
            if path in self.links_found: continue

            print("[*] Link found -",path)
            self.urls.append(path)
            self.links_found.append(path)

    def crawl(self):
        while self.urls:
            url = self.urls.pop(0)
            print(f"[+] Crawling: {url}\n")
            try:
                self.fetch_all_links(url)
            except Exception as e:
                print(f'[!] Failed to crawl: {url}')
                print("[!] REASON:",e,'\n')

# page content
index = 0
def fetch_data(url, content_class, dirName='.'):
    global index
    try:
        print(f"[{index}] Scraping {url}")
        index += 1
        response = requests.get(url)
        data = BeautifulSoup(response.text, 'html.parser')
        # title = data.find('title').text     # for filename = title of page
        data = data.find_all(class_=content_class)[1:]      # skips the first element
    except Exception as e:
        print("[!] Failed to fetch",url)
        print("[ERROR]",e)
        return

    # title => filename
    title = urlparse(url).path[1:-1].replace('/','-')
    fileName = f"{dirName}/{title}.txt"

    # data -> file
    content = f"[{title}]\n"
    content += f"[{url}]\n"
    for i in data:
        content += '\n'+i.text.strip()+'\n'
    saveData(fileName, content)


def scrape_all(url, content_class, dirName, crawl_limit):
    domain = urlparse(url).hostname
    aave = Crawler(base_url=url, restricted_domain=domain, crawl_limit=crawl_limit)
    aave.crawl()
    saveData(f'{dirName}/links_found.txt',"/n".join(aave.links_found))

    for path in aave.links_found:
        try:
            fetch_data(path, content_class,dirName)
        except Exception as e:
            print("[!] Failed to fetch",path)
            print("[ERROR]",e)


    
if __name__ == "__main__":
    printScreen()
    
    root_dir = input("[=] create a directory in currect directory for saving all the data: ")
    root_dir = get_dirname(root_dir)
    makeDir(root_dir)

    url = "https://docs.aave.com/"
    ## UPDATE THIS VALUE IF NO DATA IS FETCHED
    # it might be possible that the website developers may have changed the content class or maybe just modified
    data_class = "r-1xnzce8"

    crawl_limit = input("[=] Enter a crawl limit: ")
    if not crawl_limit.isnumeric():
        print("[!] Enter a valid number")
        exit()

    try:
        scrape_all(url, data_class, root_dir, int(crawl_limit))
    except KeyboardInterrupt:
        print("[-] KeyBoard interrupted")
        print("Exiting...")
