from scrapy import Spider, Request
from mediaspider.items import VInfoItem,ReplyInfoItem,DanmuInfoItem,UInfoItem
import json
import logging
import requests
import re
import time


class BilibiliSpider(Spider):     
    name = 'bilibili'
    
    url_userspace=r'https://api.bilibili.com/x/space/arc/search?mid={mid}&pn={pn}&ps={ps}'
    url_videoinfo=r'http://api.bilibili.com/x/web-interface/view?bvid={bvid}'
    url_reply=r'http://api.bilibili.com/x/v2/reply?type={Type}&oid={oid}&pn={pn}&ps={ps}'
    
    def __init__(self, *args, mid: str=None, ps: int=None, **kwargs):
        """初始化

            Args:
                mid: 用户id
                ps: 视频列表每页视频数量，默认100
        """

        super().__init__(*args, **kwargs)

        if mid is None: mid = 672328094  #用户的id 老番茄 546195 番剧 928123 影视 15773384 嘉然 672328094
        if ps is None: ps = 100

        self.mid = mid
        self.ps = ps
        self.count=0
        # 视频列表链接模版 （一个参数）
        self.url = self.url_userspace.format(mid=mid, ps=ps, pn='{}')

        self.pn = 1
        # self.maxpn=int(GetArchivecount(mid)/ps)+1
        # self.logger.debug('======'  + str(maxpn) + "======")
        # 初始链接
        self.start_urls = [self.url.format(self.pn)]

    def parse(self, response):
        
        jresponse=json.loads(response.text)
        

        # logging.warning('======'  + str(len(vlist)) + "======")
        # logging.warning('======code'  + str(jresponse['code']) + "======")
        logging.warning(str(self.pn)+'======status:'  + str(response.status) + "======")

        
        vlist=jresponse['data']['list']['vlist']
        if len(vlist)>0:
            for vinfo in vlist:
                bvid=vinfo['bvid']
                oid=vinfo['aid']
                vurl=self.url_videoinfo.format(bvid=bvid)
                rurl=self.url_reply.format(Type=1,oid=oid,pn=100,ps=40)
                logging.warning('======'  + str(bvid) + "======")
                
                yield Request(url=vurl, callback=self.ParseVideoInfo,dont_filter =True)
                
                yield Request(url=rurl, callback=self.ParseReplyInfo,dont_filter = True)

        
            self.pn += 1
            url = self.url.format(self.pn)
            yield Request(url=url, callback=self.parse,dont_filter = True)
            
    
    

    def ParseVideoInfo(self, response):
        # logging.warning('======code:'  + str(json.loads(response.text)['code']) + "======")
        # logging.warning('======code:'  + str(response.status) + "======")
        if json.loads(response.text)['code']==-412:
            yield None
        else:
            data=json.loads(response.text)['data']
            #基本信息
            
            aid = data['aid']  # 视频ID
            
            bvid = data['bvid']  # 视频ID
            cid = data['cid']  # 弹幕连接id
            tid = data['tid']  # 区       
            iscopy=data['copyright'] # 是否转载  
            tname=data['tname']  # 子分区
            pic = data['pic']  # 封面
            title = data['title']  # 标题
            desc = data['desc']  # 简介
            duration = data['duration']  # 总时长，所有分P时长总和
            dimension=str(data['dimension'] ) #视频1P分辨率
            videos = data['videos']  # 分P数
            pubdate = data['pubdate']  # 发布时间
            ctime=data['ctime'] #用户投稿时间      
            
            
            #视频状态
            stat=data['stat']            
            view = stat['view']  # 播放数
            danmaku = stat['danmaku']   # 弹幕数
            reply = stat['reply']   # 评论数
            like = stat['like']   # 点赞数
            dislike = stat['dislike']   # 点踩数
            coin = stat['coin']   # 投币数
            favorite = stat['favorite']   # 收藏数
            share = stat['share']  # 分享数
            now_rank=stat['now_rank'] #当前排名 
            his_rank=stat['his_rank'] #历史最高排名

            # UP主信息
            owner=data['owner']
            mid = owner['mid']  # UP主ID

            item = VInfoItem(
                    
                aid = aid ,
                bvid = bvid,
                cid = cid  ,
                iscopy=iscopy ,
                tid = tid  ,
                tname=tname ,
                pic = pic  ,
                title = title ,
                descs = desc ,
                duration =duration ,
                dimension=dimension ,
                videos = videos  ,
                pubdate = pubdate  ,
                ctime=ctime ,
                

                
                view = view  ,
                danmaku = danmaku  ,
                reply = reply   ,
                likes =like  ,
                dislikes = dislike  ,
                coin = coin  ,
                favorite = favorite  ,
                share = share  ,
                now_rank=now_rank ,
                his_rank=his_rank ,
                    
                
                mid = mid 
                )
            yield item

    def ParseReplyInfo(self, response):

        
        if json.loads(response.text)['code']==-412:
            
            yield None
        else:
            data=json.loads(response.text)['data']
            logging.warning(json.loads(response.text)['code'])
            # logging.warning(data)
            item_list=[]
            RepliList=data['replies']
            for Repli in RepliList:
                objRepli={}
                objRepli['oid']=Repli['oid']
                objRepli['message']=Repli['content']['message']
                objRepli['mid']=Repli['mid']
                objRepli['likes']=Repli['like']
                objRepli['ctime']=Repli['ctime']
                objRepli['rpid']=Repli['rpid']
                item= objRepli
                yield item
                  
    





# class PartitionSpider(Spider):
#     url=

# class UserSpider(Spider):
#     url=

# class RankSpider(Spider):
#     url=

# class KeyWordSpider(Spider):
#     url=

# class VInfoSpider(Spider):
#     url=r'http://api.bilibili.com/x/web-interface/view?bvid={bvid}'

# class DanmuSpder(Spider):
#     url=

class ReplySpider(Spider):

    name = 'replyspider'
    url=r'http://api.bilibili.com/x/v2/reply?type={type}&oid={oid}&pn={pn}&ps={ps}'
    
    def __init__(self,oid='974254684',type=1,pn=1,ps=20,*args,**kwargs):
        """初始化

            Args:
                mid: 用户id
                ps: 视频列表每页视频数量，默认100
        """

        super().__init__(*args, **kwargs)

        self.oid=oid
        self.ps = ps
        self.pn=pn
        self.type=type

        self.url = self.url.format(oid=oid, ps=ps, pn=pn,type=type)
        self.start_urls = [self.url]

    def parse(self, response, **kwargs):

        if json.loads(response.text)['code']==-412:
            
            yield None
        else:
            data=json.loads(response.text)['data']
            logging.warning(json.loads(response.text)['code'])
            # logging.warning(data)
            item_list=[]
            RepliList=data['replies']
            for Repli in RepliList:
                objRepli=ReplyInfoItem()
                objRepli['oid']=Repli['oid']
                objRepli['message']=Repli['content']['message']
                objRepli['mid']=Repli['mid']
                objRepli['likes']=Repli['like']
                objRepli['ctime']=Repli['ctime']
                objRepli['rpid']=Repli['rpid']
                item= objRepli
                yield item
        
        
        






