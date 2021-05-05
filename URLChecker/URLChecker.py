import requests
import argparse
import re
from multiprocessing import Pool


def main():

    args = argparse.ArgumentParser()
    path = None

    args.add_argument('-path', '--path', help='Wordlist to parse', default=None, type=str)
    args.add_argument('-u', '--url', help='Url to search if valid', default=None, type=str)
    args.add_argument('-t', '--threads', help='Amount of threads to use, default: 1, max 200', default=1, type=int)
    
    args = args.parse_args()
    urls = []

    if args.threads > 0 and args.threads < 201:
        threads = args.threads
    else:
        raise ValueError('Invalid amount of threads specified')
        exit(0)
    if args.path:
        try:
            with open(args.path, 'r') as f:
                for line in f:
                    url = line.replace('\n', '').replace('\r','')
                    if re.match(r'^http(s)?://www\..+\.(com|net|org)$', url):
                        urls.append(url)
                    else:
                        if not re.match(r'\.(com|net|org)', url):
                            urls.append('https://www.'+url)
                        else:
                            urls.append(f'https://www.{url}.com')
        except OSError as e:
            print(f'Unable to locate file path {path}')
            exit(1)

    elif args.url:
        if re.match(r'^http(s)?://www\..+\.(com|net|org)$', args.url):
            urls.append(args.url)
        else:
            urls.append(f'https://www.{args.url}.com')
    else:
        raise ValueError('No url or list specified')
    
    if args.path:
        pool = Pool(processes=threads)
        pool.map(connect, urls)
        pool.close()
        pool.join()
    else:
        connect(urls[0])


def connect(url):
    try:
        request = requests.get(url, timeout=5)
    except ConnectionError:
        with open('invalid-urls', 'a') as f:
            f.writelines(['\n'+url])
        return
    if request.status_code == 200:
        print(f'{url} is valid')
        content_length = len(request.content)
        print(f'Content-Length: {content_length}')
        with open('valid-urls', 'a') as f:
            f.writelines(['\n'+url, f'\nContent-Length: {content_length}'])
    else:
        with open('invalid-urls', 'a') as f:
            f.writelines(['\n'+url])


if __name__ == '__main__':
    main()
