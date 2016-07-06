# coding: utf8

from simple_load_test import make_data, batch_request

HOST = 'http://webservice.webxml.com.cn'

def get_getWeatherbyCityName(concurrent_num):
    url = HOST + "/WebServices/WeatherWebService.asmx/getWeatherbyCityName"
    params = {
        'theCityName': ("广州","深圳"),
    }
    reqs = make_data(params)
    batch_request(url, reqs, method='GET', workers_num=concurrent_num)

def post_getWeatherbyCityName(concurrent_num):
    url = HOST + "/WebServices/WeatherWebService.asmx/getWeatherbyCityName"
    params = {
        'theCityName': ("广州","深圳"),
    }
    reqs = make_data(params)
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    batch_request(url, reqs, headers, method='POST', workers_num=concurrent_num)


if __name__ == '__main__':
    get_getWeatherbyCityName(2)
    post_getWeatherbyCityName(3)
