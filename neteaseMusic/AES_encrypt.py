'''
AES解密params参数
参数解密过程参考https://www.zhihu.com/question/36081767  @平胸小仙女
'''

import base64
from Crypto.Cipher import AES


def get_params(first_param, forth_param):
    '''
    获取params
    :param first_param:
    :param forth_param:
    :return:
    '''
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'
    h_encText = AES_encrypt(first_param, first_key.encode(), iv.encode())
    h_encText = AES_encrypt(h_encText.decode(), second_key.encode(), iv.encode())
    return h_encText.decode()


def get_encSecKey():
    '''
    获取encSecKey
    :return: encSecKey
    '''
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey


def AES_encrypt(text, key, iv):
    '''
    AES解密
    :param text:
    :param key:
    :param iv:
    :return: encrypt_text
    '''
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text.encode())
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text


def crypt_api_playlist(uid):
    '''
    通过分析网易云网络请求抓包，playlist由ajax向指定网页服务器发包获取json格式文档动态生成，包含playlist所有数据, post内容为params & encSecKey
    :param uid: 用户ID
    :return: data={params,encSecKey}
    '''

    # 初始化页面与下拉页面传入参数不同
    first_param = "{uid:\"%s\",type:\"-1\",limit:\"1000\",offset:\"0\",total:\"true\",csrf_token:\"\"}" % (uid)
    # offset: 偏移量=n*limit-1   n为刷新数量
    # total: 页面初始化时为true
    # limit: 每次刷新歌单数量
    # first_param = "{uid:\"%s\",wordwrap:\"7\", offset:\"%s\", total:\"false\", limit:\"36\", csrf_token:\"\"}" % (uid, offset)

    forth_param = "0CoJUm6Qyw8W8jud"
    params = get_params(first_param, forth_param)
    encSecKey = get_encSecKey()
    data = {
        "params": params,
        "encSecKey": encSecKey
    }
    return data