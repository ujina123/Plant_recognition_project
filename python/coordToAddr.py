import requests

kakao_key = ""

def coordToAddr(lng, lat):
    url = 'https://dapi.kakao.com/v2/local/geo/coord2address.json'
    headers = {"Authorization" : f"KakaoAK {kakao_key}"}
    params = {'x' : lng, 'y' : lat}
    res = requests.get(url, params=params, headers=headers)
    if res.status_code != 200:
        return
    addr = res.json()['documents'][0]['address']['address_name']
    return addr
