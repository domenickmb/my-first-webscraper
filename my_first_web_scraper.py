#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 23:18:00 2020
Author: Domenick Botardo

Program Description:
    This webscraper parse and extracts data about laptop details on
    http://webscrape.io/test-sites/e-commerce/static/computers/laptops.
    It then prints the gathered data on screen and saves it to a csv file.
"""
import requests
import csv
from bs4 import BeautifulSoup
from collections import namedtuple

def get_product_details(product_soup):
    """
    Extract the specific details of the product.
    Returns an instance of Product namedtuple.
    """
    Product = namedtuple('Product', 'title description price rating reviews')
    title = product_soup.find('a', {'class':'title'}).attrs['title']
    description = product_soup.find('p', {'class':'description'}).text.strip()
    price = product_soup.find('h4', {'class':'pull-right price'}).text.strip()
    rating_container = product_soup.find('div', {'class':'ratings'})
    rating = rating_container.find_all('p')[1].attrs['data-rating']
    reviews = rating_container.find('p', {'class':'pull-right'}).text.strip()
    return Product(title=title, description=description,
                   price=price, rating=rating, reviews=reviews)


def print_product(product):
    """Print product details on screen"""
    print('Model:', product.title)
    print('Description:', product.description)
    print('Price:', product.price)
    print('Rating:', product.rating)
    print('Reviews:', product.reviews)
    print()


def write_csv(filename, product_list):
    """Write all gathered data on a csv file"""
    with open(filename, mode='w', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        headers = ['Model', 'Description', 'Price', 'Rating', 'Reviews']
        csv_writer.writerow(headers)
        for product in product_list:
            csv_writer.writerow(product)
        
        
def crawl_data(url):
    """The main function where we parse and scrape the data"""
    product_list = []
    # We loop until there's no next page
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for item in soup.find_all('div', {'class':'thumbnail'}):
            product = get_product_details(item)
            product_list.append(product)
            print_product(product)
            
        # Get the next page and set it as the new url if it exists,
        # otherwise, set the url to None to terminate the loop
        next_page = soup.find('a', {'rel':'next'})
        if next_page:
            next_page = next_page['href']
            # next_page is an internal link so we concatenate
            # to get the domain to get the complete url
            url = domain + next_page
        else:
            url = None
    
    # Save all the gathered data on a csv file
    write_csv('laptops.csv', product_list)
      
domain = 'https://webscraper.io'
start_url = f'{domain}/test-sites/e-commerce/static/computers/laptops'
crawl_data(start_url)
