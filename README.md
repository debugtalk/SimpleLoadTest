## Install requirements

```bash
$ pip install gevent
$ pip install requests
```

## make GET load test

Here is a `HTTP GET` example.

```
GET /WebServices/WeatherWebService.asmx/getWeatherbyCityName?theCityName=string HTTP/1.1
Host: webservice.webxml.com.cn
```

And its response:

```
HTTP/1.1 200 OK
Content-Type: text/xml; charset=utf-8
Content-Length: length

<?xml version="1.0" encoding="utf-8"?>
<ArrayOfString xmlns="http://WebXml.com.cn/">
  <string>string</string>
  <string>string</string>
</ArrayOfString>
```

To test this webservice, we can write test like this:

```python
def get_getWeatherbyCityName(concurrent_num):
    url = HOST + "/WebServices/WeatherWebService.asmx/getWeatherbyCityName"
    params = {
        'theCityName': ("广州","深圳"),
    }
    reqs = make_data(params)
    batch_request(url, reqs, method='GET', workers_num=concurrent_num)
```

## make POST load test

Here is a `HTTP POST` example.

```
POST /WebServices/WeatherWebService.asmx/getWeatherbyCityName HTTP/1.1
Host: webservice.webxml.com.cn
Content-Type: application/x-www-form-urlencoded
Content-Length: length

theCityName=string
```

And its response:

```
HTTP/1.1 200 OK
Content-Type: text/xml; charset=utf-8
Content-Length: length

<?xml version="1.0" encoding="utf-8"?>
<ArrayOfString xmlns="http://WebXml.com.cn/">
  <string>string</string>
  <string>string</string>
</ArrayOfString>
```

To test this webservice, we can write test like this:

```python
def post_getWeatherbyCityName(concurrent_num):
    url = HOST + "/WebServices/WeatherWebService.asmx/getWeatherbyCityName"
    params = {
        'theCityName': ("广州","深圳"),
    }
    reqs = make_data(params)
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    batch_request(url, reqs, headers, method='POST', workers_num=concurrent_num)
```

## Run tests

Once testcase.py is done, start rolling!

```bash
$ python testcase.py
```
