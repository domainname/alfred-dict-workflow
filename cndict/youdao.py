#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import json
from cndict.utils import *

def lookup(word, *args):
    params = {
        'keyfrom': 'awf-Chinese-Dict',
        'key': '19965805',
        'version': '1.1',
        'type': 'data',
        'doctype': 'json',
        'q': word
    }
    url = '{}?{}'.format('http://fanyi.youdao.com/openapi.do', urllib.parse.urlencode(params))
    try:
        data = urllib.request.urlopen(url).read()
        data = json.loads(data)
    except:
        raise DictLookupError('error to fetch data.')
    err_code = data.get('errorCode', -1)
    if err_code != 0:
        err_msg = {
            20: 'word is too long.',
            30: 'unable to translate.',
            40: 'language is not supported.',
            50: 'key is invalid.'
        }
        raise DictLookupError(err_msg.get(err_code, 'unkown error.'))
    result = []
    basic = data.get('basic', {})
    if basic:
        if is_english(word):
            result.extend(basic.get('explains', []))
        else:
            for explain in basic.get('explains', []):
                pos = explain.rfind(']')
                result.append(explain[pos+1:] if pos >= 0 else explain)
        if result:
            phonetic = basic.get('phonetic', '')
            result.insert(0, '{}{}'.format(word, ' /{}/'.format(phonetic) if phonetic else ''))
    return result


def extract(word, item):
    if not is_english(word):
        return item


def get_url(word):
    params = {'q': word}
    return '{}?{}'.format('http://dict.youdao.com/search', urllib.urlencode(params))
