# coding: utf8

from simple_load_test import *

HOST = 'http://localhost:3000'
CONCURRENT_NUM = 1

def login(user, pwd):
    print 'login user: %s' % user
    uri = HOST + "/api/users/login.json"
    payload = {
        'login': user,
        'password': pwd
    }
    response = requests.post(uri, data=payload)
    resp_json = response.json()
    assert resp_json['status'] == 0
    token = resp_json['token']
    print 'login token: %s' % token
    return token

def get_tokens():
    accounts_list = [
        {'user': 'test1@debugtalk.com', 'password': '123456'},
        {'user': 'test2@debugtalk.com', 'password': '123456'},
    ]
    token_list = []
    for account in accounts_list:
        print account
        token = login(
            account['user'],
            account['password']
        )
        token_list.append(token)
    global CONCURRENT_NUM
    CONCURRENT_NUM = len(token_list)
    return tuple(token_list)

def post_weapon_fire():
    url = HOST + "/api/games/weapon_fire.json"
    reqs, headers = weapon_fire_params()
    config = {
        "headers": headers,
        "method": "POST",
        "expected": "'\"status\":0' in response"
    }
    batch_request(url, reqs, config=config, workers_num=CONCURRENT_NUM)

def weapon_fire_params():
    params = {
        'token': get_tokens(),
        'robot_id': (1,3,5,7,9),
        'bullets_type': (1,2,3),
        'speed': (20,30),
        'frequence': (1,2)
    }
    reqs = make_data(params)
    headers = {"content-type": "application/json"}
    return reqs, headers


if __name__ == '__main__':
    post_weapon_fire()
