from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import requests
import os
import re
import sys


class CosDownloader:

    def __init__(self):
        self.client = self.initial_cos_client()
        self.actions_list = {}

    @staticmethod
    def initial_cos_client():
        secret_id = 'AKIDWt55sQDlZ9VaPyrL7csra3GF2ZqyMWv6'      # 替换为用户的 secretId
        secret_key = '4uWt1uYw4wXsxlJabMr53kBLxJPFp9D2'      # 替换为用户的 secretKey
        region = 'ap-guangzhou'     # 替换为用户的 Region
        token = ''                  # 使用临时密钥需要传入 Token，默认为空，可不填
        scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
        config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
        # 2. 获取客户端对象
        return CosS3Client(config)

    def download(self, photos_keys_dict):
        root_dir = os.getcwd()
        print(u'Root dir is ' + root_dir)
        for corporation_name_with_id in photos_keys_dict:
            cos_key = photos_keys_dict[corporation_name_with_id]
            dirs_list = cos_key.split('/')
            for to_be_created_dir in dirs_list:
                if 'jpg' not in to_be_created_dir:
                    try:
                        os.mkdir(to_be_created_dir)
                        os.chdir(to_be_created_dir)
                    except FileExistsError:
                        # print(to_be_created_dir + ' already exists, go into in directly...')
                        os.chdir(to_be_created_dir)
                else:
                    corporation_name = re.sub(r'\^\w*', "", corporation_name_with_id)  # 取得企业真实名称
                    try:
                        os.mkdir(corporation_name)
                        os.chdir(corporation_name)
                    except FileExistsError:
                        os.chdir(corporation_name)
                    target_file = os.getcwd() + '/' + to_be_created_dir
                    if os.path.isfile(target_file):
                        print(to_be_created_dir + u' 已经存在')
                        pass
                    else:
                        print(u'正在下载：' + to_be_created_dir)
                        response = self.client.get_object(
                            Bucket='aic-1253948304',
                            Key=cos_key,
                        )
                        response['Body'].get_stream_to_file(target_file)
            os.chdir(root_dir)

    @staticmethod
    def get_actions_list(div='SL'):
        r = requests.get('https://www.shilingaic.cn/index.php/api/special_action/' + div)
        special_action_json = r.json()
        special_action_data = special_action_json['data']
        actions_list = {}
        for action in special_action_data:
            actions_list[action['sp_num']] = action['sp_name']
        return actions_list

    @staticmethod
    def get_action_photos(div='SL', action='all'):
        r = requests.get('https://www.shilingaic.cn/index.php/api/photos/' + div + '/' + action)
        photos_json = r.json()
        photos_data = photos_json['data']
        photos_keys = {}
        for photo in photos_data:
            photos_keys[photo['corporation_name'] + '^' + str(photo['id'])] = (photo['link'])
            # photos_keys.append(photo['link'])
        return photos_keys


if __name__ == '__main__':
    c = CosDownloader()
    # print(c.get_action_photos_dict())
    # print(c.get_action_photos('sl', '2018-06'))
    c.download(c.get_action_photos('SL'))
    k = input(u'按任意键退出。')
