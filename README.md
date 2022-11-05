# 4chan-dl
## Disclaimer: **THIS IS PROBABLY THE WORST CODE YOU WILL EVER SEE!**

## Usage
Download the requirements:
```bash
pip i -r requirements.txt
```
Run the script:
```bash
py main.py
# or
python3 main.py
```
# How does it work?
The script will crawl through the https://a.4cdn.org/gif/threads.json file
```python
:12 <- line number
url = 'https://a.4cdn.org/gif/threads.json'
...
:55 
def get_threads():
    r = requests.get(url)
    data = json.loads(r.text)
    threads = []
    
    for page in data:
        for thread in page['threads']:
            number = thread['no']
            thread_folder = folder + str(number) + '/'
            if not os.path.isdir(thread_folder):
                os.mkdir(thread_folder)
            thread = {'number': number, 'folder_': thread_folder}
            threads.append(thread)
    return threads
```
and it will get the thread number.
From the thread number it will create a folder in a 4chan/gif/ directory.

Then with the thread number it will get the threads .json file eg. https://a.4cdn.org/gif/thread/123456789.json
```python
:81
def get_files(thread):
    number = thread['number']
    thread_url = 'https://a.4cdn.org/gif/thread/' + str(number) + '.json'
    r = requests.get(thread_url)
    data = json.loads(r.text)
    files = []
    for post in data['posts']:
        if 'filename' in post:
            file_url = 'https://i.4cdn.org/gif/' + str(post['tim']) + post['ext']
            files.append(file_url)
    return files
```
tim is the file name and ext is the file extension.

Then it will download the files to the thread folder.
```python
:20
def download(url_, folder_):
    file = url_.split('/')[-1]
    path = folder_ + file
    if not os.path.isfile(path):
        r = requests.get(url_, stream=True)
        total_size = int(r.headers.get('content-length', 0))
        downloaded = 0
        block_size = 1024
        mode = 'wb'
        if os.path.isfile(path):
            mode = 'ab'
            downloaded = os.path.getsize(path)
        with open(path, mode) as f:
            for data in tqdm.tqdm(r.iter_content(block_size), total=total_size, unit='B', unit_scale=True, desc=file):
                downloaded += len(data)
                f.write(data)
        if os.path.getsize(path) == 0:
            os.remove(path)
```

## TODO
- [ ] Add support for other boards
- [ ] Add support for other file types
- [ ] Better code
- [x] Better README.md (kinda)
- [ ] Better comments
- [ ] Better everything lol
