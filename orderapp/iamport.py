import requests

from django.conf import settings


DEFAULT_URL = 'https://api.import.kr/'


#  Iamport에 토큰 얻어오기
def get_token():
    access_data = {
        'imp_key': settings.IAMPORT_KEY,
        'imp_secret': settings.IAMPORT_SECRET,
    }
    url = DEFAULT_URL+'users/getToken'
    req = requests.post(url, data=access_data)
    json_res = req.json()

    if json_res['code'] == 0:
        return json_res['response']['access_token']
    else:
        return None


#  결제될 내역에 대한 사전정보 등록 및 검증
def payments_prepare(order_id, amount, *args, **kwargs):
    access_token = get_token()
    if access_token:
        access_data = {
            'merchant_uid': '',
            'amount': '',
        }
        url = DEFAULT_URL + 'payments/prepare'
        headers = {
            'Authorization': access_token
        }
        req = requests.post(url, data=access_data, headers=headers)
        json_res = req.json()

        if json_res['code'] != 0:
            raise ValueError('API 통신 오류')

    else:
        raise ValueError('Access Token 오류')


#  결제 결과를 조회
def find_transaction(order_id, *args, **kwargs):
    access_token = get_token()
    if access_token:
        url = DEFAULT_URL + 'payments/find/' + order_id
        headers = {
            'Authorization': access_token
        }
        req = requests.post(url, headers=headers)
        json_res = req.json()

        if json_res['code'] == 0:
            context = {
                'imp_id': json_res['response']['imp_uid'],
                'merchant_order_id': json_res['response']['merchant_uid'],
                'amount': json_res['response']['amount'],
                'status': json_res['response']['status'],
                'type': json_res['response']['pay_method'],
                'receipt_url': json_res['response']['receipt_url'],
            }
            return context
        else:
            return None
    else:
        raise ValueError('Access Token 오류')