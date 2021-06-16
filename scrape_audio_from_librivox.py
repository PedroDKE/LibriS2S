# -*- coding: utf-8 -*-
import os
import argparse
import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='A program to download all the chapters in a given librivox URL.')
parser.add_argument("--save_dir",
                    default="./chapters",
                    help='directory to save the downloaded chapters. If the directory does not exist it will be made.',
                    required=False,
                    type=str)

parser.add_argument("--url",
                    help='URL to audiobook.',
                    required=True,
                    type=str)

args = parser.parse_args()

page = requests.get(args.url)
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find_all(class_='chapter-name')
hrefs = []
for c in results:
    hrefs.append(c['href'])
print('found {} chapters to download'.format(len(hrefs)))

if not os.path.exists(args.save_dir):
    os.makedirs(args.save_dir)
    print('made new directory at:',args.save_dir)

for audio in hrefs:
    audio_path = args.save_dir+'/'+audio.split('/')[-1][:-3]+'wav'
    print('writing {} to:'.format(audio),audio_path)
    file = requests.get(audio)
    with open(audio_path, 'wb') as f:
        f.write(file.content)
