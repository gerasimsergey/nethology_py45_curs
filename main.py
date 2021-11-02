import os
from tokens import *
from yauploader import YaUploader
from vk import Vk
from tqdm import tqdm
import time
import json

def main():
    vk_id = input('Введите id пользователя VK, Enter используем по умолчанию begemot_korovin')
    ya_token = input('Введите токен Yandex.Disk, Enter используем по умолчанию')

    if len(ya_token) < 39:
        ya_token = yandex_token

    uploader = YaUploader(ya_token)

    vk = Vk(token= vk_token)
    if len(vk_id) > 0:
        vk.user_id = vk_id

    backup_dir = "mybackups" # Можно конечно и запрашивать
    photos = vk.get_photos()

    print(f"Выгружаем фото в Yandex: {len(photos)} фото")

    photo_log = []
    for photo in tqdm(photos):
        log_item = {
            "file_name": "34.jpg",
            "size": "z"
        }

        file_name = photo['file_name']
        url = photo['sizes']['url']

        log_item = {
            "file_name": file_name,
            "size": photo['size'], # !!! sizE
        }
        photo_log.append(log_item)

        uploader.backup_photo_from_url(url, file_name, backup_dir)
        time.sleep(0.01)

    print("Загрузка завершена")

    with open("upload.log", 'w', encoding='utf-8') as file:
        json.dump(photo_log, file)

if __name__ == '__main__':
    main()


