import requests
from dotenv import load_dotenv
import os


def fetch_comics():
    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()
    response = response.json()
    img_url = response['img']
    comment = response['alt']
    print(comment)

    response = requests.get(img_url)
    with open('comix.png', 'wb') as img:
        img.write(response.content)


def get_wall_upload_server(access_token):
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
    print(upload_url, album_id, user_id, sep='\n')


def save_wall_photo(access_token):
    url = 'photos.saveWallPhoto'
    params = {
        'access_token': f'{access_token}',
        'v': '5.131',
        'group_id': '657767863',
        }
    response = requests.post(url, params=params)
    response.raise_for_status()



def publish_comics(access_token):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
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

    save_wall_photo(access_token)


if __name__ == '__main__':
    main()
