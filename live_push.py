import json
import logging
import time

import requests
import schedule

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CQHTTP_HOST = 'http://cqhttp:5700'

room_list = [
    {
        'room_id': 30097617,
        'name': 'Nagi_小凪',
        'status': 0,
        'cover': '',
        'send_cover': True,
        'title': '',
        'interval': 60000,
        'qq_group': 0,
        'qq_group_list': [
            {
                'id': 707363327,
                'at_all': True,
            },
        ],
        'qq_person': 0,
        'msg': [
            '{name}尚未开播',
            '{name}正在直播：{title} https:',
            '{name}正在轮播',
        ],
    },
    {
        'room_id': 30507853,
        'name': '天姬樂_Rakii',
        'status': 0,
        'cover': '',
        'send_cover': True,
        'title': '',
        'interval': 60000,
        'qq_group': 0,
        'qq_group_list': [
            {
                'id': 908110223,
                'at_all': True,
            },
            {
                'id': 831227322,
                'at_all': True,
            },
        ],
        'qq_person': 0,
        'msg': [
            '{name}尚未开播',
            '{name}正在直播：{title} https:',
            '{name}正在轮播',
        ],
    },
]


def get_live_room_data(room_id):
    url = f"https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom?room_id={room_id}"
    response = requests.get(url, timeout=1000)

    try:
        json_data = json.loads(response.content)
        cb(room_id, json_data)
    except Exception as error:
        logger.error(error)


def get_room_cfg(room_id):
    room = next((data for data in room_list if data['room_id'] == room_id), None)
    if not room:
        logger.info(f"没找到这个直播间的配置{room_id}")
    return room


def cb(room_id, json_data):
    room = get_room_cfg(room_id)
    if not room:
        return

    status = json_data['data']['room_info']['live_status']

    room['cover'] = json_data['data']['room_info']['cover']
    room['title'] = json_data['data']['room_info']['title']

    if status != room['status']:
        room['status'] = status
        if status == 0:
            pass
        elif status == 1:
            send_msg(room_id)
        elif status == 2:
            pass
        else:
            logger.info(f"不知道啥情况。status {status}")


def send_msg(room_id):
    room = get_room_cfg(room_id)
    if not room:
        return
    msg = room['msg'][room['status']]
    if not msg:
        return logger.info(f"没有找到提醒消息。{room_id} {room['status']}")

    msg = msg.replace('{name}', room['name']).replace('{title}', room['title']).replace('{room_id}', str(room['room_id']))
    logger.info(msg)
    image_code = f"[CQ:image,file={room['cover']}]" if room['send_cover'] and room['cover'] else ''
    if room['qq_group'] != 0:
        message = f'{image_code}{msg}'
        logger.info(message)
        url = f"{CQHTTP_HOST}/send_group_msg?group_id={room['qq_group']}&message={message}&auto_escape=false"
        requests.post(url, timeout=1000)

    if room['qq_group_list'] and len(room['qq_group_list']) > 0:
        for group in room['qq_group_list']:
            if group['id']:
                at_code = '[CQ:at,qq=all,name=不在群的QQ]' if group['at_all'] else ''
                message = f'{image_code}{at_code}{msg}'
                logger.info(message)
                url = f"{CQHTTP_HOST}/send_group_msg?group_id={group['id']}&message={message}&auto_escape=false"
                requests.post(url, timeout=1000)

    if room['qq_person'] != 0:
        message = f'{image_code}{msg}'
        logger.info(message)
        url = f"{CQHTTP_HOST}/send_private_msg?user_id={room['qq_person']}&message={message}&auto_escape=false"
        requests.post(url, timeout=1000)


def main():
    for room_data in room_list:
        get_live_room_data(room_id=room_data['room_id'])
        schedule.every(room_data['interval'] / 1000).seconds.do(get_live_room_data, room_id=room_data['room_id'])
    while True:
        schedule.run_pending()
        time.sleep(10)


if __name__ == '__main__':
    main()
