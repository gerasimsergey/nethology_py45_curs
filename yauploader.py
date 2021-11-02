import os
import requests
# from tokens import yandex_token


class YaUploader:
    BASE_URL = 'https://cloud-api.yandex.net/v1/disk'

    def __init__(self, yandex_token):
        self.token = yandex_token
        self.headers = {
            "Accept": "application/json",
            "Authorization": "OAuth " + self.token
        }

    def __get_url_to_upload(self, file_path):
        file_name =  os.path.basename(file_path)
        url = self.BASE_URL + '/resources/upload'
        headers = self.headers
        params = {'path': f'{file_name}', 'overwrite': 'true'}
        response = requests.get(url=url, headers=headers, params=params)
        return response.json().get('href')


    def upload(self, file_path):
        upload_url = self.__get_url_to_upload(file_path)
        with open(file_path, "rb") as file:
            response = requests.put(url=upload_url, data=file)
        response.raise_for_status()
        if response.status_code == 201:
            print('Done')

    # новые методы

    def disk_info(self):
        url = self.BASE_URL
        headers = self.headers
        response = requests.get(url, headers=headers)
        print(response.json())

    def _create_folder_if_not_exist(self, folder):
        url = self.BASE_URL + '/resources'
        headers = self.headers
        path_to_folder = f'/{folder}/'

        #  НЕ Перезаписываем
        params = {'path': path_to_folder, 'overwrite': 'false'}
        response = requests.put(url=url, headers=headers, params=params)


    def backup_photo_from_url(self, url, file_name, backupd_dir =''):
        upload_url = self.BASE_URL + '/resources/upload'
        if len(backupd_dir) > 0:
            # создаем если не существует
            self._create_folder_if_not_exist(backupd_dir)
            file_name = f"{backupd_dir}/{file_name}",
        params = {
            'path': file_name,
            'url': url
        }
        response = requests.post(url=upload_url, params=params, headers=self.headers)
        if response.status_code != 202:
            print(f'Ошибка на сервере. Код ошибки: {response.status_code}')