import json
import random
import time

try:
    import requests
    import schedule
except ModuleNotFoundError:
    from os import system
    system('pip install requests==2.23.0')
    system('pip install schedule==1.2.0')
    import requests
    import schedule


USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
    "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
]

DYNAMIC_DICT = {}

def get_random_useragent():
    return random.choice(USER_AGENTS)


def requests_get(url, headers=None, params=None):
    if headers is None:
        headers = {}
    headers = dict({
        'User-Agent': get_random_useragent()
    }, **headers)
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
    except Exception as e:
        return None
    return response


def requests_post(url, headers=None, params=None, data=None, json=None):
    if headers is None:
        headers = {}
    headers = dict({
        'User-Agent': get_random_useragent()
    }, **headers)
    try:
        response = requests.post(url, headers=headers, params=params, data=data, json=json, timeout=10)
    except Exception as e:
        return None
    return response


def check_response_is_ok(response=None):
    if response is None:
        return False
    if response.status_code != requests.codes.OK:
        return False
    return True

def get_headers(uid):
    return {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'cookie': 'l=v;',
        'origin': 'https://space.bilibili.com',
        'pragma': 'no-cache',
        'referer': f'https://space.bilibili.com/{uid}/dynamic',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
    }

def main(uid:str):
    offset_dynamic_id = 0
    query_url = 'http://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history' \
                f'?host_uid={uid}&offset_dynamic_id={offset_dynamic_id}&need_top=0&platform=web&my_ts={int(time.time())}'
    headers = get_headers(uid)
    response = requests_get(query_url, headers=headers)
    if check_response_is_ok(response):
        try:
            result = json.loads(str(response.content, 'utf-8'))
        except UnicodeDecodeError:
            return

        if result['code'] != 0:
            return

        data = result['data']

        if len(data['cards']) == 0:
            return

        item = data['cards'][0]
        try:
            uname = item['desc']['user_profile']['info']['uname']
        except KeyError:
            return

        timestamp = item['desc']['timestamp']
        dynamic_id = item['desc']['dynamic_id']
        if DYNAMIC_DICT[uid][1] == 0:
            if timestamp <= DYNAMIC_DICT[uid][0]:
                DYNAMIC_DICT[uid][0] = timestamp
                DYNAMIC_DICT[uid][1] = dynamic_id
                return
        elif DYNAMIC_DICT[uid][1] == dynamic_id:
            DYNAMIC_DICT[uid][0] = timestamp
            DYNAMIC_DICT[uid][1] = dynamic_id
            return

        dynamic_type = item['desc']['type']
        if dynamic_type == 2 or dynamic_type == 4:
            #cqhttp_url = f'http://cqhttp:5700/send_private_msg?user_id=809474873&message=【{uname}】发布了动态，快来围观一下：https://www.bilibili.com/opus/{dynamic_id}&auto_escape=false'
            cqhttp_url = f'http://cqhttp:5700/send_group_msg?group_id=707363327&message=【{uname}】发布了动态，快来围观一下：https://www.bilibili.com/opus/{dynamic_id}&auto_escape=false'
            requests_get(cqhttp_url, headers=headers)
        elif dynamic_type == 8:
            bvid = item['desc']['bvid']
            #cqhttp_url = f'http://cqhttp:5700/send_private_msg?user_id=809474873&message=【{uname}】投稿了，一键三连支持一下：https://www.bilibili.com/opus/{dynamic_id}&auto_escape=false'
            cqhttp_url = f'http://cqhttp:5700/send_group_msg?group_id=707363327&message=【{uname}】投稿了，一键三连支持一下：https://www.bilibili.com/video/{bvid}'
            requests_get(cqhttp_url, headers=headers)

        DYNAMIC_DICT[uid][0] = timestamp
        DYNAMIC_DICT[uid][1] = dynamic_id


if __name__ == '__main__':
    #from datetime import datetime
    #custom_timestamp = '2023-8-27'
    #datetime_obj = datetime.strptime(custom_timestamp, '%Y-%m-%d')
    #int_timestamp = int(datetime_obj.timestamp())
    DYNAMIC_DICT['3493299188927189'] = [int(time.time()), 0]
    main('3493299188927189')
    schedule.every(1).minutes.do(main, uid='3493299188927189')
    while True:
        schedule.run_pending()
        time.sleep(10)
