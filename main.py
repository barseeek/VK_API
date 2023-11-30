import requests
from environs import Env


def save_photo(url, filename, params={}):
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def upload_photo(url, filename):
    with open(filename, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
        return response.json()


def get_upload_url(access_token, group_id):
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {
        'group_id': group_id,
        'v': '5.199'
    }
    response = requests.get(
        "https://api.vk.com/method/photos.getWallUploadServer",
        headers=headers,
        params=params
    )
    return response.json().get("response").get("upload_url")


def save_photo_to_album(access_token, photo_data, group_id):
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {
        'photo': photo_data.get("photo"),
        'group_id': group_id,
        'hash': photo_data.get("hash"),
        'server': photo_data.get("server"),
        'v': '5.199'
    }
    response = requests.get(
        "https://api.vk.com/method/photos.saveWallPhoto",
        headers=headers,
        params=params
    )
    first_element_of_response = response.json().get("response")[0]
    return first_element_of_response.get("id"), \
        first_element_of_response.get("owner_id")


def publish_photo_to_album(access_token, photo_id, owner_id, post_message):
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {
        'owner_id': f'-{vk_group_id}',
        'attachments': f'photo{owner_id}_{photo_id}',
        'message': post_message,
        'v': '5.199'
    }
    response = requests.get(
        "https://api.vk.com/method/wall.post",
        headers=headers,
        params=params
    )
    return response.json()


def main(access_token, group_id):
    filename = 'python.png'
    comics_response = requests.get("https://xkcd.com/353/info.0.json")
    save_photo(comics_response.json()['img'], filename)
    upload_url = get_upload_url(access_token, group_id)
    photo_data = upload_photo(upload_url, filename)
    photo_id, owner_id = save_photo_to_album(
        access_token,
        photo_data,
        group_id
    )
    print(publish_photo_to_album(
        access_token,
        photo_id,
        owner_id,
        comics_response.json()['alt']
    ))


if __name__ == '__main__':
    env = Env()
    env.read_env()
    vk_group_id = env.int("VK_GROUP_ID")
    vk_access_token = env.str("VK_ACCESS_TOKEN")
    main(vk_access_token, vk_group_id)