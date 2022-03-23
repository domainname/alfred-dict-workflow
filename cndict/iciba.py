#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import urllib
import urllib.parse
import urllib.request

from cndict.utils import *


def lookup(word, *args):
    params = {
        'key': 'E93A321FB1995DF5EC118B51ABAF8DC7',
        'type': 'json',
        'w': word.lower()
    }
    url = '{}?{}'.format('http://dict-co.iciba.com/api/dictionary.php', urllib.parse.urlencode(params))
    try:
        data = urllib.request.urlopen(url).read()
        data = json.loads(data)
    except:
        raise DictLookupError('error to fetch data.')
    result = []
    symbol = data.get('symbols', [{}])[0]
    if is_english(word):
        for elem in symbol.get('parts', []):
            result.append('{} {}'.format(elem.get('part', ''), '；'.join(elem.get('means', []))))
        if result:
            phonetic = symbol.get('ph_am', '')
            result.insert(0, '{}{}'.format(word, ' /{}/'.format(phonetic) if phonetic else ''))
    else:
        elem = symbol.get('parts', [{}])[0]
        for mean in elem.get('means', []):
            word_mean = mean.get('word_mean', '')
            if word_mean:
                result.append(word_mean)
        if result:
            phonetic = symbol.get('word_symbol', '')
            result.insert(0, '{}{}'.format(word, ' /{}/'.format(phonetic) if phonetic else ''))
    return result


def extract(word, item):
    if not is_english(word):
        match = re.match(r'(\[.+\] )?(.+)', item)
        if match:
            return match.group(2)


def get_url(word):
    return 'http://www.iciba.com/' + urllib.parse.quote(word)
