import json
import logging
import random

try:
    import requests
    from flask import Flask, request
except ModuleNotFoundError:
    from os import system
    system('pip install requests==2.23.0')
    system('pip install Flask==2.3.3')
    import requests
    from flask import Flask, request



app = Flask(__name__)

CQHTTP_HOST = 'cqhttp:5700'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_random_usagi_pic()->str:
    return f'usagi/{random.randint(0, 9)}.gif'


@app.route('/', methods=['POST'])
def receive_post_data():
    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            logger.info(data)
            post_type = data['post_type']
            match post_type:
                case 'meta_event':
                    meta_event_type = data['meta_event_type']
                    match meta_event_type:
                        case 'heartbeat':
                            logger.info(data['time'])
                case 'message':
                    message_type = data['message_type']
                    match message_type:
                        case 'private':
                            response = requests.post(f'http://{CQHTTP_HOST}/send_private_msg?user_id={data["user_id"]}&message={data["message"]}&auto_escape=false', timeout=1000)
                            return response.text, response.status_code
                        case 'group':
                            sub_str = '[CQ:at,qq=3596295889]'
                            if sub_str in data['message']:
                                msg = data['message'].replace(sub_str, '').strip()
                                response = requests.post(f'http://{CQHTTP_HOST}/send_group_msg?group_id={data["group_id"]}&message={msg}&auto_escape=false', timeout=1000)
                                return response.text, response.status_code
                case 'notice':
                    notice_type = data['notice_type']
                    match notice_type:
                        case 'group_increase':
                            response = requests.post(f'http://{CQHTTP_HOST}/send_group_msg?group_id={data["group_id"]}&message=欢迎新人[CQ:at,qq={data["user_id"]}]&auto_escape=false', timeout=1000)
                            return response.text, response.status_code
                        case 'notify':
                            if data['target_id'] == data['self_id']:
                                group_id = data.get('group_id')
                                if group_id is not None:
                                    image_code = f"[CQ:image,file={get_random_usagi_pic()}]"
                                    response = requests.post(f'http://{CQHTTP_HOST}/send_group_msg?group_id={group_id}&message={image_code}&auto_escape=false', timeout=1000)
                                    return response.text, response.status_code
                                else:
                                    image_code = f"[CQ:image,file={get_random_usagi_pic()}]"
                                    response = requests.post(f'http://{CQHTTP_HOST}/send_private_msg?user_id={data["user_id"]}&message={image_code}&auto_escape=false', timeout=1000)
                                    return response.text, response.status_code
            return 'Received and logged JSON data successfully.'
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON data: {str(e)}")
            return 'Failed to decode JSON data.', 400
    else:
        return 'Only POST requests are allowed on this route.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
