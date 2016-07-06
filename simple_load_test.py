# coding: utf8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from gevent import monkey; monkey.patch_all()
import gevent
from gevent.queue import Queue

from time import time
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

def request_worker(url, headers, tasks, method="POST", worker=0):
    while not tasks.empty():
        req = tasks.get()
        if method == 'GET':
            res = requests.get(url, headers=headers, params=req)
        elif method == 'POST':
            res = requests.post(url, headers=headers, data=req)
        else:
            raise "Only support GET and POST method!"
        print "%s request: %s time: %s\n%s\n" % (method, url, datetime.now() , req)
        print "response: \n%s" % res.text
        if not res.ok:
            print "Error! Status Code: %s" % res.text
        else:
            print "worker %d finished one request!\n" % worker

def batch_request(url, reqs, headers={}, method='POST', workers_num=1):
    if "content-type" in headers and headers["content-type"] == "application/json":
        reqs = [json.dumps(req).strip() for req in reqs]

    reqs = list(reqs) * workers_num

    tasks = Queue()
    for req in reqs:
        tasks.put_nowait(req)

    count = tasks.qsize()

    workers = [gevent.spawn(request_worker, url, headers, tasks, method=method, worker=worker) for worker in range(workers_num)]
    start = time()
    # send requests at the same time
    gevent.joinall(workers)
    # Response.elapsed for a single request, offered by requests
    print "total requests: %d" % (count)
    print "elapsed time: %s\n" % (time()-start)
