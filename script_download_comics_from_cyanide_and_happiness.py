import requests
import os
from bs4 import BeautifulSoup


os.makedirs('cyanide_and_happiness', exist_ok=True)

res = requests.get('http://explosm.net/comics/')
res.raise_for_status()
number_of_comics_to_download = int(input('How many comics would you like to download? '))
comics_downloaded = 0
while comics_downloaded < number_of_comics_to_download:
    soup = BeautifulSoup(res.text, 'html.parser')
    current_comic_number = int(soup.button['data-slug'].split('-')[1])
    comic_tag = soup.select('#main-comic')[0]
    comic_url = 'http:' + comic_tag.get('src')
    current_comic_file = requests.get(comic_url)
    comic_basename = os.path.basename(comic_url).split('.')[0]

    print(f'Downloading comic_{current_comic_number}_{comic_basename}')

    with open(os.path.join('cyanide_and_happiness', f"comic_{current_comic_number}_{comic_basename}.png"), 'wb') as file:
        for chunk in current_comic_file.iter_content(100000):
            file.write(chunk)
    print('Download complete!')
    comics_downloaded += 1

    prev = soup.find(attrs={'title': 'Oldest comic'})

    if 'disabled' not in prev['class']:
        previous_comic_url = soup.select('.nav-previous')[0]['href']
        previous_comic_num = previous_comic_url.split('/')[2]
    else:
        break

    res = requests.get(f'http://explosm.net/comics/{previous_comic_num}')
    res.raise_for_status()

print(f'Job complete! {comics_downloaded} comics downloaded successfully!')
