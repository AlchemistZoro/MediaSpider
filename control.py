import time
import os

def main(midlist):
    while True:
        for mid in midlist:
            os.system("scrapy crawl userspider -a mid={}".format(mid))
            os.system("scrapy crawl uservideospider -a mid={}".format(mid))
        time.sleep(60*60)

if __name__=="__main__":
    midlist=['327074361','672328094']
    main(midlist)