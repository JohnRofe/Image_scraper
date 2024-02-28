'''image scraper from Unsplash'''

import requests 
from bs4 import BeautifulSoup

def scrape_images(query_term, num_images):
    url = f'https://unsplash.com/s/photos/{query_term}'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    soup = soup.find('div', {'data-test': 'search-photos-route'})
    imgs = soup.find_all('img', {'itemprop':'thumbnailUrl'})
    links = [img['srcset'].split(' ')[-2] for img in imgs if 'premium' not in img['srcset']]

    # save as images
    saved_images = 0
    for i, link in enumerate(links):
        if saved_images >= num_images:
            break
        img = requests.get(link)
        with open(f'{query_term}_{i}.jpg', 'wb') as f:
            f.write(img.content)
            print(f'{query_term}_{i}.jpg saved')
            saved_images += 1

    if saved_images < num_images:
        print(f'Only {saved_images} images were available.')

def main():
    query_term = input('Enter a search term: ')
    num_images = int(input('Enter the number of images to save: '))
    scrape_images(query_term, num_images)

if __name__ == '__main__':
    main()

