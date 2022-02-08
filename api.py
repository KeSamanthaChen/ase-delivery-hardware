import requests
from requests import Session


hostname = 'ec2-3-70-186-30.eu-central-1.compute.amazonaws.com'
port = 10789
hostUrl = 'http://' + hostname + ':' + str(port)


session = requests.Session()


params = {
    'mode': 'cors',
    'cache': 'no-cache',
    'credentials': 'include',
    'withCredentials': 'true',
    'redirect': 'follow',
    'referrerPolicy': 'origin-when-cross-origin'
}


def httpRequest(method, url, params, headers='', content='', auth=''):
    if method == 'GET':
        res = session.get(url, params=params)
        return res
    elif method == 'POST':
        if auth == '':
            res = session.post(url, params=params, headers=headers, json=content)
        else:
            res = session.post(url, params=params, headers=headers, auth=auth)
        return res
    elif method == 'PUT':
        if auth == '':
            res = session.put(url, params=params, headers=headers, json=content)
        else:
            res = session.put(url, params=params, headers=headers, auth=auth)
        return res
    else:
        raise ValueError('Method Not Found')


def getBaseHeaders(xsrf_token):
    return {
        'Content-Type': "application/json",
        'X-XSRF-TOKEN': xsrf_token
    }


def getXSRFToken():
    r = httpRequest('GET', hostUrl + '/api/auth/csrf', params)
    print('xsrf: ', r.status_code)
    #1. Check response status and return the xsrf token or throw an exception
    if r.status_code == requests.codes.ok:
        return r.cookies['XSRF-TOKEN']
    else:
        r.raise_for_status()


#get jwt
def auth(xsrf_token):
    r = httpRequest(
        'POST',
        hostUrl + '/api/auth',
        params,
        #2. Include the base headers
        headers=getBaseHeaders(xsrf_token),
        #3. use basic auth
        auth=('Box', 'someStrongPassword')
    )
    print('jwt authStatusCode=', r.status_code)
    #4. Check response status and return the jwt token or throw exceptioni
    if r.status_code == requests.codes.ok:
        return r.cookies['jwt']
    else:
        r.raise_for_status()


def auth_box(content):
    r = httpRequest(
        'POST',
        hostUrl + '/api/delivery/boxes/box/auth',
        params,
        #5. Include the base header
        headers=getBaseHeaders(session.cookies['XSRF-TOKEN']),
        #6. add the request body
        content=content
    )
    print('Status code auth box', r.status_code)
    #7. Check response status and return project or throw an exception
    if r.status_code == requests.codes.ok:
        # return r.json()
        return r.text
    else:
        r.raise_for_status()


def update_state(content):
    r = httpRequest(
        'PUT',
        hostUrl + '/api/delivery/boxes/close',
        params,
        #5. Include the base header
        headers=getBaseHeaders(session.cookies['XSRF-TOKEN']),
        #6. add the request body
        content=content
    )
    print('Status code update state', r.status_code)
    #7. Check response status and return project or throw an exception
    if r.status_code == requests.codes.ok:
        return r.text
    else:
        r.raise_for_status()


# token = getXSRFToken()
# jwt = auth(token)
# res = auth_box({'box_id': '61eedcdb818c905a54c2128a', 'rfid':'132323'})
# print(res)
# res = update_state({"box_id": "61eedcdb818c905a54c2128a", "box_state":"closed"})
# print(res)