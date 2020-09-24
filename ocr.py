# -*- coding: utf-8 -*-
from aip import AipOcr


class baidu_orc(object):

    def __init__(self):
        """ 你的 APPID AK SK """
        self.APP_ID = '19619552'
        self.API_KEY = 'PfcjGMklICWSZNbdI11OQLBW'
        self.SECRET_KEY = 'rpNLYQpW1WdxqfrU7tLHa3K4VhvhpMMe'
        self.client = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    """ 读取图片 """

    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def get_captcha(self,filePath):
        image = self.get_file_content(filePath)

        """ 调用通用文字识别（高精度版） """
        self.client.basicAccurate(image);

        """ 如果有可选参数 """
        options = {}
        options["detect_direction"] = "false"
        options["probability"] = "false"

        """ 带参数调用通用文字识别（高精度版） """
        result = self.client.basicAccurate(image, options)['words_result'][0]['words']

        return result

if __name__ == '__main__':
    a = baidu_orc()
    result = a.get_captcha('math.jpg')
    print(result)