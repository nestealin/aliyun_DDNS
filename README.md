# aliyun_DDNS
###阿里云域名解析增删改查。


#脚本前言赘述：
####1, 此脚本已通过3.7.4运行，用来对阿里云云解析增删改查，使用之前请先安装sdk:pip3 install aliyun-python-sdk-core-v3
####2, 手动引入部分请从阿里云github下载，地址：https://github.com/aliyun/aliyun-openapi-python-sdk
####2.1, git clone https://github.com/aliyun/aliyun-openapi-python-sdk.git
####2.2, cd aliyun-openapi-python-sdk/aliyun-python-sdk-alidns/
####2.3, python3 setup.py install


#执行逻辑：
####1, 判定只执行nestealin.com域名；
####2, 获取线上当前解析和记录信息；
####3, 与线下域名文件比对；
####4.1, 域名在本地存在，线上记录不存在，添加记录；
####4.2, 域名在本地不存在，线上记录存在，删除记录（泛域名解析除外）；
####4.3, 解析不对，更新解析；