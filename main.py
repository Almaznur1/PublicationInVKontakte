import requests
import os
from dotenv import load_dotenv
from random import randint


def process_vk_api_response(response):
    if 'error' in response:
        raise requests.HTTPError(
            f'''Код ошибки: {response['error']['error_code']}
            Ошибка: {response['error']['error_msg']}'''
            )


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


def get_wall_upload_server(access_token, api_version):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': access_token,
        'v': api_version,
        }
    response = requests.get(url, params=params)
    response.raise_for_status()

    response = response.json()
    process_vk_api_response(response)

    upload_url = response['response']['upload_url']
    return upload_url


def upload_on_wall(access_token, upload_url, api_version):
    params = {
        'access_token': access_token,
        'v': api_version,
        }
    with open(f'{os.path.dirname(os.path.abspath(__file__))}\comics.png', 'rb') as img:
        file = {
            'photo': img,
        }
        response = requests.post(upload_url, params=params, files=file)
    response.raise_for_status()

    response = response.json()
    process_vk_api_response(response)

    server = response['server']
    photo = response['photo']
    hash = response['hash']
    return server, photo, hash


def save_wall_photo(access_token, server, photo, hash, api_version):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'access_token': access_token,
        'v': api_version,
        'server': server,
        'photo': photo,
        'hash': hash,
        }
    response = requests.post(url, params=params)
    response.raise_for_status()

    response = response.json()
    process_vk_api_response(response)

    photo_id = response['response'][0]['id']
    photo_owner_id = response['response'][0]['owner_id']
    return photo_id, photo_owner_id


def post_on_wall(
        access_token, comment, photo_id, photo_owner_id, group_id, api_version
        ):
    url = 'https://api.vk.com/method/wall.post'
    params = {
        'access_token': access_token,
        'v': api_version,
        'owner_id': f'-{group_id}',
        'from_group': '1',
        'attachments': f'photo{photo_owner_id}_{photo_id}',
        'message': comment,
        }
    response = requests.post(url, params=params)
    response.raise_for_status()

    process_vk_api_response(response.json())


def main():
    load_dotenv()
    access_token = os.environ['VK_ACCESS_TOKEN']
    group_id = os.environ['GROUP_ID']
    api_version = '5.131'

    comment = fetch_random_comic()
    upload_url = get_wall_upload_server(access_token, api_version)
    server, photo, hash = upload_on_wall(access_token, upload_url, api_version)
    photo_id, photo_owner_id = save_wall_photo(
        access_token, server, photo, hash, api_version
        )
    post_on_wall(
        access_token, comment, photo_id, photo_owner_id, group_id, api_version
        )
    os.remove(f'{os.path.dirname(os.path.abspath(__file__))}\\comics.png')


if __name__ == '__main__':
    main()
