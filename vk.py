import requests
import time
from tqdm import tqdm


class Vk:
    VERSION = '5.131'
    URL = 'https://api.vk.com/method/'

    def __init__(self, token):
        self.items_names = []
        self._user_id = None
        self.token = token
        self.params = {
            'access_token': self.token,
            'v': self.VERSION
        }
        # self.visitor = requests.get(self.URL + 'stats.trackVisitor', self.params)
        owner_id = requests.get(self.URL + 'users.get', self.params)
        self.owner_id = owner_id.json()['response'][0]['id']


    @property
    def user_id(self):
        if self._user_id is None:
            return "begemot_korovin"
        else:
            return self._user_id

    def get_name_for_item(self, item):

        likes = item['likes']['count']
        # if likes in self.items_names:
        #     name = f"{likes}_{item['id']}"
        # else:
        #     name = likes
        # self.items_names.append(name)

        name = f"{likes}"

        return  (f"{name}.jpg")

    def get_photos(self, photos_count = 5):
        def get_max_size(size_list):
            newlist = sorted(size_list, key=lambda k: (k['width'], k['height']))
            return newlist[0]

        photos_params = {
            'owner_id': self.owner_id,
            'album_id': 'profile',
            'rev': 0,
            'extended': 1,
            'count': photos_count
        }

        photos_url = self.URL + 'photos.get'
        params = {**self.params, **photos_params}
        response = requests.get(photos_url, params).json()

        items = response['response']['items']
        items_to_save = []

        print('Получаем и обрабатываем фотографии профиля ...')

        for i in tqdm(items):
            sizes_count = len(i['sizes'])
            if sizes_count > 1:
                size_item = get_max_size(i['sizes'])

                i['sizes'] = size_item
                i['size'] = f"{size_item['height']}x{size_item['width']}"

                i['file_name'] = self.get_name_for_item(i)
                items_to_save.append(i)
                time.sleep(0.01)
        print('Фото получены ...')

        return items_to_save


    # для тестирования
    def check_user(self, user_id):
        result = None
        url = self.URL + 'users.get'
        params = self.params
        params['user_ids'] = user_id
        try:
            response = requests.get(
                url,
                params,
            )
            if response.status_code == 200:
                result = True
            else:
                print('Response HTTP Status Code: {status_code}'.format(
                    status_code=response.status_code))
                print('Response HTTP Response Body: {content}'.format(
                content=response.content))

        except requests.exceptions.RequestException:

            print('HTTP Request failed')
            print('Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))
            print('Response HTTP Response Body: {content}'.format(
                content=response.content))

            result = False

        return result