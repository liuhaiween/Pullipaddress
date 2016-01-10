#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time,json,os,sys
from bisect import bisect
from IPy import IP
##省，在函数judgment_area()使用，主要用来判断是不是中国地区，和拼接出省
REGION=['山东省','山西省','河北省','河南省','湖北省','湖南省','广东省','黑龙江省',
'辽宁省','浙江省','安徽省','江苏省','福建省','甘肃省','江西省','云南省','贵州省','四川省','青海省','陕西省'
,'吉林省','海南省']

##直辖市，同时，拼接出直辖市
ZXS=['北京','天津','重庆','上海']
##一些自治区，用于拼接
ZZQ=['内蒙古','西藏','新疆','宁夏','广西','台湾','澳门','香港']

##国外地区，用来判断国外城市
##可按list格式添加
#例如GW=['ac']，那么就能能在函数judgment_area()判断出带有ac的地区
#GW=['a州'] ，result['isp']="123a州xxx"，那么出来的地点就是123a州，仅对国外城市有效
#
GW=['州','市','首尔','釜山','市','仁川','北海道','东京','大手','纽约','墨尔本',"华盛顿"]


##网络运营商
#可按字典格式添加
#例如 移动 包含了'移动','铁通','网通'，那么通过函数judgment_area()来完成输出移动isp
#假若刚刚新增一家gogo的公司做了一个 f的isp,恰好数据库中更新出了这个isp的关键字是gogo_isp，那么就要在字典里添加'f':['go']
##ISP
ISP={
    "电信":['电信'],
    "移动":['移动','铁通','网通'],
    "联通":['联通'],
    "哥伦布市Dod网络中心":['哥伦布市Dod网络中心'],
    "Orange":['Orange'],
    'IBM公司':['IBM公司'],
    '通用公司':['通用电气公司'],
    'CZ8.NET':['CZ88.NET'],
    'Level_3通讯公司':['德市Level'],
    '美国哥伦布信息中心':['哥伦布市DoD网络信息'],
    '美国国防部':['国防部网'],
    '谷歌公司':['谷歌公司'],
    'Apple':['Apple公司'],
    'Inc':['Inc']
}

_LIST1, _LIST2 = [], []
_INIT = False

ip2int = lambda ip_str: reduce(lambda a, b: (a << 8) + b, [int(i) for i in ip_str.split('.')])

def _init():
    global _LIST, _INIT
    if not _INIT:
        for l in open('ipdata.txt', 'rb'):
            ip1, ip2 = l.split()[:2]
            addr = ' '.join(l.split()[2:])
            ip1, ip2 = ip2int(ip1), ip2int(ip2)
            _LIST1.append(ip1)
            _LIST2.append((ip1, ip2, addr))
        _INIT = True
    
def ip_from(ip):
    _init()
    i = ip2int(ip)
    idx = bisect(_LIST1, i)
    assert(idx > 0)
    if len(_LIST1) <= idx:
        return u'unknown ip address %s' % ip
    else:
        frm, to ,addr = _LIST2[idx - 1]
        if frm <= i <= to:
            return addr
        else:
            return u'unknown ip address %s' % ip


def put_ip2file(data):

    if os.path.exists("ip-info"):
        with open("ip-info/%s.txt" %data['title'],'a') as f:
            ip=data['ip']
            country=data['country']
            if data['region'] == "":
                region="null"
            else:
                region=data['region']

            isp=data['isp']
            if isp == "":
                isp ="null"
            f.write("%s %s %s %s " %(ip,country,region,isp)+'\n')
            print "%s %s %s %s " %(ip,country,region,isp)
    else:
        os.mkdir("ip-info")


##国外，港澳台统一isp为null
def judgment_area(data):
    area_data = data['place']
    result={}
    result['country'] = "系统国家"
    result['region'] = "系统地方"
    result['isp']="null"
    result['title']=data['title']
    result['ip']=data['ip']

    f=0
    ##判断省
    # print area_data,area_data in REGION
    # if area_data in REGION and f==0:

    #     result['country'] = "中国"
    #     result['region'] = data['place'].split("省")[0]+"省"
    #     f=1

    for j in REGION:
        if j in area_data and f==0:
            result['country'] = "中国"
            result['region'] = data['place'].split("省")[0]+"省"
            f=1
    ##判断直辖市
    for x in ZXS:
        if x in area_data and f==0:
            result['country'] = "中国"
            result['region'] = x+"市"
            f=1
    for i in ZZQ:
        if i in area_data and f==0:
            result['country'] = "中国"
            result['region'] = i+"区"
            f=1
    ##这里就是国外了,地区
    if f==0:
        result['country']=area_data##赋值国家
        result['isp']="null"
        for i in GW:
            if i in data["isp"]:
                #print data
                #print i in data['isp']
                result['region'] = data['isp'].split(i)[0]+i
                break
            else:
                result['region'] = "未知地方(省or州)"

    ##ISP
    for i in ISP:
        for j in ISP[i]:
            if j in data['isp']:
                result['isp'] = i
    # print result
    put_ip2file(result)
    #print result['country'],result['region'],result['isp'],data['ip'],result['title']










def produced_legal_ip(s_ip,e_ip):
    p_startingip=s_ip.split(".")
    p_endingip=e_ip.split(".")
    p_title="%s-%s" %(p_startingip[0],p_endingip[0])

    #*.x.x.255
    
    for i in range(int(p_startingip[0]),int(p_endingip[0])+1):
        #print i
        #x.*.x.255
        for j in range(int(p_startingip[1]),int(p_endingip[1])+1):
            #print "%d.%d" %(i,j)
            #x.x.*.255
            for n in range(int(p_startingip[2]),int(p_endingip[2])+1):
                ips="%d.%d.%d.255" %(i,j,n)
                if IP(ips).iptype()=="PUBLIC":
                    # print ips
                    ip_dir={"ip":ips,"title":p_title}
                    #print "判断%s为公网IP**" %ips
                    date = ip_from(ips)
                    result={}
                    result['ip']=ips
                    try:
                        result['place']=date.split(" ")[0]
                        result['isp']=date.split(" ")[1]
                        result['title']=p_title
                        judgment_area(result)
                    except Exception, e:
                        result['place']=date.split(" ")[0]
                        result['isp']="未知"
                        result['title']=p_title
                        judgment_area(result)
                else:
                    pass

    
if __name__ == '__main__':
    startingip=raw_input("输入起始ip:")
    endingip=raw_input("输入终止ip:")
    produced_legal_ip(startingip,endingip)
