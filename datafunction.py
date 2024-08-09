import csv
import json
import xlrd
import zipfile
import requests
import functools
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def get_json(url):
    """
    Request a HTTP GET method to the given url (for REST API)
    and return its response as the dict object.

    Args:
    ====
    url: string
        valid url for REST API
    """
    try:
        print("HTTP GET", url)
        r = requests.get(url)
        json_dict = r.json()
        return json_dict
    except requests.exceptions.RequestException as error:    
        print(error)

def download_json(url, filepath):
    """
    Request a HTTP GET method to the given url (for REST API)
    and save its response as the json file.

    url: string
        valid url for REST API
    filepath: string
        valid path to the destination file
    """
    try:
        print("HTTP GET", url)
        r = requests.get(url)
        json_dict = r.json()
        json_str = json.dumps(json_dict, indent=2, ensure_ascii=False)
        with open(filepath, "w") as f:
            f.write(json_str)
    except requests.exceptions.RequestException as error:
        print(error)

def download_csv(url, filepath, enc="utf-8", dec="utf-8", logging=False):
    """
    Request a HTTP GET method to the given url (for REST API)
    and save its response as the csv file.

    url: string
        valid url for REST API
    filepathe: string
        valid path to the destination file
    enc: string
        encoding type for a content in a given url
    dec: string
        decoding type for a content in a downloaded file
            dec = 'utf-8' for general env
            dec = 'sjis'  for Excel on Win
            dec = 'cp932' for Excel with extended JP str on Win
    logging: True/False
        flag whether putting process log
    """
    try:
        if logging:
            print("HTTP GET", url)
        r = requests.get(url, stream=True)
        with open(filepath, 'w', encoding=enc) as f:
            f.write(r.content.decode(dec))
    except requests.exceptions.RequestException as error:
        print(error)


def download_all_csv(
        urls,
        filepathes,
        max_workers=10,
        enc="utf-8",
        dec="utf-8"):
    """
    Request some HTTP GET methods to the given urls (for REST API)
    and save each response as the csv file.
    (!! This method uses multi threading when calling HTTP GET requests
    and downloading files in order to improve the processing speed.)

    urls: list of strings
        valid urls for REST API
    filepathes: list of strings
        valid pathes to the destination file
    max_workers: int
        max number of working threads of CPUs within executing this method.
    enc: string
        encoding type for a content in a given url
    dec: string
        decoding type for a content in a downloaded file
            dec = 'utf-8' for general env
            dec = 'sjis'  for Excel on Win
            dec = 'cp932' for Excel with extended JP str on Win
    logging: True/False
    """
    func = functools.partial(download_csv, enc=enc, dec=dec)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(
            tqdm(executor.map(func, urls, filepathes), total=len(urls))
        )
        del results

