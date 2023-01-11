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
def printScreen():
    os.system('cls' if 'win' in uname().system.lower() else 'clear')
    print("<"+"="*50+" AAVE's Docs Scraper "+"="*50+">\n")

from time import time 
def makeDir(dname):
    now = str(int(time()))
    if os.path.exists(dname): 
        print(f"[-] '{dname}/' directory already Exists, creating and saving all the data in '{dname} {now}/' directory")
        dname = f"{dname} {now}"
    else:
        print(f"[+] Creating directory '{dname}'")
    os.mkdir(dname)

# for saving the data
def saveData(fname, data):
    with open(fname,'w',encoding="utf-8") as file:
        file.write(str(data))

# links crawler class
class Crawler:
    def __init__(self, base_url, restricted_domain='https://'):
        self.urls = [base_url]
        self.links_found = [base_url]
        self.restricted_domain = restricted_domain

    def fetch_all_links(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if not path.startswith('http'): path = urljoin(url,path)

            if '#' in path: continue
            if not path.startswith(self.restricted_domain): continue
            if path in self.links_found: continue

            print("[+] Link found -",path)
            self.urls.append(path)
            self.links_found.append(path)

    def crawl(self, crawl_limit=20):
        while self.urls:
            if len(self.links_found)>crawl_limit: break

            url = self.urls.pop(0)
            print("[+] Crawling:",url)
            try:
                self.fetch_all_links(url)
            except AttributeError:
                print(f'[-] No href on : {url}\n')
            except Exception as e:
                print(f'[!] Failed to crawl: {url}')
                print("[!] REASON:",e,'\n')

# page content
def fetch_data(url, content_class, dirName='.'):
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


def scrape_all(url,content_class,dirName):
    domain = '/'.join(url.split('/')[0:3])+'/'
    aave = Crawler(base_url=url, restricted_domain=domain)
    aave.crawl(crawl_limit=20)
    saveData(f'{dirName}/links_found.txt',"/n".join(aave.links_found))

    for path in aave.links_found:
        try:
            print("[+] Scraping",path)
            fetch_data(path, content_class,dirName)
        except Exception as e:
            print("[!] Failed to fetch",path)
            print("[ERROR]",e)


    
if __name__ == "__main__":
    printScreen()
    
    root_dir = input("[=] Enter a root directory name: ")
    print(f"[+] Data will saved in '{root_dir}' in the currect directory")
    makeDir(root_dir)

    url = "https://docs.aave.com/"
    data_class = "css-175oi2r r-bnwqim"

    try:
        scrape_all(url,data_class,root_dir)
    except KeyboardInterrupt:
        print("[-] KeyBoard interrupted")
        print("Exiting...")
