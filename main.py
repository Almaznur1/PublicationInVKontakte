import requests
from dotenv import load_dotenv
import os


def fetch_comics():  # step 1, 2
    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()
    response = response.json()
    img_url = response['img']
    comment = response['alt']
    print(comment)

    response = requests.get(img_url)
    with open('comix.png', 'wb') as img:
        img.write(response.content)


def get_wall_upload_server(access_token):  # step 8
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': f'{access_token}',
        'v': '5.131',
        }
    response = requests.get(url, params=params)
    response.raise_for_status()
    response = response.json()['response']
    upload_url = response['upload_url']
    album_id = response['album_id']
    user_id = response['user_id']
    return upload_url


def save_wall_photo(access_token, upload_url):  # step 9
    url = upload_url
    params = {
        'access_token': f'{access_token}',
        'v': '5.131',
        'group_id': '657767863',
        }
    with open('comix.png', 'rb') as file:
        url = upload_url
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
    response.raise_for_status()
    print(response.json())


def publish_comics(access_token):  # step 7 возращает имеющиеся группы
    url = 'https://api.vk.com/method/groups.get'
    params = {
        'access_token': f'{access_token}',
        'v': '5.131',
        }
    response = requests.get(url, params=params)
    response.raise_for_status()
    print(response.json())


def main():
    load_dotenv()
    access_token = os.environ['VK_ACCESS_TOKEN']

    upload_url = get_wall_upload_server(access_token)
    save_wall_photo(access_token, upload_url)


if __name__ == '__main__':
    main()
