# coding: utf8

from simple_load_test import *

HOST = 'http://webservice.webxml.com.cn'
CONCURRENT_NUM = 2

def get_getWeatherbyCityName():
    url = HOST + "/WebServices/WeatherWebService.asmx/getWeatherbyCityName"
    params = {
        'theCityName': ("广州","深圳"),
    }
    reqs = make_data(params)
    batch_request(url, reqs, method='GET', workers_num=CONCURRENT_NUM)

def post_getWeatherbyCityName():
    url = HOST + "/WebServices/WeatherWebService.asmx/getWeatherbyCityName"
    params = {
        'theCityName': ("广州","深圳"),
    }
    reqs = make_data(params)
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    batch_request(url, reqs, headers, method='POST', workers_num=CONCURRENT_NUM)


if __name__ == '__main__':
    # get_getWeatherbyCityName()
    post_getWeatherbyCityName()
