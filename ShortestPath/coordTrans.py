from __future__ import division
from math import pi, sqrt, sin, cos
import pandas as pd
import csv
"""
    将原T-dive数据集中的经纬度的坐标系进行转换
    地球坐标系转火星坐标系
    保留位于mMap.csv路网中的出租车经纬度数据
    处理后的出租车数据 <id,时间,修正后的经纬度> 存储至新csv文件
    
    注：选取1-1000的出租车txt文件
"""

a = 6378245.0
ee = 0.00669342162296594323

# World Geodetic System ==> Mars Geodetic System
def transformC(wgLat, wgLon):
    """
    transform(latitude,longitude) , WGS84
    return (latitude,longitude) , GCJ02
    """
    if outOfChina(wgLat, wgLon):
        mgLat = wgLat
        mgLon = wgLon
        return
    dLat = transformLat(wgLon - 105.0, wgLat - 35.0)
    dLon = transformLon(wgLon - 105.0, wgLat - 35.0)
    radLat = wgLat / 180.0 * pi
    magic = sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * pi)
    dLon = (dLon * 180.0) / (a / sqrtMagic * cos(radLat) * pi)
    mgLat = wgLat + dLat
    mgLon = wgLon + dLon
    return mgLon, mgLat


def outOfChina(lat, lon):
    if lon < 72.004 or lon > 137.8347:
        return True
    if lat < 0.8293 or lat > 55.8271:
        return True
    return False


def transformLat(x, y):
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * sqrt(abs(x))
    ret += (20.0 * sin(6.0 * x * pi) + 20.0 * sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * sin(y * pi) + 40.0 * sin(y / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * sin(y / 12.0 * pi) + 320 * sin(y * pi / 30.0)) * 2.0 / 3.0
    return ret


def transformLon(x, y):
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * sqrt(abs(x))
    ret += (20.0 * sin(6.0 * x * pi) + 20.0 * sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * sin(x * pi) + 40.0 * sin(x / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * sin(x / 12.0 * pi) + 300.0 * sin(x / 30.0 * pi)) * 2.0 / 3.0
    return ret


if __name__ == "__main__":
    f1 = open('csv/segment/weekday/04082324.csv', 'w')        # 'a+':可读写，不清除已写内容; 'w':写，清除已写内容
    time1 = '23:00:00'
    time2 = '24:00:00'
    # 举个例子如latt和lont
    latt = 39.85155
    lont = 116.69169
    print(latt, lont)
    print(transformC(latt, lont))

    for aa in csv.reader(open('csv/path.csv')):     # path.csv存储的是出租车数据文本所在的位置
        f = open(str(aa)[2:-2])     # 获取出租车文本aa的路径
        data = pd.read_csv(f, names=['ID', 'time', 'lat', 'lon'])
        # 去掉重复项（id、时间、经纬度完全重复） 默认保留重复数据出现的第一行数据
        data = data.drop_duplicates(subset=['ID', 'time', 'lat', 'lon'])
        # 去掉包含空值的行数据
        # axis = 0 行操作, how = 'any' 只要有空值就删除，(all 为全为空值才删除)
        # inplace = False 为返回新数据集（默认）（True 为在源数据集上操作）
        data = data.dropna(axis=0, how='any')
        # 按时间顺序排序 -> 同时导致data['name'] = data[0]
        data = data.set_index('time')
        # 获取一段时间范围内的数据
        nData1 = data['2008-02-04 ' + time1:'2008-02-04 ' + time2]
        nData2 = data['2008-02-05 ' + time1:'2008-02-05 ' + time2]
        nData3 = data['2008-02-06 ' + time1:'2008-02-06 ' + time2]
        nData4 = data['2008-02-07 ' + time1:'2008-02-07 ' + time2]
        nData5 = data['2008-02-08 ' + time1:'2008-02-08 ' + time2]
        # 暂存nData中的数据
        nData = nData1.append(nData2).append(nData3).append(nData4).append(nData5)
        print(nData)
        nData.to_csv('D:/data/tmp.csv')
        for row in csv.reader(open('D:/data/tmp.csv'), delimiter=','):
            if row[3] == 'lon':     # 读取到标题则跳过
                continue
            # 不在北京范围内，比如有的lat lon是 0.0 0.7
            if float(row[2]) < 115.0 or float(row[2]) > 118.0 or float(row[3]) < 39.0 or float(row[3]) > 42.0:
                continue
            # 经纬度转换
            lat = str(transformC(float(row[3]), float(row[2]))[0])
            lon = str(transformC(float(row[3]), float(row[2]))[1])
            print(lat, lon)
            # 找到starTrek内的点
            if 116.152675 <= float(lat) <= 116.409291 and 39.885149 <= float(lon) <= 40.0413:
                print('可供收录的点：' + row[1] + ',' + row[0] + ',' + lat + ',' + lon + '\r')
                f1.write(row[1] + ',' + row[0] + ',' + lat + ',' + lon + '\r')

