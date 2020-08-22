import csv
import math
import folium
from heapq import *
from datetime import datetime


# 根据输入经纬度(lon, lat)匹配起始结点或终止结点
def searchPoint(lon, lat, dataFilePosition, Pointtype):
    with open(dataFilePosition, 'r') as f:
        next(f)     # 跳过首行
        dis = math.inf      # dis初始化为无穷大
        reader = csv.reader(f)
        # 遍历Geometry以找到距离(lon, lat)最近的点M(lonM, latM)，并及时更新对应dis和idPoint
        for row in reader:
            geo = str(row[5]).split(';')
            for i in geo:
                # 获取到点M (lonM, latM)
                lonM = str(i).split(':')[0]
                latM = str(i).split(':')[1]
                # 计算M到输入点之间的距离 （如下计算公式只作比较作用，不深究其单位）
                tmpDis = ((lon-float(lonM))*10000)**2 + ((lat-float(latM))*10000)**2
                if tmpDis < dis:
                    dis = tmpDis     # tmpDis比dis小就更新dis,同时更新idPoint
                    if Pointtype == 0:      # 起点
                        idPoint = row[2]
                    else:                   # 终点
                        idPoint = row[1]
    # print(dis)
    return int(idPoint)


# 根据特定的路网，初始化结点距离数据graph
def initGraph(fileLoc):
    graph = {1: {1: 0}}     # 用字典存储数据
    for row in csv.reader(open(fileLoc), delimiter=','):
        if row[0] == "LinkID":      # 跳过第一行
            continue
        if int(row[1]) not in graph.keys():
            graph[int(row[1])] = {}
        if int(row[2]) not in graph.keys():
            graph[int(row[2])] = {}
        graph[int(row[1])][int(row[2])] = float(row[3])
        if int(row[1]) not in graph[int(row[2])].keys():
            graph[int(row[2])][int(row[1])] = math.inf  # inf无穷大，结点间不可达
        else:
            graph[int(row[2])][int(row[1])] = float(row[2])
    print(graph)
    return graph


def initDistance(graph, st):
    distance = {st: 0}
    for vertex in graph:
        if vertex != st:
            distance[vertex] = math.inf
    return distance
# 最短路经算法
def Dijkstra(graph, s):
    queue = []     # 队列
    heappush(queue, (0, s))
    seen = set()
    seen.add(s)
    parent = {s: None}
    distance = initDistance(graph, s)
    while len(queue) > 0:
        pair = heappop(queue)  # 一对的
        dist = pair[0]
        vertex = pair[1]
        seen.add(vertex)
        nodes = graph[vertex].keys()
        for w in nodes:
            if w not in seen:
                if dist + graph[vertex][w] < distance[w]:
                    heappush(queue, (dist + graph[vertex][w], w))
                    parent[w] = vertex
                    distance[w] = dist + graph[vertex][w]
    return parent, distance


# input_info = '2020-06-03,00:19:59'
input_info = input("请输入日期及时间，格式如“2020-06-06,00:19:59”：")
data_time = datetime.strptime(input_info, "%Y-%m-%d,%H:%M:%S")
# print(data_time)
week = data_time.isoweekday()
hour = data_time.hour
print("星期" + str(week) + "，" + str(hour) + "时")
# 根据星期和时刻确定待使用的路网文件名
if week < 6:
    hourStrL = str(hour)
    if len(hourStrL) == 1:
        hourStrL = '0'+hourStrL
    hourStrR = str(hour+1)
    if len(hourStrR) == 1:
        hourStrR = '0'+hourStrR
    mapFile = 'weekday/0408' + hourStrL + hourStrR + '_map.csv'
else:
    hourStrL = str(int(hour/2)*2)
    if len(hourStrL) == 1:
        hourStrL = '0'+hourStrL
    hourStrR = str(int(hour/2)*2+2)
    if len(hourStrR) == 1:
        hourStrR = '0'+hourStrR
    mapFile = 'weekend/0203' + hourStrL + hourStrR + '_map.csv'
# print(hourStrL, hourStrR)
print("路网文件：")
print(mapFile)

fileLoc = 'csv/map/'+mapFile

print("待输入的经纬度范围：lon: 116.152675~116.409291, lat: 39.885149,40.0413")
fromGPS = input("请输入起点经纬度，格式如“116.186651,39.917878”：")
lonFromT = float(fromGPS.split(',')[0])
latFromT = float(fromGPS.split(',')[1])
# lonFromT = 116.303614
# latFromT = 39.952674
fromNode = searchPoint(lonFromT, latFromT, fileLoc, 0)
toGPS = input("请输入起点经纬度，格式如“116.303614,39.952674”：")
lonToT = float(toGPS.split(',')[0])
latToT = float(toGPS.split(',')[1])
# lonToT = 116.186651
# latToT = 39.917878
toNode = searchPoint(lonToT, latToT, fileLoc, 1)
print(fromNode, toNode)

graph = initGraph(fileLoc)
parent, distance = Dijkstra(graph, fromNode)
print(parent)

ployList = []   # 记录从起点到终点依此经过的经纬度点
count = 0       # 记录经过路段Geometry的个数

print("依次经过的经纬度点如下：")
while parent[toNode] is not None:
    fromN = parent[toNode]
    for row in csv.reader(open('csv/mMap.csv'), delimiter=','):
        if row[0] == "LinkID":
            continue
        if str(row[1]) == str(fromN) and str(row[2]) == str(toNode):
            count += 1
            geo = str(row[5]).split(';')
            geo.reverse()
            for i in geo:
                lonTmp = float(str(i).split(':')[0])
                latTmp = float(str(i).split(':')[1])
                ployList.append([latTmp, lonTmp])
                print(latTmp, lonTmp)
    toNode = fromN

print("路段总数：" + str(count))
if count == 0:
    print("未找到可达路径")
    exit(0)

mmap = folium.Map(location=[39.9632245, 116.280983], zoom_start=11,
                  tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
                  attr='default')
folium.PolyLine(ployList, color='green').add_to(mmap)
folium.Marker([latFromT, lonFromT],  tooltip='起点', icon=folium.Icon(color='blue')).add_to(mmap)
folium.Marker([latToT, lonToT], tooltip='终点', icon=folium.Icon(color='red')).add_to(mmap)
mmap.add_child(folium.LatLngPopup())
mmap.save('html/trajectory.html')
