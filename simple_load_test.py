# coding: utf8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from gevent import monkey; monkey.patch_all()
import gevent
from gevent.queue import Queue

from time import time, sleep
from datetime import datetime
import json
import requests
import itertools
import random


def make_data(data):
    ''' create Cartesian product
    params:
        data = {
            "imeis":("a", "b"),
            "page":(1, 2),
            "count":(20,),
        }
    output:
        {'count': 20, 'imeis': 'a', 'page': 1}
        {'count': 20, 'imeis': 'a', 'page': 2}
        {'count': 20, 'imeis': 'b', 'page': 1}
        {'count': 20, 'imeis': 'b', 'page': 2}
    '''
    for key, items in data.iteritems():
        if isinstance(items, (int, float, str, unicode, dict, list)):
            data[key] = (items, )
    keys = data.keys()
    for values in itertools.product(*data.values()):
        yield dict(zip(keys, values))

def request_worker(url, reqs_queue, config, worker=0):
    headers = config["headers"]
    method = config["method"]
    interval_time = config["interval_time"]

    while not reqs_queue.empty():
        req = reqs_queue.get()
        start = time()
        print "worker %d --- %s request: %s time: %s\n%s\n" % (worker, method, url, datetime.now() , req)

        if method == 'GET':
            res = requests.get(url, headers=headers, params=req)
        elif method == 'POST':
            res = requests.post(url, headers=headers, data=req)
        else:
            raise "Only support GET and POST method!"

        print "elapsed time: %s" % (time()-start)
        print "response: \n%s\n" % res.text

        # check validation of response
        response = res.text
        valid_expression = config["expected"]
        assert eval(valid_expression) == True

        if interval_time is not None:
            sleep(interval_time)

        if not res.ok:
            print "Error! Status Code: %s" % res.status_code

def batch_request(url, reqs, config={}, workers_num=1):
    if "interval_time" not in config:
        config["interval_time"] = None

    if "headers" not in config:
        config["headers"] = {}
    elif "content-type" in config["headers"]:
        if config["headers"]["content-type"] == "application/json":
            reqs = [json.dumps(req).strip() for req in reqs]

    if "method" not in config:
        config["method"] = "POST"

    if "expected" not in config:
        config["expected"] = "True"

    reqs_queue = Queue()

    for req in reqs:
        reqs_queue.put_nowait(req)

    count = reqs_queue.qsize()

    workers = [gevent.spawn(request_worker, url, reqs_queue, config, worker=worker) for worker in range(workers_num)]
    start = time()
    # send requests at the same time
    gevent.joinall(workers)
    # Response.elapsed for a single request, offered by requests
    print "total requests number: %d" % (count)
    print "total elapsed time: %s\n" % (time()-start)
