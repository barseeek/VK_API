import requests


def save_photo(url, filename, params={}):
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def main():
    response = requests.get("https://xkcd.com/353/info.0.json")
    comics_data = response.json()
    save_photo(comics_data["img"], 'python.png')
    print(comics_data["alt"])


if __name__ == '__main__':
    main()