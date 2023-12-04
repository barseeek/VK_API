import requests
from environs import Env
import random
from pathlib import Path


def check_vk_exception(decoded_response):
    if "error" in decoded_response:
        raise requests.exceptions.HTTPError(
            decoded_response["error"]["error_code"],
            decoded_response["error"]["error_msg"]
        )


def download_random_comics():
    response = requests.get("https://xkcd.com/info.0.json")
    response.raise_for_status()
    comics_num = random.randint(1, response.json()["num"])
    filename = '{0}.png'.format(comics_num)
    comics_response = requests.get(f"https://xkcd.com/{comics_num}/info.0.json")
    comics_response.raise_for_status()
    decoded_comics_response = comics_response.json()
    response = requests.get(decoded_comics_response['img'])
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)
    return filename, decoded_comics_response


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
    response.raise_for_status()
    decoded_response = response.json()
    check_vk_exception(decoded_response)
    return decoded_response.get("response").get("upload_url")


def save_photo_to_album(access_token, group_id, photo, hash, server):
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {
        'photo': photo,
        'group_id': group_id,
        'hash': hash,
        'server': server,
        'v': '5.199'
    }
    response = requests.get(
        "https://api.vk.com/method/photos.saveWallPhoto",
        headers=headers,
        params=params
    )
    response.raise_for_status()
    decoded_response = response.json()
    check_vk_exception(decoded_response)
    first_photo = decoded_response.get("response")[0]
    return first_photo.get("id"), \
        first_photo.get("owner_id")


def publish_photo_to_album(
        access_token,
        group_id,
        photo_id,
        owner_id,
        post_message
):
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {
        'owner_id': f'-{group_id}',
        'attachments': f'photo{owner_id}_{photo_id}',
        'message': post_message,
        'v': '5.199'
    }
    response = requests.get(
        "https://api.vk.com/method/wall.post",
        headers=headers,
        params=params
    )
    decoded_response = response.json()
    check_vk_exception(decoded_response)
    return decoded_response


def main():
    try:
        env = Env()
        env.read_env()
        vk_group_id = env.int("VK_GROUP_ID")
        vk_access_token = env.str("VK_ACCESS_TOKEN")
        filename, decoded_comics_response = download_random_comics()
        upload_url = get_upload_url(vk_access_token, vk_group_id)
        photo_params = upload_photo(upload_url, filename)
        photo_id, owner_id = save_photo_to_album(
            vk_access_token,
            vk_group_id,
            photo_params.get("photo"),
            photo_params.get("hash"),
            photo_params.get("server")
        )
        publish_photo_to_album(
            vk_access_token,
            vk_group_id,
            photo_id,
            owner_id,
            decoded_comics_response['alt']
        )
    finally:
        Path.unlink(filename)


if __name__ == '__main__':
    main()
