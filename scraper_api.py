import requests
import os

def get_response_for(query_term, results_per_page, page):
    # Request more results than needed
    url = 'https://unsplash.com/napi/search/photos?page={page}&per_page={results_per_page}&query={query_term}'
    response = requests.get(url)
     
    if response.status_code != 200:
        raise Exception(f'Error: {response.status_code}')
    else:
        return response.json()

def get_image_urls(data, results_per_page):
    results = data['results']
    img_urls = [x['urls']['raw'] for x in results if not (x['premium'] or x['plus'])]
    img_urls = [x.split('?')[0] for x in img_urls]

    # Limit the number of images after filtering
    img_urls = img_urls[:results_per_page]

    return img_urls

def download_images(img_urls, dest_dir='images', tag, max_download):
    success = 0
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for i, url in enumerate(img_urls):
        if success >= max_download:
            break
        img = requests.get(url)
        with open(f'{dest_dir}/{tag}_{i}.jpg', 'wb') as f:
            f.write(img.content)
            print(f'{tag}_{i}.jpg saved')
            success += 1

    return success

def main():
    start_page = 1
    query_term = input('Enter a search term: ')
    results_per_page = int(input('Enter the number of images to save: '))

if __name__ == '__main__':
    main()
