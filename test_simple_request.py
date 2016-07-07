# coding: utf8

from simple_load_test import make_data, batch_request

HOST = "http://webservice.webxml.com.cn"

def get_getWeatherbyCityName(concurrent_num):
    url = HOST + "/WebServices/WeatherWebService.asmx/getWeatherbyCityName"
    params = {
        'theCityName': ("广州","深圳"),
    }
    reqs = make_data(params)
    config = {
        "method": "GET"
    }
    batch_request(url, reqs, config=config, workers_num=concurrent_num)

def post_getWeatherbyCityName(concurrent_num):
    url = HOST + "/WebServices/WeatherWebService.asmx/getWeatherbyCityName"
    params = {
        'theCityName': ("广州","深圳"),
    }
    reqs = make_data(params)
    headers = {"content-type": "application/x-www-form-urlencoded"}
    config = {
        "headers": headers,
        "method": "POST"
    }
    batch_request(url, reqs, config=config, workers_num=concurrent_num)


if __name__ == '__main__':
    get_getWeatherbyCityName(2)
    post_getWeatherbyCityName(3)
