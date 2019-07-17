#!/usr/bin/ python3
# -*- coding: utf-8 -*-
# Author: nestealin
# Created: 2019-07-18


import urllib
from aliyunsdkcore.client import *
from aliyunsdkcore.request import CommonRequest
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import *
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import *
from aliyunsdkalidns.request.v20150109.DeleteDomainRecordRequest import *
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import *


# 需要检测的主域名
DomainName = '**主域名**'
# 阿里云的AccessKey_ID
AccessKey_ID = '**阿里云的AccessKey_ID**'
# 阿里云的Access_Key
Access_Key = '**阿里云的Access_Key**'
# 请求方式
client = AcsClient(AccessKey_ID, Access_Key, 'cn-hangzhou')
# 声明api请求版本及方式
request = CommonRequest()
request.set_accept_format('json')
request.set_domain('alidns.aliyuncs.com')
request.set_method('POST')
request.set_version('2015-01-09')
# 本地域名文档路径
DomainListPath = '**本地域名文档路径**'


'''
脚本前言赘述：
1, 此脚本已通过3.7.4运行，用来对阿里云云解析增删改查，使用之前请先安装sdk:pip3 install aliyun-python-sdk-core-v3
2, 手动引入部分请从阿里云github下载，地址：https://github.com/aliyun/aliyun-openapi-python-sdk
2.1, git clone https://github.com/aliyun/aliyun-openapi-python-sdk.git
2.2, cd aliyun-openapi-python-sdk/aliyun-python-sdk-alidns/
2.3, python3 setup.py install

API传参说明：
名称	        类型	    是否必须	描述
Action	    String	是	    操作接口名，系统规定参数，取值：UpdateDomainRecord
RecordId	String	是	    解析记录的ID，此参数在添加解析时会返回，在获取域名解析列表时会返回，可从“DescribeDomainRecords”这个API获取
RR	        String	是	    主机记录，如果要解析@.exmaple.com，主机记录要填写”@”，而不是空
Type	    String	是	    解析记录类型，参见解析记录类型格式
Value	    String	是	    记录值
TTL	        Long	否	    生存时间，默认为600秒（10分钟），参见TTL定义说明
Priority	Long	否	    MX记录的优先级，取值范围[1,10]，记录类型为MX记录时，此参数必须
Line	    String	否	    解析线路，默认为default。参见解析线路枚举
------------------------------ 以 上 适 用 于 增 、 删 、 改 域 名 操 作 传 参 -----------------------------------------------
以下适用于获取解析记录列表(DescribeDomainRecords)
名称	            类型	    是否必须	描述
Action	        String	是	    操作接口名，系统规定参数，取值：DescribeDomainRecords
DomainName	    String	是	    域名名称
PageNumber	    Long	否	    当前页数，起始值为1，默认为1
PageSize	    Long	否	    分页查询时设置的每页行数，最大值500，默认为20
RRKeyWord	    String	否	    主机记录的关键字，按照”%RRKeyWord%”模式搜索，不区分大小写
TypeKeyWord	    String	否	    解析类型的关键字，按照全匹配搜索，不区分大小写
ValueKeyWord	String	否	    记录值的关键字，按照”%ValueKeyWord%”模式搜索，不区分大小写

执行逻辑：
1, 判定只执行一个主域名；
2, 获取线上当前解析和记录信息；
3, 与线下域名文件比对；
4.1, 域名在本地存在，线上记录不存在，添加记录；
4.2, 域名在本地不存在，线上记录存在，删除记录（泛域名解析除外）；
4.3, 解析不对，更新解析；
'''


def get_record_id(RRKeyWord):
    global RecordId
    request.set_action_name('DescribeDomainRecords')
    # 这里写死了主域名
    request.add_query_param('DomainName', DomainName)
    request.add_query_param('RRKeyWord', RRKeyWord)
    request.add_query_param('TypeKeyWord', 'A')
    response = client.do_action_with_exception(request)
    encode_json = json.loads(response)
    # print(encode_json)
    # 需要获取这个RecordId
    RecordId = encode_json['DomainRecords']['Record']
    if RecordId:
        return RecordId[0]['RecordId']
    else:
        print('域名' + RRKeyWord + '.' + DomainName + '找不到Rcord信息。')


# 更新域名解析
def update_domain_record(RRKeyWord, Value):
    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')
    request.set_Type("A")
    request.set_RR(RRKeyWord)
    request.set_Value(Value)
    # 根据RecordID决定更新那个主域名的主机记录
    request.set_RecordId(get_record_id(RRKeyWord))
    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))


# 添加域名解析记录
def add_domain_record(RRKeyWord, Value):
    request = AddDomainRecordRequest()
    request.set_accept_format('json')
    request.set_Value(Value)
    request.set_Type("A")
    request.set_RR(RRKeyWord)
    request.set_DomainName(DomainName)
    # 输出格式为byte，需要转成str输出为宜
    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))


