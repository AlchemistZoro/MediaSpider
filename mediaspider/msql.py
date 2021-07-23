
import pymysql
# from videospider import GetAllInfoByBid
import argparse
import time

sqldic={

'CreateTableVinfo':'''
create table if not exists Vinfo(bvid varchar(31) primary key,
                            aid varchar(31),
                            cid varchar(31),
                            iscopy int(10) ,
                            tid int(10) ,
                            tname varchar(31) ,
                            pic varchar(255) ,
                            title varchar(255),
                            descs varchar(255),
                            duration int(10) ,
                            dimension varchar(255) ,
                            videos int(10)   ,
                            pubdate varchar(31)  ,
                            ctime varchar(31) ,                                                   
                            view int(10) ,
                            danmaku int(10) ,
                            reply int(10),
                            likes int(10) ,
                            dislikes int(10) ,
                            coin int(10) ,
                            favorite int(10),
                            share int(10),
                            now_rank int(10),
                            his_rank int(10),                            
                            mid varchar(31)
                            );''',
'CreateTableDanmu':'''
create table if not exists Danmu(rowid varchar(31) primary key,

                            cid varchar(31) ,

                            timestamp varchar(31),

                            floattime float(16,5),

                            mode int(10),

                            size int(10),

                            color varchar(31),

                            pool  int(10),

                            author varchar(31),                            

                            text varchar(255)
                            );''',
'CreateTableReply':'''
create table if not exists Reply(rpid varchar(31) primary key,
                            oid varchar(31),

                            mid varchar(31),
                            
                            likes int(10),

                            ctime  varchar(31),

                            message text
                            );''',

'CreateTableVinfo_dynamic': '''                     create table if not exists Vinfo_dynamic(bvid varchar(31) ,
                                                                           
                            view int(10) ,
                            danmaku int(10) ,
                            reply int(10),
                            likes int(10) ,
                            dislikes int(10) ,
                            coin int(10) ,
                            favorite int(10),
                            share int(10),
                            now_rank int(10),
                            his_rank int(10),                            
                            mid varchar(31),
							recordtime varchar(30) 
                            );'''

}

def GetSql(sqlname):
    return sqldic[sqlname]

def CreateTable(cursor,conn,sql):
    cursor.execute(sql)
    conn.commit()

def CreateReply(cursor,conn):
    CreateTable(cursor,conn,createTableVReply)

# item 已经是dict的形式
def InsertVInfo(data,cursor,conn):
    # data = dict(item)
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    sql = 'insert ignore into %s (%s) values (%s)' % ('Vinfo', keys, values)
    cursor.execute(sql, tuple(data.values()))
    conn.commit()


def InsertDanmu(data,cursor,conn):
    # data = dict(item)
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    sql = 'insert ignore into %s (%s) values (%s)' % ('Danmu', keys, values)
    cursor.execute(sql, tuple(data.values()))
    conn.commit()


def InsertVReply(data,cursor,conn):
    # data = dict(item)
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    sql = 'insert ignore into %s (%s) values (%s)' % ('VReply', keys, values)
    cursor.execute(sql, tuple(data.values()))
    conn.commit()

# def ProcessVideoInfo(vbid,MYSQL_DBNAME='bilibili',MYSQL_HOST='localhost',MYSQL_USER= 'root',MYSQL_PASSWD= '123456',MYSQL_PORT= 3306):
   
#     conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWD, database=MYSQL_DBNAME,
#                                   port=MYSQL_PORT)
    
#     cursor = conn.cursor()
#     CreateTable(cursor,conn,createTableVinfo)
#     CreateTable(cursor,conn,createTableDanmu)
#     CreateTable(cursor,conn,createTableVReply)

#     DanmuList,VInfoObj,VReplyList=GetAllInfoByBid(vbid)
    
#     InsertVInfo(VInfoObj,cursor,conn)
#     for Danmu in  DanmuList:
#         InsertDanmu(Danmu,cursor,conn)
#     for Reply in  VReplyList:   
#         InsertVReply(Reply,cursor,conn)
#     # print('finishi video :'+vbid)
#     cursor.close()
#     conn.close()


if __name__ == "__main__":
    time_start=time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("vbid", help="vbid of a video on bilibili platform",default='BV1hL411p7XA')
    args = parser.parse_args()
    # danmu=GetDanmuByBid(args.bvid)
    # VInfo,oid=GetVInfoByBid(args.bvid)  
    # VReply=GetVReplyByOid(oid,cookie)
    # conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWD, database=MYSQL_DBNAME,
    #                               port=MYSQL_PORT)
    # cursor = conn.cursor()

    # # vbid='BV1hL411p7XA'

    # CreateTable(cursor,conn,createTableVinfo)
    # CreateTable(cursor,conn,createTableDanmu)
    # CreateTable(cursor,conn,createTableVReply)

    # DanmuList,VInfoObj,VReplyList=GetAllInfoByBid(args.vbid)
    # InsertVInfo(VInfoObj,cursor,conn)
    # for Danmu in  DanmuList:
    #     InsertDanmu(Danmu,cursor,conn)
    # for Reply in  VReplyList:   
    #     InsertVReply(Reply,cursor,conn)

    # cursor.close()
    # conn.close()

    ProcessVideoInfo(args.vbid)

    time_end=time.time()

    print(time_end-time_start)