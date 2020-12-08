import requests

headers = {
    'authority': 'www.ximalaya.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
    'xm-sign': '987eed28ac86bb4f07c07414004e7a8d(85)1605856492228(12)1605856393877',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.ximalaya.com/search/album/%E8%BF%9B%E5%8D%9A%E4%BC%9A',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': '_xmLog=h5&b8bae21a-8664-4c1f-8432-6aeed68afc9b&2.1.2; x_xmly_traffic=utm_source%253A%2526utm_medium%253A%2526utm_campaign%253A%2526utm_content%253A%2526utm_term%253A%2526utm_from%253A; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1605236706,1605492863,1605758265,1605840828; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1605840828',
}

params = (
    ('core', 'album'),
    ('kw', '\u8FDB\u535A\u4F1A'),
    ('page', '1'),
    ('spellchecker', 'true'),
    ('rows', '20'),
    ('condition', 'relation'),
    ('device', 'iPhone'),
    ('fq', ''),
    ('paidFilter', 'false'),
)

response = requests.get('https://www.ximalaya.com/revision/search/main', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://www.ximalaya.com/revision/search/main?core=album&kw=%E8%BF%9B%E5%8D%9A%E4%BC%9A&page=1&spellchecker=true&rows=20&condition=relation&device=iPhone&fq=&paidFilter=false', headers=headers)
