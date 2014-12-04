# -*- encoding:UTF-8 -*-
import json

import requests

import utils

'''
Created on 2014/12/03

@author: user
'''
def get_api_url(url, action, key):
    '''
    APIのURLを得る
    '''
    return url + '/index.php?page=api&action=' + action + '&api_key=' + key

def get_dashboard_data(url, key):
    '''
    getdashboarddata から必要な情報を取得
    '''
    r = requests.get(get_api_url(url, 'getdashboarddata', key))
    d = json.loads(r.text)

    # 個人のh ashrate と通貨単位 を取得
    hashrate = utils.kiri_age(d['getdashboarddata']['data']['personal']['hashrate'])
    currency = d['getdashboarddata']['data']['pool']['info']['currency']

    # TODO; 単位はとりあえず'kH/s'決め打ち
    result = {'hashrate': hashrate, 'unit': 'kH/s', 'currency': currency}

    return result

def get_credit(url, key):
    '''
    getusertransactions から必要な情報を取得
    '''
    r = requests.get(get_api_url(url, 'getusertransactions', key))
    d = json.loads(r.text)

    # Credit を取得
    result = {
            'credit': utils.kiri_age(
                    d['getusertransactions']['data']['transactionsummary']['Credit']
            )
    }

    return result

def get_worker_info(url, key):
    '''
    getuserworkers から必要な情報を取得
    '''
    r = requests.get(get_api_url(url, 'getuserworkers', key))
    d = json.loads(r.text)

    # username、hashrate を取得
    # template内のif文で計算が出来ないため、出し分け制御用の数値を取っておく
    worker_list = []
    for i, worker in enumerate(d['getuserworkers']['data']):
        info = {
                'username': worker['username'].split('.')[1]
                , 'hashrate': utils.kiri_age(worker['hashrate'], 2)
                , 'n': i % 3
        }
        worker_list.append(info)

    return worker_list
