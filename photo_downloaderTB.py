from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import requests
import os
import re


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
        for special_action in special_action_data:
            actions_list[special_action['sp_num']] = special_action['sp_name']
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
    # 选择监管所
    division = 'TB'
    divisions = {'SL': '狮岭', 'YH': '裕华', 'TB': '炭步'}
    # 取得专项行动列表
    action_list = CosDownloader.get_actions_list(division)
    action_list_string = ''
    i = 3
    confirm = False
    actions_dict = {'1': 'all', '2': ''}
    # 组装显示的文字
    for action_num in action_list:
        action_list_string = action_list_string + str(i) + '、' + action_num + ' : ' + action_list[action_num] + '\n'
        actions_dict[str(i)] = action_num
        i += 1
    # 输出提示
    print('***便捷版照片下载器（' + divisions[division] + '所专用）***')
    while not confirm:  # 输入出错时再次输入的循环
        action_index = input('请选择下载范围(仅输入数字)：\n'
                             '1、全部照片\n'
                             '2、仅日常监管照片\n'
                             '（以下为专项行动）\n'
                             + action_list_string)
        try:
            action = actions_dict[action_index]
            confirm = True  # 输入有效后中止循环
            c = CosDownloader()
            c.download(c.get_action_photos(division, action))
            k = input(u'完成，按回车键退出。')
        except KeyError:
            print('输入有误，请重新输入，或直接关闭本软件。')

