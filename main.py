import requests


if __name__ == '__main__':
    url = 'https://he.122.gov.cn/m/mvehxh/getTfhdList'

    data = {
        'page': '0',
        'glbm': '130900000400',
        'hpzl': '02',
        'type': '0',
        'startTime': '2020-07-23',
        'endTime': '2020-09-23',
        'csessionid': '1',
    }

    res = requests.post(url=url,data=data)

    print(res.text)
