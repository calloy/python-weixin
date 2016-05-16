# coding=utf-8
import re
import urllib2
from bs4 import BeautifulSoup


#一个简单的爬虫类
class Zhicheng(object):

    def __init__(self):
        self.bus_url ='http://wapapp.dy4g.cn/bus/auto/test.php?t=linhtml&busline='
        self.bus_data_url ='http://wapapp.dy4g.cn/bus/auto/test.php?t=busdb&busline='
        self.bus_data = {}
    #天气模块主要是用来，获取新浪天气情况的。
    #return 当前温度，和天气情况
    def tianqi(self,city='deyang'):
        url = 'http://weather.sina.com.cn/'+city

        htm = urllib2.urlopen(url)
        if htm.getcode() != 200:
            return '天气查询被玩坏了，等2秒钟后继续玩玩看。'
        soup = BeautifulSoup(htm,'html.parser',from_encoding='utf-8')
        wendu = soup.find('div',class_='slider_degree').get_text()
        mingcheng = soup.find('p',class_='slider_detail').get_text()
        return wendu+' '+mingcheng.replace(' ','')

    def get_bus(self,busline=24):
        if not self._get_bus_data(self.bus_url+str(busline)):
            return
        html = urllib2.urlopen(self.bus_data_url+str(busline))
        bus = re.compile(r'([\d]+),([\d]+),([\d]+),([\d]+),([\d]+),([\d]+)')
        d = re.findall(bus,html)
        lis = []
        for i in range(5):
            lis[i] = d[i]
            str = re.split(',',d[i])
            if str[2] == '2':
                if int(str[3]) < 4425532: #9北泉小区
                    return self.bus_data[str[3]]

    def _get_bus_data(self,url):
        html = urllib2.urlopen(url)
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        # print soup
        name = soup.find_all(name='p', attrs={"id": re.compile(r'BUSSTOPNO_\d*?')})
        for i in name:
            # print i['id'].split('_')[1] + '--' + i.get_text()
            self.bus_data[i] = i.get_text
        return True
