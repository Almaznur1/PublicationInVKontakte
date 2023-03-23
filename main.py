import requests
import os
from dotenv import load_dotenv
from random import randint


def fetch_random_comic():
    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()

    comics_count = response.json()['num']
    response = requests.get(
        f'https://xkcd.com/{randint(1, comics_count)}/info.0.json'
        )
    response = response.json()
    img_url = response['img']
    comment = response['alt']

    response = requests.get(img_url)
    with open(
        f'{os.path.dirname(os.path.abspath(__file__))}\\comics.png', 'wb'
            ) as img:
        img.write(response.content)
    return comment


def get_wall_upload_server(access_token):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': f'{access_token}',
        'v': '5.131',
        }
    response = requests.get(url, params=params)
    response.raise_for_status()
    upload_url = response.json()['response']['upload_url']
    return upload_url


def upload_on_wall(access_token, upload_url):
    params = {
        'access_token': f'{access_token}',
        'v': '5.131',
        }
    with open(f'{os.path.dirname(os.path.abspath(__file__))}\comics.png', 'rb') as img:
        file = {
            'photo': img,
        }
        response = requests.post(upload_url, params=params, files=file)
    response.raise_for_status()
    response = response.json()
    photo = {
        'server': response['server'],
        'photo': response['photo'],
        'hash': response['hash'],
        }
    return photo


def save_wall_photo(access_token, photo):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'access_token': f'{access_token}',
        'v': '5.131',
        'server': photo['server'],
        'photo': photo['photo'],
        'hash': photo['hash'],
        }
    response = requests.post(url, params=params)
    response.raise_for_status()
    response = response.json()
    photo_id = response['response'][0]['id']
    photo_owner_id = response['response'][0]['owner_id']
    return photo_id, photo_owner_id


def post_on_wall(access_token, comment, photo_id, photo_owner_id, group_id):
    url = 'https://api.vk.com/method/wall.post'
    params = {
        'access_token': f'{access_token}',
        'v': '5.131',
        'owner_id': f'-{group_id}',
        'from_group': '0',
        'attachments': f'photo{photo_owner_id}_{photo_id}',
        'message': comment,
        }
    response = requests.post(url, params=params)
    response.raise_for_status()


def main():
    load_dotenv()
    access_token = os.environ['VK_ACCESS_TOKEN']
    group_id = os.environ['GROUP_ID']

    comment = fetch_random_comic()
    upload_url = get_wall_upload_server(access_token)
    photo = upload_on_wall(access_token, upload_url)
    photo_id, photo_owner_id = save_wall_photo(access_token, photo)
    post_on_wall(access_token, comment, photo_id, photo_owner_id, group_id)
    os.remove(f'{os.path.dirname(os.path.abspath(__file__))}\\comics.png')


if __name__ == '__main__':
    main()
