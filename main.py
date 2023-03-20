import requests
from dotenv import load_dotenv
import os
from random import randint


def fetch_comics():  # step 1, 2
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
    with open('comix.png', 'wb') as img:
        img.write(response.content)
    return comment


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


def wall_upload(access_token, upload_url):  # step 9
    url = upload_url
    params = {
        'access_token': f'{access_token}',
        'v': '5.131',
        'group_id': '219393195',
        }
    with open('comix.png', 'rb') as file:
        url = upload_url
        files = {
            'photo': file,
        }
        response = requests.post(url, params=params, files=files)
    response.raise_for_status()
    response = response.json()
    photo = {
        'server': response['server'],
        'photo': response['photo'],
        'hash': response['hash'],
        }
    return photo


def save_wall_photo(access_token, photo):  # step 10
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


def wall_post(access_token, comment, photo_id, photo_owner_id):
    url = 'https://api.vk.com/method/wall.post'
    params = {
        'access_token': f'{access_token}',
        'v': '5.131',
        'owner_id': '-219393195',
        'from_group': '0',
        'attachments': f'photo{photo_owner_id}_{photo_id}',
        'message': comment,
        }
    response = requests.post(url, params=params)
    response.raise_for_status()


def get_groups(access_token):  # step 7 возращает имеющиеся группы
    url = 'https://api.vk.com/method/groups.get'
    params = {
        'access_token': f'{access_token}',
        'v': '5.131',
        'extended': '1',
        }
    response = requests.get(url, params=params)
    response.raise_for_status()


def main():
    load_dotenv()
    access_token = os.environ['VK_ACCESS_TOKEN']

    comment = fetch_comics()
    upload_url = get_wall_upload_server(access_token)
    photo = wall_upload(access_token, upload_url)
    photo_id, photo_owner_id = save_wall_photo(access_token, photo)
    wall_post(access_token, comment, photo_id, photo_owner_id)

    # get_groups(access_token)


if __name__ == '__main__':
    main()
