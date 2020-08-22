import os
import create_map as map
import clustering as cluster

# 封装一个函数：遍历，循环读取
def deal(data_path, save_path):
    """
    循环 读取 处理 写入
    :param data_path:     存放原数据的文件夹
    :param save_path:     存放处理后数据的文件夹
    :return:                none
    """
    files = os.listdir(data_path)  # 得到文件夹下的所有文件名称
    for file in files:  # 遍历文件夹
        data = data_path + '/' + file  # 构造绝对路径，"\\"，其中一个'\'为转义符
        save = save_path + '/' + file[:-4] + "_map" + ".csv"
        print(data)
        print(save)
        # cluster.cluster(data, save)   # 聚类
        map.box(data, save)             # 路网
        print()


data_path = 'csv/cluster/temp'
save_path = 'csv/map/weekday'
deal(data_path, save_path)
