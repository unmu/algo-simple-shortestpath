import folium

"""
    此py文件 临时测试用
"""

# mmap = folium.Map()
mmap = folium.Map(location=[30.53, 114.355], zoom_start=12,
                  tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
                  attr='default')
folium.PolyLine([
    [30.533, 114.37],
    [30.53, 114.364],
    [30.525, 114.368]
], color='green').add_to(mmap)

mmap.save('html/test.html')
