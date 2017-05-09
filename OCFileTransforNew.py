# -*- coding:utf-8 -*-
import time
import requests
import os


# 返回权限说明
def rightWord(className, projectName, creator, rightOwner):
    createTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    year = time.strftime('%Y年', time.localtime(time.time()))
    right = '/**\n * ' + className + '\n * ' + projectName + '\n *\n * Created by ' + creator + ' on ' + createTime + '\n * Copyright © ' + year + ' ' + rightOwner + ' All rights reserved.\n */\n\n'
    return right


def requestForNet(requestUrl, data):
    response = requests.post(requestUrl, data)
    if response.status_code == 404:
        print('无响应')
    responseJson = response.json()
    return responseJson


# json转换为oc格式m文件字符串
def translateJsonForOc(jsonObject):
    dictionary = dict(jsonObject)
    allItems = list(dictionary.items())
    itAllItems = iter(allItems)
    finalPropertyString = ''
    while True:
        try:
            item = next(itAllItems)
            noteForProperty = '/**' + str(item[1]) + '*/ \n'
            propertyWord = item[0]
            propertyString = '@property(nonatomic, copy) NSString *'
            currentProperty = noteForProperty + propertyString + propertyWord + '\n'
            finalPropertyString = finalPropertyString + currentProperty
        except StopIteration:
            finalPropertyString = finalPropertyString + '\n\n'
            break
    return finalPropertyString


# 传入类名，项目名，创建者，权限所有者，以及需要写入的oc属性（json格式），生成m文件
def wiriteOcModelTofile(className, projectName, creator, rightOwner, jsonObject):
    # 如果是子目录，问加你啊必须存在才行
    path = os.environ['HOME']
    basePath = path + '/' + className
    try:
        os.makedirs(basePath)
    except FileExistsError:
        print('文件夹已存在')

    # basePath = os.path.dirname(sys.argv[0])
    pathM = basePath + '/' + className + '.m'
    pathH = basePath + '/' + className + '.h'
    outputM = open(pathM, 'w')
    outputH = open(pathH, 'w')
    createTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    year = time.strftime('%Y年', time.localtime(time.time()))
    # 权限文档
    right = '/**\n * ' + className + '\n * ' + projectName + '\n *\n * Created by ' + creator + ' on ' + createTime + '\n * Copyright © ' + year + ' ' + rightOwner + ' All rights reserved.\n */\n\n'

    # import根据h和m文件不同而不同
    importStringM = '#import "' + className + '.h"\n\n\n'
    importStringH = '#import <Foundation/Foundation.h>\n\n\n'

    # interface的文字
    interfaceStringM = '@interface ' + className + ' ()\n\n'
    interfaceStringH = '@interface ' + className + ' : NSObject\n\n'

    # 属性（目前全部为私有变量，可以在生成后移到h文件中）
    ocProperty = translateJsonForOc(jsonObject)

    # 实现文字，仅M文件有
    implementationString = '@implementation ' + className + '\n\n'

    # @end
    endString = '@end\n\n'

    # 权限+头文件导入+interface+OC属性声明+@end+实现+@end
    finalStringM = right + importStringM + interfaceStringM + ocProperty + endString + implementationString + endString
    # h文件稍简洁
    finalStringH = right + importStringH + interfaceStringH + endString

    try:
        outputM.write(finalStringM)
        outputH.write(finalStringH)
        outputM.close()
        outputH.close()
        command = 'open ' + basePath
        os.system(command)
    except:
        print('写入错误')
    return


# 写入的路径，以类名为子路径存放在用户目录
def pathForWrite(className):
    path = os.environ['HOME']
    writePath = path + '/' + className
    try:
        os.makedirs(writePath)
    except FileExistsError:
        print('文件夹已存在')
    finally:
        command = 'open ' + writePath
        print(command)
        os.system(command)
