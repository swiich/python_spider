# coding=utf-8
"""
AES decrypt 'param' parameter
reference https://www.zhihu.com/question/36081767  @平胸小仙女
"""

import base64
from Crypto.Cipher import AES


class ArgsError(BaseException):
    """user-defined error type
    """
    def __init__(self, arg):
        self.args = arg


def get_params(first_param, forth_param):
    """
    get params
    """
    iv = "0102030405060708"

    first_key = forth_param
    second_key = 16 * 'F'

    h_encText = AES_encrypt(first_param, first_key.encode(), iv.encode())
    h_encText = AES_encrypt(h_encText.decode(), second_key.encode(), iv.encode())

    return h_encText.decode()


def get_encSecKey():
    """
    get encSecKey
    """
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06" \
                "d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d95" \
                "2872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3" \
                "ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f6" \
                "24750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey


def AES_encrypt(text, key, iv):
    """
    AES decrypt
    """
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)

    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text.encode())
    encrypt_text = base64.b64encode(encrypt_text)

    return encrypt_text


def crypt_api(ftype, id, offset=0):
    """
    decrypt params&encSeckey
    """
    try:
        if  ftype == 'follows':
            first_param = "{uid:\"%s\",offset:\"%s\",total:\"true\",limit:\"100\",csrf_token:\"\"}" % (id, offset)

        elif ftype == 'fans':
            first_param = "{userId:\"%s\",offset:\"%s\",total:\"true\",limit:\"100\",csrf_token:\"\"}" % (id, offset)

        elif ftype == 'comments':
            first_param = "{rid:\"\", offset:\"%s\", total:\"true\", limit:\"100\", csrf_token:\"\"}" % offset

        elif ftype == 'playlists':
            first_param = "{uid:\"%s\",type:\"-1\",limit:\"1000\",offset:\"%s\",total:\"true\",csrf_token:\"\"}" % (id, offset)

        elif ftype == 'ranks':
            first_param = "{uid:\"%s\",type:\"-1\",limit:\"1000\",offset:\"0\",total:\"true\",csrf_token:\"\"}" % id

        elif ftype == 'lyrics':
            first_param = "{id:\"%s\",lv:\"-1\",tv:\"-1\",csrf_token:\"\"}" % id

        elif ftype == 'mp3':
            first_param = "{ids:\"[%s]\",br:\"128000\",csrf_token:\"\"}" % id

        else:
            raise ArgsError('wrong type of ftype，fans or follows or comments or playlists or ranks or lyrics or mp3')

    except ArgsError as a:
        print(''.join(a.args))
        data = {}
        return data

    forth_param = "0CoJUm6Qyw8W8jud"
    params = get_params(first_param, forth_param)
    encSecKey = get_encSecKey()

    data = {
        "params": params,
        "encSecKey": encSecKey
    }

    return data
