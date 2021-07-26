from scrapy import Spider, Request, spiders,FormRequest
from scrapy.item import DictItem
from scrapy.utils.trackref import NoneType
from mediaspider.items import VInfoItem,ReplyInfoItem,DanmuInfoItem,UInfoItem,VInfoDynamicItem
import json
import logging
import requests
import re
import time
import datetime
import base64
header = {
       
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
    }

cookies="_uuid=FE18E94F-CAB1-69C0-753C-245A94DB063C04672infoc; buvid3=5D8ED97F-100C-4AAE-951D-9720D91F29EC143079infoc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(k|RYJYllJY0J'uY|ukYlm||; buivd_fp=5D8ED97F-100C-4AAE-951D-9720D91F29EC143079infoc; buvid_fp_plain=5D8ED97F-100C-4AAE-951D-9720D91F29EC143079infoc; buvid_fp=5D8ED97F-100C-4AAE-951D-9720D91F29EC143079infoc; fingerprint3=7cdce1880b09344ee0d74616931713d7; fingerprint_s=193f3299bcb4e2c36d107cd3a0b51a14; CURRENT_QUALITY=112; bp_video_offset_471644009=542730492934997055; bp_t_offset_471644009=542734418540372470; LIVE_BUVID=AUTO4616264373573122; fingerprint=8ad433d08805dd3661276580326c9208; SESSDATA=4b205deb,1642470292,f6610*71; bili_jct=7e4d9ba2897d7ed66e90e6ffd63f18ba; DedeUserID=327074361; DedeUserID__ckMd5=b5989e33de2a6abb; sid=6xct9ybc; bsource=search_baidu; _dfcaptcha=52c37e0e20fb82c0451705500419ae0c; PVID=2"

url5 = 'https://member.bilibili.com/x/vu/web/cover/up'
cover_path='/home/wzc/testcode/factory/output/picture/1.jpg'

class Upload(Spider):
    name='upload'
    cover_path='/home/wzc/testcode/factory/output/picture/1.jpg'
    def __init__(self):
        self.bili_jct = re.findall(r'bili_jct=(\S+?);',cookies)[0]
        
        self.cookies= {i.split('=')[0]: i.split('=')[1] for i in cookies.split('; ')}


    def start_requests(self) :
        
        try:
            with open(self.cover_path,'rb+') as file:
                print('正在上传封面')
                code = b'data:image/jpeg;base64,'+base64.b64encode(file.read())
                body={'cover': code,'csrf': self.bili_jct}
                yield FormRequest(url5,headers=header,formdata=body, cookies=self.cookies,method='POST',callback=self.parse)               
        except Exception:
            print('封面路径无效')

    def parse(self, response):
        logging.warning(response.text)

        js = json.loads(response.text)
        
        print('封面上传完毕')

        return None


class User(Spider):
    name='user'



    
