# encoding: utf-8
import json
import math
import csv

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import DBSCAN
from sklearn import metrics


# DBSCAN 聚类算法
def cluster(data_path, save_path):
    """
    封装：聚类
    :param data_path:   原数据路径       例：......./...csv
    :param save_path:   关键点数据存储路径
    :return:
    """
    data = data_path
    save = save_path
    X = []
    with open(data, "r") as f:
        reader = csv.reader(f)
        for line in reader:
            tmp = [line[2], line[3]]
            X.append(tmp)
        X = np.array(X, np.float)

    print(X)

    def calc_distance(lat1, lon1, lat2, lon2):
        theta = lon1 - lon2
        dist = math.sin(math.radians(lat1)) * math.sin(math.radians(lat2)) + math.cos(math.radians(lat1)) * math.cos(
            math.radians(lat2)) * math.cos(math.radians(theta))
        if dist - 1 > 0:
            dist = 1
        elif dist + 1 < 0:
            dist = -1
        dist = math.acos(dist)
        dist = math.degrees(dist)
        miles = dist * 60 * 1.1515
        return miles

    def distance(p1, p2):
        lat1, lon1 = p1
        lat2, lon2 = p2
        distance = calc_distance(lat1, lon1, lat2, lon2) * 1.609344
        return distance

    distance_matrix = squareform(pdist(X, (lambda u, v: distance(u, v))))
    db = DBSCAN(eps=0.05, min_samples=3, metric='precomputed')
    labels = db.fit_predict(distance_matrix)

    # Plot
    fig = plt.figure(1)
    col = 'k'
    plt.plot(X[:, 0], X[:, 1], '*', markerfacecolor='k', markeredgecolor='k', markersize=5)

    core_samples_mask = np.zeros_like(labels, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True

    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    fig = plt.figure(2)
    center_point = []
    heatmap_point = []

    f_cluster = open(save, 'w', newline='')

    for k, col in zip(unique_labels, colors):
        if k == -1:
            col = 'k'

        class_member_mask = (labels == k)
        xy = X[class_member_mask & core_samples_mask]

        print("%d reference points contain %d points" % (k, len(xy)))
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=14)

        print("center pos %f %f" % (np.mean(xy[:, 0]), np.mean(xy[:, 1])))
        f_cluster.write(str(k) + ',' + str(len(xy)) + ',' + str(np.mean(xy[:, 0])) + ',' + str(np.mean(xy[:, 1])) + '\r')
        center_point.append([np.mean(xy[:, 1]), np.mean(xy[:, 0])])
        heatmap_point.append({"lng": np.mean(xy[:, 1]), "lat": np.mean(xy[:, 0]), "count": len(xy[:, 1])})

    plt.title('DBSCAN :Estimated number of clusters: %d' % n_clusters_)
    print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, labels))
    plt.show()
    print("Done.")
