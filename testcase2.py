# coding: utf8

from simple_load_test import *

HOST = 'http://localhost:3000'
REQS_TOTAL_COUNT = 1

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
    REQS_TOTAL_COUNT = len(token_list)
    return tuple(token_list)

def post_weapon_fire():
    url = HOST + "/api/games/weapon_fire.json"
    reqs, headers = weapon_fire_params()
    batch_request(url, reqs, headers=headers, method='POST', reqs_total_count=REQS_TOTAL_COUNT, workers_num=REQS_TOTAL_COUNT)

def weapon_fire_params():
    params = {
        'token': get_tokens(),
        'robot_id': (1,2,3),
        'bullets_type': (1,2,3,4),
        'speed': (20,30),
        'frequence': (5,8,10)
    }
    reqs = make_data(params)
    headers = {"content-type": "application/json"}
    return reqs, headers


if __name__ == '__main__':
    post_weapon_fire()
