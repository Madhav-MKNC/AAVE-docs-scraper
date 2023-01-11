#!/usr/bin/env python3

# """
# Title:    Links Crawler
# author:   MKNC
# created:  12-01-2023 01:50 
# """

from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

import os
from platform import uname
def printScreen():
    os.system('cls' if 'win' in uname().system.lower() else 'clear')
    print("["+"="*30+" LINKS CRAWLER "+"="*30+"]\n")

class Crawler:
    def __init__(self, base_url, restricted_domain='https://'):
        self.urls = [base_url]
        self.urls_dict = dict()
        self.restricted_domain = restricted_domain
    
    def inList(self, url):
        try: return self.urls_dict[url]
        except: return False

    def crawl_all_links(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if not path.startswith('http'): path = urljoin(url,path)

            if self.inList(path): continue
            if '#' in path: continue
            if not path.startswith(self.restricted_domain): continue

            print("[+] Link found -",path)
            self.urls.append(path)
            self.urls_dict[path] = True

    def crawl(self):
        while self.urls:
            url = self.urls.pop(0)
            print("[+] Crawling:",url)
            try:
                self.crawl_all_links(url)
            except AttributeError:
                print(f'[-] No href on : {url}\n')
            except Exception as e:
                print(f'[!] Failed to crawl: {url}')
                print("[!] REASON:",e,'\n')

    def saveData(self, fname='links_found.txt'):
        with open(fname,'w',encoding="utf-8") as file:
            file.write("\n".join(self.urls))
        print("[+] list saved in 'links_crawled.txt'")

if __name__ == '__main__':
    printScreen()

    url = input('[=] Enter the base url you want to crawl: ')
    url = "https://docs.aave.com/"
    if not url.startswith('http'): url = 'https://'+url

    try:
        aave = Crawler(base_url=url)
        aave.crawl()
    except KeyboardInterrupt:
        print("[Program Stopped]")
    aave.saveData()

    print("len(urls) =",len(aave.urls))
    print("len(set(urls)) =",len(set(aave.urls)))

