import csv
import pandas as pd
import numpy as np


def box(key_points, save_path):
    """
    封装完整的匹配写入新的路网算法
    :param key_points: 关键点路径    例 'G:\python\项目\测试数据/c_021718.csv'
    :param save_path:  保存路径（带名字） 例 'G:/python/项目/测试数据/tiem-7-8.csv'
    :return:
    """
    data_test = key_points
    write_test = save_path

    # 文件路径  测试关键点(聚类得）  原路网数据   测试路网数据（节选部分）   写入文件测试路径
    # data_test = 'G:\python\项目\测试数据/c_021718.csv'
    data_starterk = 'csv/mMap.csv'
    # test_starterk = 'G:\python\项目/path.csv'
    # write_test = 'G:\python\项目\测试数据/t_021718.csv'

    # 从关键点中读取数据
    # 存储读取的经纬点
    a = []
    with open(data_test, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            a.append([row[2], row[3]])
        print(a)

    # 保存新的数据  要写入新的路网中
    write = []
    # 查看结果  查看有多少数据匹配上了，匹配项有多少个点
    res = []

    # f = open(data_starterk, 'r')

    # 打开原路网数据，进行关键点匹配，降低权重
    with open(data_starterk, 'r') as f:
        # 跳过首行
        next(f)
        reader = csv.reader(f)
        for row in reader:
            # 匹配项计数
            count = 0
            # 将路由列表化，便于匹配
            geometry = row[5]
            geometry = geometry.split(";")
            # 遍历每一行路由
            for i in geometry:
                i = i.split(":")
                # 匹配，误差范围0.0003，30 m
                for num in a:
                    if float(num[0]) - 0.00015 <= float(i[0]) <= float(num[0]) + 0.00015 and \
                            float(num[1]) - 0.00015 <= float(i[1]) <= float(num[1]) + 0.00015:
                        count += 1
            # 降低权重，用原length/(count+1)  一条路由中匹配到的点越多，降低权重越多，但始终为正数
            if count != 0:
                res.append(count)
                row[3] = float(row[3]) / float(count + 1)
            write.append(row)

    print("匹配上的数据次数：" + str(res))
    print("匹配上的数据总数：", res.__len__())
    print("需要写入新的路网的数据量：", write.__len__())

    # 写入，新的路网信息
    # 1. 创建文件对象
    f = open(write_test, 'w', encoding='utf-8', newline='')

    # 2. 基于文件对象构建 csv写入对象
    csv_writer = csv.writer(f)

    # 3. 构建列表头
    csv_writer.writerow(["LinkID", "FromNode", "ToNode", "Length", "RoadClass", "Geometry"])
    # count = 0
    for row in write:
        csv_writer.writerow(row)
        count += 1
        print("写入的行号：", format(count))
    f.close()

    return str(key_points+" finished！")
