# -*- coding:UTF-8 -*-

import PIL.Image as Image
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def transform_sensor_data(sensor_data):
    '''
    将跌倒数据转化成图像数据
    :param sensor_data: 长度为1200的数组
    :return:
    '''
    # 初始大小为3*400的矩阵。3为RGB通道
    transform_data = np.zeros(shape=[3,400],dtype=np.int)
    # re = np.zeros(shape=[3,400],dtype=np.float)

    for i in range(400):
        # 传感器数据大小敢为-20~20，需要将其值拓展为0~255的数值
        transform_data[0][i] = (sensor_data[3*i] + 20) * 5 # R通道，传感器x值
        transform_data[1][i] = (sensor_data[3*i+ 1] + 20) * 5 # G通道，传感器y值
        transform_data[2][i] = (sensor_data[3*i+ 2] + 20) * 5 # B通道，传感器z值
        #
        # re[0][i] = (sensor_data[3 * i] )  # R通道，传感器x值
        # re[1][i] = (sensor_data[3 * i + 1])   # G通道，传感器y值
        # re[2][i] = (sensor_data[3 * i + 2])   # B通道，传感器z值
    #
    # x = np.arange(400)
    # plt.plot(x, transform_data[0], label='x')
    # plt.plot(x, transform_data[1], label='y')
    # plt.plot(x, transform_data[2], label='z')
    # plt.show()
    #
    # plt.plot(x, re[0], label='x')
    # plt.plot(x, re[1], label='y')
    # plt.plot(x, re[2], label='z')
    #
    # plt.show()

    transform_data = transform_data.reshape([3,20,20])
    return transform_data

def data2image(transform_data,num):
    '''
    将规范化后的传感器数据转化为图像数据
    :param transform_data: 规范后的数据
    :param num: 图像编号
    :return: 生成好的图像数据
    '''
    if transform_data.shape != (3,20,20):
        print('需要转化的数据类型不匹配，错误shape=',transform_data.shape)
        return None

    r = Image.fromarray(transform_data[0],'L')#.convert('L')
    g = Image.fromarray(transform_data[1],'L')#.convert('L')
    b = Image.fromarray(transform_data[2],'L')#.convert('L')

    image = Image.merge('RGB',(r,g,b))
    image.save('/home/tony/git_project/fall_down_detection/data/'+str(num) + '.png','png')


    return image



if __name__=='__main__':

    fall_data = pd.read_csv('../data/fall_data.csv')

    num = fall_data.label.size

    for i in range(num):
        sensor_data = fall_data.iloc[i:i+1, 1:1201].values.reshape([1200, 1])
        transform_data = transform_sensor_data(sensor_data)
        data2image(transform_data, i)
