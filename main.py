import requests


def main():
    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()
    response = response.json()
    img_url = response['img']

    response = requests.get(img_url)
    with open('comix.png', 'wb') as img:
        img.write(response.content)


if __name__ == '__main__':
    main()
