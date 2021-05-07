from bs4 import BeautifulSoup
import requests
import re
import html


extensions = ('.html', '.htm', '.php', '.asp', '.aspx')
media_types = ('.mp3', '.mp4')
urls = []


def download(r, recurse):
    global recursion
    global extensions
    global urls
    if recurse == 0:
        return

    soup = BeautifulSoup(r.content, 'html.parser')
    base_url = r.url
    
    print(f'Scanning: {base_url}')

    for a in soup.find_all('a', href=True):
        url = clean_url(base_url, a['href'])
        if url == '':
            continue
        if url not in urls:
            urls.append(url)
        if is_downloadable(r.headers) or is_media(url):
            path = html.unescape(url[url.rindex('/')+1:]).replace('%20', ' ')
            with open(path, 'wb') as f:
                f.write(requests.get(url).content)
                print(f"Downloaded {path}")
        elif url != base_url:
            download(requests.get(url), recurse-1)

def clean_url(base_url, url):
    if url.startswith('/'):
        url = base_url + url[1:]
    else:
        url = base_url + url
    if '?' in url:
        url = url[:url.rindex('?')]
    return url
        

def is_downloadable(header):
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True


def is_webpage(r):
    try:
        if url[url.rindex('.'):] in extensions:
            return True
    except ValueError:
        return False


def is_media(url):
    try:
        if url[:-1] == '/':
            return True
        elif url[url.rindex('.'):] in media_types:
            return True
        else:
            return False
    except ValueError:
        return False