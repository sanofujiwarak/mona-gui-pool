# -*- encoding:UTF-8 -*-
import re

'''
Created on 2014/12/03

@author: user
'''
def get_absolute_url(request):
    '''
    絶対URLを返す
    末尾の'/'を削ったURLを返す
    '''
    # 存在しないURIを設定し、'/'を削って絶対URLを得る
    absolute_uri = request.build_absolute_uri('a')
    return absolute_uri[0:len(absolute_uri)-2]

def kiri_age(m, n=0):
    '''
    切り上げ処理を行う
    '''
    # 小数点以下桁数指定をint型にする
    n = int(n)

    # m の絶対値を処理対象とする
    m_str = str(abs(m))

    # X.Xe-nn 表記かをチェック
    pattern = re.compile('(\d+\.\d+)[eE]-(\d+)')
    obj = pattern.match(m_str)
    if obj:
        # X.Xe-nn 表記の場合
        # 0.00･･･ 表記に変更する
        m_str = '0.' + ''.center(int(obj.group(2)) - 1, '0') \
                + obj.group(1).replace('.', '')

    # 整数部分と小数部分に分ける
    m_str = m_str.split('.')

    if 1 < len(m_str) and 0 <= n < len(m_str[1]):
        # 小数部分が存在し、小数点以下桁数指定が有効な場合
        # 切り上げ
        if n == 0:
            # 整数部を切り上げる
            result = int(m_str[0]) + 1
        else:
            # 小数点以下桁数の指定部分に1を加算し、残りの桁は捨てる
            result = int(m_str[0]) + 10**(-n) * (int(m_str[1][:n]) + 1)

        if m < 0:
            # m が負の数である場合
            # マイナスを掛けて正負を元に戻す
            result = -1 * result

    else:
        # 小数点以下桁数指定が無効な場合
        if n < 0:
            # 負の数が指定された場合
            raise RuntimeError, u"小数点以下桁数には正の整数を指定してください。"

        # それ以外は値をそのまま返す
        result = m

    return result
