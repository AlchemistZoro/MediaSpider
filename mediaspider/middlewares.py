
import json
import requests
import logging
import random
import time

from mediaspider.settings import USER_AGENT_LIST

#随机设置user-agent
class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        rand_use  = random.choice(USER_AGENT_LIST)
        if rand_use:
            request.headers.setdefault('User-Agent', rand_use)


class ProxyMiddleware(object):
    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url

    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:             
                proxy=response.text
                return proxy
        except requests.ConnectionError:
           
            return False

    # def process_request(self, request, spider):
    #     logging.error('======' + 'retry_times ' + str(request.meta.get('retry_times')) + "======")
    #     if request.meta.get('retry_times'):
    #         proxy = self.get_random_proxy()
    #         if proxy:
    #             logging.error('======' + '使用代理 ' + str(proxy) + "======")
    #             request.meta['proxy'] = 'https://{proxy}'.format(proxy=proxy)
    #         # time.sleep(10)
    #     # response = requests.get(self.proxy_url)
    #     # proxy=response.text
    #     # logging.error('======' + '使用代理 ' + str(proxy) + "======")
    #     # request.meta['proxy'] = 'https://{proxy}'.format(proxy=proxy)
    #     # logging.error('======' + '使用代理 ' + str( request) + "======")


    # def process_request(self, request, spider):
    #     proxy = self.get_random_proxy()
    #     if proxy:
    #         self.logger.warning('======' + '使用代理 ' + str(proxy) + "======")
    #         request.meta['proxy'] = 'https://{proxy}'.format(proxy=proxy)

    def process_response(self, request, response, spider):
        self.logger.warning("response.status:"+str(response.status)+"  request:"+request.url)
        if response.status != 200:          
            
            request.meta['proxy'] = 'https://{proxy}'.format(proxy=self.get_random_proxy())
            self.logger.warning("again response ip:"+request.meta['proxy'])
            return request
        return response

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        #返回一个初始化过后的类
        return cls(
            proxy_url=settings.get('PROXY_URL')
        )

class RandomDelayMiddleware(object):
    def __init__(self, delay):
        self.delay = delay

    @classmethod
    def from_crawler(cls, crawler):
        delay = crawler.spider.settings.get("RANDOM_DELAY", 10)
        if not isinstance(delay, int):
            raise ValueError("RANDOM_DELAY need a int")
        return cls(delay)

    def process_request(self, request, spider):
        delay = random.randint(0, self.delay)
        logging.debug("### random delay: %s s ###" % delay)
        time.sleep(delay)
