import requests
import json
import os

base_url = 'https://www.douyu.com/'
backpack_uri = 'japi/prop/backpack/web/v1'
send_gift_uri = 'japi/prop/donate/mainsite/v1'
serve_base_url = 'https://sc.ftqq.com/'

room_id = os.environ['ROOMID']
cookie = os.environ['COOKIE']
sc_key = os.environ['SCKEY']
sc_on = os.environ['SCON'] == 'ON'

headers = {
    'authority': 'www.douyu.com',
    'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="97", "Chromium";v="97"',
    'accept': 'application/json, text/plain, */*',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69',
    'referer': f'https://www.douyu.com/{room_id}',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-ch-ua-platform': '"Windows"',
}


def send_message_list(message_list: list, sc_key: str) -> None:
    raw_message = '\n'.join(message_list)
    requests.get(serve_base_url + sc_key + '.send?text=' + raw_message)


def format_cookie(cookie_str: str) -> dict:
    cookie_dict = {}
    for line in cookie_str.split(';'):
        key, value = line.split('=', 1)
        cookie_dict[key] = value
    return cookie_dict


def query_gift_list() -> list:
    payload = {
        'rid': room_id,
    }
    query_backpack_url = base_url + backpack_uri
    response = requests.get(url=query_backpack_url, headers=headers, params=payload, cookies=format_cookie(cookie))
    res_json_obj = json.loads(response.text)
    gift_list = res_json_obj['data']['list']
    return gift_list


def send_gift(gift_list: list) -> list:
    message_list = []
    send_gift_url = base_url + send_gift_uri
    for gift in gift_list:
        gift_id = gift['id']
        gift_num = gift['count']
        gift_name = gift['name']
        data = {
            'propId': gift_id,
            'propCount': 1,
            'roomId': room_id,
            'bizExt': '{"yzxq":{}}'
        }
        succ_cnt = 0
        err_msg_list = []
        for _ in range(0, gift_num):
            res = requests.post(send_gift_url, data=data, headers=headers, cookies=format_cookie(cookie))
            if res.status_code == 200 and res.json()['error'] == 0:
                succ_cnt += 1
            else:
                err_msg_list.append(res.json())
                message_list.append(f'赠送 {gift_num} 个{gift_name}给房间: {room_id} 出现错误，错误代码为 {res.status_code} : {res.json()}')
        message_list.append(f'成功赠送了 {succ_cnt}/{gift_num} 个{gift_name}给房间: {room_id}')
        message_list.append(f'赠送出现错误，共 {gift_num - succ_cnt}/{gift_num} 出现错误，错误信息为 {err_msg_list}')
    return message_list


if __name__ == '__main__':
    gift_list = query_gift_list()
    msg_list = send_gift(gift_list)
    print(msg_list)
    if sc_on:
        send_message_list(msg_list, sc_key)
