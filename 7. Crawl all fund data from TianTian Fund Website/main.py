# -*- coding:utf-8 -*-

import requests
import random
import re
import queue
import threading
import csv
import json

# List of User-Agent strings to mimic different browsers
user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36'
]

# List of Referer URLs to mimic requests coming from different pages
referer_list = [
    'http://fund.eastmoney.com/110022.html',
    'http://fund.eastmoney.com/110023.html',
    'http://fund.eastmoney.com/110024.html',
    'http://fund.eastmoney.com/110025.html'
]

# Function to get a proxy from a proxy pool
# This function calls an external API to get a proxy
# It's recommended to set up a local proxy pool for better performance
def get_proxy():
    data_json = requests.get("http://proxy.1again.cc:35050/api/v1/proxy/?type=2").text
    data = json.loads(data_json)
    return data['data']['proxy']

# Function to get all fund codes from Eastmoney
def get_fund_code():
    # Select a random User-Agent and Referer
    header = {'User-Agent': random.choice(user_agent_list),
              'Referer': random.choice(referer_list)
    }

    # Make a request to the Eastmoney API to get fund codes
    req = requests.get('http://fund.eastmoney.com/js/fundcode_search.js', timeout=5, headers=header)

    # Process the response to extract fund codes
    fund_code = req.content.decode()
    fund_code = fund_code.replace("﻿var r = [","").replace("];","")

    # Use regex to find all fund code entries
    fund_code = re.findall(r"[\[](.*?)[\]]", fund_code)

    # Parse each entry and store in a list
    fund_code_list = []
    for sub_data in fund_code:
        data = sub_data.replace("\"","").replace("'","")
        data_list = data.split(",")
        fund_code_list.append(data_list)

    return fund_code_list

# Function to get fund data using the fund code
def get_fund_data():
    # Continue processing while there are fund codes in the queue
    while (not fund_code_queue.empty()):
        # Get a fund code from the queue
        fund_code = fund_code_queue.get()

        # Get a proxy for the request
        proxy = get_proxy()

        # Select a random User-Agent and Referer
        header = {'User-Agent': random.choice(user_agent_list),
                  'Referer': random.choice(referer_list)
        }

        # Use try-except to handle exceptions and retry if necessary
        try:
            # Make a request to the fund data API using the proxy
            req = requests.get("http://fundgz.1234567.com.cn/js/" + str(fund_code) + ".js", proxies={"http": proxy}, timeout=3, headers=header)

            # Process the response to extract fund data
            data = (req.content.decode()).replace("jsonpgz(","").replace(");","").replace("'","\"")
            data_dict = json.loads(data)
            print(data_dict)

            # Acquire a lock to safely write to the CSV file
            mutex_lock.acquire()

            # Write the data to a CSV file
            with open('./fund_data.csv', 'a+', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                data_list = [x for x in data_dict.values()]
                csv_writer.writerow(data_list)

            # Release the lock after writing
            mutex_lock.release()

        except Exception:
            # If an error occurs, put the fund code back into the queue
            fund_code_queue.put(fund_code)
            print("Access failed, trying with another proxy")

if __name__ == '__main__':
    # Get all fund codes
    fund_code_list = get_fund_code()

    # Create a queue to hold the fund codes
    fund_code_queue = queue.Queue(len(fund_code_list))
    # Add each fund code to the queue
    for i in range(len(fund_code_list)):
        fund_code_queue.put(fund_code_list[i][0])

    # Create a lock to synchronize file writing among threads
    mutex_lock = threading.Lock()
    # Create and start multiple threads to improve crawling efficiency
    for i in range(50):
        t = threading.Thread(target=get_fund_data, name='LoopThread'+str(i))
        t.start()
