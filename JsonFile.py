import json

defaultRightJson = {'className': 'JFModel',
                    'projectName': 'JFProject',
                    'creator': 'Jeffrey',
                    'rightOwner': 'YourCompanyName'}

defaultDataJson = {'requestUrl': 'http://ip.taobao.com/service/getIpInfo.php', }


# 根据字典和文件名写入到json文件中
def writeDicToFile(dictionary: dict, fileName: str):
    # 写入json格式文件
    fileNameFinal = fileName + '.json'
    jsonFile = open(fileNameFinal, 'w')
    json.dump(dictionary, jsonFile)
    jsonFile.close()
    return


# 读取一个json文件，返回json
def readJsonFile(fileName: str):
    fileNameFinal = fileName + '.json'
    jsonFile = open(fileNameFinal, 'r')
    readJson = json.load(jsonFile)
    jsonFile.close()
    return readJson


# 把文件写入right.json
def setRightJson(right: dict):
    writeDicToFile(right, 'right')


# 根据参数写入right.json
def setRightJsonWithParameter(className: str, projectName: str, creator: str, rightOwner: str):
    jsonForWrite = {'className': className,
                    'projectName': projectName,
                    'creator': creator,
                    'rightOwner': rightOwner}
    setRightJson(jsonForWrite)


# 读取right.json文件，返回rightjson
def getRightJson():
    try:
        rightJson = readJsonFile('right')
        return rightJson
    except FileNotFoundError:
        print('文件不存在，写入默认right：')
        print(defaultRightJson)
        setRightJson(defaultRightJson)
        return getRightJson()


# 获取dataJson.json文件，返回dataJson，里面可以添加参数
def getDataJson():
    try:
        dataJson = readJsonFile('data')
        return dataJson
    except FileNotFoundError:
        print('文件不存在，写入默认data：')
        print(defaultDataJson)
        setDataJson(defaultDataJson)
        return getDataJson()


# 把文件写入right.json
def setDataJson(data: dict):
    writeDicToFile(data, 'data')


# 更新data里的字段或者增加字段
def updateDataJson(key: str, value: str):
    dataJson = getDataJson()
    dataJson[key] = value
    setDataJson(dataJson)


def updateRequestUrl(requestUrl: str):
    updateDataJson('requestUrl', requestUrl)

