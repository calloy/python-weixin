# coding=utf-8
import urllib2
from bs4 import BeautifulSoup


#一个简单的爬虫类
class Zhicheng(object):

    def __init__(self):
        pass
    def tianqi(self,city='deyang'):
        url = 'http://weather.sina.com.cn/'+city

        htm = urllib2.urlopen(url)
        if htm.getcode() != 200:
            return '天气查询被玩坏了，等2秒钟后继续玩玩看。'
        soup = BeautifulSoup(htm,'html.parser',from_encoding='utf-8')
        wendu = soup.find('div',class_='slider_degree').get_text()
        mingcheng = soup.find('p',class_='slider_detail').get_text()
        return wendu+' '+mingcheng.replace(' ','')
