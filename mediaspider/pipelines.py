
import pymysql
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from mediaspider.msql import GetSql
from mediaspider.items import DanmuInfoItem,VInfoItem,ReplyInfoItem,UInfoItem
import logging



class MysqlPipeline():
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
       
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DBNAME'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWD'),
            port=crawler.settings.get('MYSQL_PORT'),
        
        )
    
    def open_spider(self, spider):
        tables = ['Vinfo','Reply','Danmu']
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database,
                                  port=self.port)
        self.cursor = self.conn.cursor()
      
        for table in tables:
            sqlname='CreateTable'+table
            

            sql=GetSql(sqlname)
            

            self.cursor.execute(sql)
            self.conn.commit()


    
    def close_spider(self, spider):

        self.conn.close()
    
    def process_item(self, item, spider):
        if isinstance(item, ReplyInfoItem):
            table='Reply'
            data=item['ReplyItem']
        elif isinstance(item, VInfoItem):
            table='Vinfo'

        elif isinstance(item, DanmuInfoItem):
            table='Danmu'
        elif isinstance(item, UInfoItem):
            table='UInfo'

        
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'insert ignore into %s (%s) values (%s)' % (table, keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.conn.commit()

        return item

       
    

   
        
        