# 删除域名解析记录
def del_domain_record(RRKeyWord):
    try:
        record_id = get_record_id(RRKeyWord)
        # print(RecordId)
        if record_id != 0:
            request = DeleteDomainRecordRequest()
            request.set_RecordId(record_id)
            # 输出格式为byte，需要转成str输出为宜
            response = client.do_action_with_exception(request)
            print('域名' + RRKeyWord + '.' + DomainName + ',\nRcordID为:' + str(response,
                                                                             encoding="utf-8").split(':')[1].split(',')[0].split('"')[1] + '\nA记录已被删除。')
        else:
            print('域名' + RRKeyWord + '.' + DomainName + '找不到Rcord信息，删除失败。')

    except Exception as e:
        print(e)


# 获取当前线上解析记录列表,同时可获得RecordID
def domain_resolve_records_aliyun():
    '''
    返回三组数据：
    [[A记录],[解析IP],{"A记录": "解析IP"}]
    '''
    try:
        request = DescribeDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(DomainName)
        response = client.do_action_with_exception(request)
        # print(response)
        json_data = json.loads(str(response, encoding='utf-8'))
        # print(json_data)
        # return json_data
        total_data = []
        # 现有解析中的A记录
        domain_a_record_list_aliyun = []
        # 现有解析中的A记录IP
        ip_list_aliyun = []
        resolve_dict_aliyun = {}
        # 检查出有IP变化的域名，加入更新列表
        for i in json_data['DomainRecords']['Record']:
            ip_list_aliyun.append(i['Value'])
            domain_a_record_list_aliyun.append(i['RR'])
            resolve_dict_aliyun[i['RR']] = i['Value']
        total_data.append(domain_a_record_list_aliyun)
        total_data.append(ip_list_aliyun)
        total_data.append(resolve_dict_aliyun)

        return total_data

    except Exception as e:
        print(e)


# 获取服务器外网IP
def get_internet_ip():
    with urllib.request.urlopen('http://www.3322.org/dyndns/getip') as response:
        html = response.read()
        ip = str(html, encoding='utf-8').replace("\n", "")
        # print (ip)
    return ip


# 读取现有域名列表
def get_domain_list():
    domain_list_tmp = open(DomainListPath).readlines()
    domain_list = []
    for i in domain_list_tmp:
        if DomainName in i:
            domain_list.append(i.split('\n')[0])
        else:
            print('域名' + i + '存在异常，请手动检查。')
    return domain_list


# 提取本地A记录
def get_A_record_local():
    a_record_local = []
    for i in get_domain_list():
        a_record_local.append(i.split('.')[0])
    # print(A_Record_Local)
    return a_record_local


# 核心函数
def main():
    # 获取本机外网IP
    Value = get_internet_ip()
    for i in get_domain_list():
        if i.split('.')[1] + '.' + i.split('.')[2] == DomainName:
            print('已检测到域名%s为正确域名，继续检测...' % (i))
        else:
            print('文本含有非%s域名，请手动排查:%s' % (DomainName, i))
    print('✅ 文本内全为%s域名，继续执行...' % DomainName)

    # 需要添加的A记录列表，本地与线上对比，线上缺少的
    add_queue_list = list(set(get_A_record_local()).difference(
        set(domain_resolve_records_aliyun()[0])))
    if add_queue_list:
        print('‼️ 发现线上缺少%s条A记录解析:%s，准备进行添加。' %
              (len(add_queue_list), ','.join(add_queue_list)))
        for i in add_queue_list:
            print('正在添加域名%s.%s解析到%s...' % (i, DomainName, Value))
            print(add_domain_record(i, Value))
    else:
        print('✅ 线上%s域名并无缺失解析，继续执行...' % DomainName)

    # 需要删除的A记录列表，本地与线上对比，线上多出来的
    del_queue_list = list(set(domain_resolve_records_aliyun()[
        0]).difference(set(get_A_record_local())))
    if del_queue_list:
        for i in del_queue_list:
            if i == '*':
                print('✅ 泛域名解析不操作删除，继续执行...')
            else:
                print('‼️ 发现线上多出%s条A记录解析:%s，准备进行删除' %
                      (len(del_queue_list), ','.join(del_queue_list)))
                print('正在执行删除域名%s.%s的记录...' % (i, DomainName))
                print(del_domain_record(i))
    else:
        print('线上%s域名并无多余域名解析，继续执行...' % DomainName)

    # 更新域名解析不正确
    for i in get_A_record_local():
        if domain_resolve_records_aliyun()[2][i] == Value:
            print('✅ 域名%s解析正常，无需更新。' % (i + '.' + DomainName))
        else:
            print('正在执行更新域名%s.%s的解析...' % (i, DomainName))
            print(update_domain_record(i, Value))
    print('✅ 所有域名操作执行完毕。')


if __name__ == "__main__":
    print("请注意！本脚本只会修改%s域名下的A记录！！！" % DomainName)
    try:
        main()
    except Exception as e:
        print(e)
