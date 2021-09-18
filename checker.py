# coding=utf-8
from bs4 import BeautifulSoup
import requests
from mailer import Mailer
import time


class Checker:
    def __init__(self):
        self.url = 'https://www.1177.se/Stockholm/sjukdomar--besvar/lungor-och-luftvagar/inflammation-och-infektion-ilungor-och-luftror/om-covid-19--coronavirus/om-vaccin-mot-covid-19/boka-tid-for-vaccination-mot-covid-19-i-stockholms-lan/'
        self.mailer = Mailer()
        self.soup = None
        self.original_headers = {
            'Vaccination av dos 2 – så bokar du',
            'Född 1962-1976 – så bokar du ',
            'Född 1962-1971 – så bokar du ',
            'Född 1957-1961 – så bokar du',
            'Född 1952-1956 – så bokar du',
            'Född 1947-1951 – så bokar du',
            'Född 1942-1946 – så bokar du',
            'Född 1941 eller tidigare – så bokar du',
            'Född 1951 eller tidigare – så bokar du',
            'Gjort transplantation eller har dialys? Så bokar du',
            'Insatser via LSS – så bokar du',
            'Bokning för dig som tillhör en riskgrupp',
            'Bokning för personer som har svårt att följa rekommendationer'
        }
        self.fetched_headers = []

    def get_page(self):
        headers = {
            'User-Agent': 'Googlebot-Video/1.0',
        }
        r = requests.get(self.url, headers=headers)
        print('[GET] ' + self.url)
        self.soup = BeautifulSoup(r.text, 'html.parser')

    def get_headers(self):
        c_teasers = self.soup.find_all("a", {"class": "c-teaser"})
        c_teaser_heading_link = self.soup.find_all("span", {"class": "c-teaser__heading__link"})
        print("Headers:")
        for link in c_teaser_heading_link:
            print(link.string)
            self.fetched_headers.append(link.string)
        print("-----------------")
        print("Found headers: " + str(len(c_teaser_heading_link)))

    def check_changed_number_of_posts(self):
        if len(self.fetched_headers) == 0:
            print("Number of posts: 0! Website is down for maintenance?")
            return

        if len(self.fetched_headers) != len(self.original_headers):
            print("Number of posts: something changed!")
            self.mailer.send_email("Number of posts: something changed!", [], self.url)
        else:
            print("Number of posts: no changes!")

    def check_content(self):
        if len(self.fetched_headers) == 0:
            print("Number of posts: 0 content! Website is down for maintenance?")
            return

        diff = []
        for fetched_header in self.fetched_headers:
            if fetched_header not in self.original_headers:
                diff.append(fetched_header)
        if len(diff) > 0:
            print(diff)
            print("Content: something changed!")
            self.mailer.send_email("Content: something changed!", diff, self.url)
        else:
            print("Content: no changes!")


while True:
    checker = Checker()
    checker.get_page()
    checker.get_headers()
    checker.check_content()
    print('')
    print('zzz 1 minutes')
    time.sleep(1 * 60)

