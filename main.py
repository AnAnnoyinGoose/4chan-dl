#!/env/bash python3

import requests
import json
import tqdm
import os
import time
import sys
import threading
import queue

# the url_ of the 4chan API
url = 'https://a.4cdn.org/gif/threads.json'

# the folder_ where the files will be downloaded
folder = '4chan/gif/'

# the program will create a folder_ for each thread
# the folder_ will be named after the thread number

def download(url_, folder_):
    # the name of the file
    file = url_.split('/')[-1]
    # the path of the file
    path = folder_ + file
    # if the file doesn't exist
    if not os.path.isfile(path):
        # download the file
        r = requests.get(url_, stream=True)
        # the total size of the file
        total_size = int(r.headers.get('content-length', 0))
        # the size of the file that has been downloaded
        downloaded = 0
        # the block size
        block_size = 1024
        # the mode of the file
        mode = 'wb'
        # if the file already exists
        if os.path.isfile(path):
            # the mode of the file
            mode = 'ab'
            # the size of the file that has been downloaded
            downloaded = os.path.getsize(path)
        # open the file
        with open(path, mode) as f:
            # for each block in the file
            for data in tqdm.tqdm(r.iter_content(block_size), total=total_size, unit='B', unit_scale=True, desc=file):
                # write the block to the file
                downloaded += len(data)
                f.write(data)
        # if the file is empty
        if os.path.getsize(path) == 0:
            # delete the file
            os.remove(path)

def get_threads():
    # get the json data
    r = requests.get(url)
    # parse the json data
    data = json.loads(r.text)
    # the threads
    threads = []
    # for each page in the json data
    for page in data:
        # for each thread in the page
        for thread in page['threads']:
            # the thread number
            number = thread['no']
            # the thread url_
            thread_url = 'https://boards.4chan.org/gif/thread/' + str(number)
            # the thread folder_
            thread_folder = folder + str(number) + '/'
            # if the thread folder_ doesn't exist
            if not os.path.isdir(thread_folder):
                # create the thread folder_
                os.mkdir(thread_folder)
            # the thread
            thread = {'number': number, 'url_': thread_url, 'folder_': thread_folder}
            # add the thread to the threads
            threads.append(thread)
    # return the threads
    return threads

def get_files(thread):
    # the thread number
    number = thread['number']
    # the thread url_
    thread_url = thread['url_']
    # the thread folder_
    thread_folder = thread['folder_']
    # the thread url_
    thread_url = 'https://a.4cdn.org/gif/thread/' + str(number) + '.json'
    # get the json data
    r = requests.get(thread_url)
    # parse the json data
    data = json.loads(r.text)
    # the files
    files = []
    # for each post in the json data
    for post in data['posts']:
        # if the post has a file
        if 'filename' in post:
            # the file url_
            file_url = 'https://i.4cdn.org/gif/' + str(post['tim']) + post['ext']
            # add the file url_ to the files
            files.append(file_url)
    # return the files
    return files

def submain():
    # the threads
    threads = get_threads()
    # for each thread
    for thread in threads:
        # the thread number
        number = thread['number']
        # the thread url_
        thread_url = thread['url_']
        # the thread folder_
        thread_folder = thread['folder_']
        # the files
        files = get_files(thread)
        # for each file
        for file in files:
            # download the file
            download(file, thread_folder)
        # wait 1 second
        time.sleep(1)

def run():
    # while the program is running
    while True:
        # run the program
        submain()
        # wait 10 seconds
        time.sleep(10)

def start():
    #     create 2 threads
    for i in range(2):
        # create a thread
        thread = threading.Thread(target=run)
        # start the thread
        thread.start()
def stop():
    # exit the program
    sys.exit()

def main():
    # the threads
    threads = queue.Queue()
    # create a thread
    thread = threading.Thread(target=start)
    # start the thread
    thread.start()
    # add the thread to the threads
    threads.put(thread)
    # while the program is running
    while True:
        # the input
        i = input()
        # if the input is 'stop'
        if i == 'stop':
            # stop the program
            stop()
            # break
            break
    # while the threads aren't empty
    while not threads.empty():
        # get the thread
        thread = threads.get()
        # join the thread
        thread.join()

if __name__ == '__main__':
    main()

