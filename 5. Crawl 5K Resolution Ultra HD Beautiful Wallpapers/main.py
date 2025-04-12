# -*- coding:utf-8 -*-

import requests
from filetype import guess
from os import rename
from os import makedirs
from os.path import exists
import json
from contextlib import closing

# Set the User-Agent header to mimic a browser request
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}

def get_photo_type():
    """
    Fetch the types of wallpapers that can be crawled
    :return: JSON response containing wallpaper types
    """
    url = "https://service.paper.meiyuan.in/api/v2/columns"
    res = requests.get(url=url, headers=headers, verify=False)
    res_json = json.loads(res.text)
    return res_json

def down_load(file_url, file_full_name, now_photo_count, all_photo_count):
    """
    Download a file from a URL and save it locally
    :param file_url: URL of the file to download
    :param file_full_name: Full path to save the downloaded file
    :param now_photo_count: Current photo count
    :param all_photo_count: Total number of photos to download
    :return: None
    """
    # Start downloading the image
    with closing(requests.get(file_url, headers=headers, stream=True)) as response:
        chunk_size = 1024  # Maximum size of each request
        content_size = int(response.headers['content-length'])  # Total size of the file
        data_count = 0  # Current size of data transferred
        with open(file_full_name, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                done_block = int((data_count / content_size) * 50)
                data_count = data_count + len(data)
                now_jd = (data_count / content_size) * 100
                print("\r %s: [%s%s] %d%% %d/%d" % (file_full_name, done_block * '█', ' ' * (50 - 1 - done_block), now_jd, now_photo_count, all_photo_count), end=" ")

    # After downloading the image, get the file type and add the appropriate extension
    file_type = guess(file_full_name)
    rename(file_full_name, file_full_name + '.' + file_type.extension)

def crawler_photo(type_id, photo_count):
    """
    Crawl photos of a specific type
    :param type_id: ID of the wallpaper type
    :param photo_count: Number of photos to download
    :return: None
    """
    url = 'https://service.paper.meiyuan.in/api/v2/columns/flow/{}?page=1&per_page={}'.format(type_id, photo_count)

    # Fetch the list of photos
    respond = requests.get(url, headers=headers, verify=False)
    photo_data = json.loads(respond.content)

    # Current photo count
    now_photo_count = 1

    # Total number of photos
    all_photo_count = len(photo_data)

    # Start downloading and saving 5K resolution wallpapers
    for photo in photo_data:
        # Create a folder to store the downloaded images
        if not exists('./' + str(type_id)):
            makedirs('./' + str(type_id))

        # Prepare the URL of the image to download
        file_url = photo['urls']['raw']

        # Prepare the name of the image file without extension
        file_name_only = file_url.split('/')
        file_name_only = file_name_only[len(file_name_only) - 1]

        # Prepare the full path to save the image locally
        file_full_name = './' + str(type_id) + '/' + file_name_only

        # Start downloading the image
        down_load(file_url, file_full_name, now_photo_count, all_photo_count)
        now_photo_count = now_photo_count + 1

if __name__ == '__main__':
    # Fetch the types of wallpapers that can be crawled
    res_json = get_photo_type()

    # Wallpaper type ID
    wall_paper_id = 0

    # Number of wallpapers to download
    wall_paper_count = 10

    # Create a string to display wallpaper types
    info_str = "Wallpaper Types:"
    for index, p_type in enumerate(res_json):
        info_str = info_str + " {} {}".format(index, p_type['langs']['zh-Hans-CN'])
        if index != len(res_json) - 1:
            info_str = info_str + ", "

    # Prompt the user to select a wallpaper type and validate the input
    while True:
        wall_paper_id = input(info_str + "\nEnter a number to select a 5K ultra HD wallpaper type: ")
        wall_paper_id = wall_paper_id.strip()
        wall_paper_id = int(wall_paper_id)
        if wall_paper_id >= len(res_json) or wall_paper_id < 0:
            continue
        else:
            break

    # Prompt the user to enter the number of wallpapers to download and validate the input
    while True:
        wall_paper_count = input("Enter the number of 5K ultra HD wallpapers to download: ")
        wall_paper_count = wall_paper_count.strip()
        wall_paper_count = int(wall_paper_count)
        if wall_paper_count <= 0:
            continue
        else:
            break

    # Start crawling 5K ultra HD wallpapers
    print("Downloading 5K ultra HD wallpapers, please wait...")
    crawler_photo(res_json[wall_paper_id]['_id'], wall_paper_count)
    print('\nDownload of 5K ultra HD wallpapers is complete. Wallpapers are located in the {} directory.'.format(res_json[wall_paper_id]['_id']))
