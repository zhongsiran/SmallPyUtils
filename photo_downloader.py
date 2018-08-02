from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import requests
import os
import sys
import logging


class CosDownloader:

    def __init__(self):
        self.client = self.initial_cos_client()

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

    def download(self, resource):
        for key, file in resource:
            response = self.client.get_object(
                Bucket='aic-1253948304',
                Key=key,
            )

            response['Body'].get_stream_to_file( os.getcwd() + file)

    @staticmethod
    def get_resource(div='SL'):
        r = requests.get('https://www.shilingaic.cn/index.php/api/special_action/' + div)
        special_action_json = r.json()
        special_action_data = special_action_json['data']
        actions_list = {}
        for action in special_action_data:
            actions_list[action['sp_num']] = action['sp_name']
        print(actions_list)


if __name__ == '__main__':
    c = CosDownloader()
    c.get_resource()
