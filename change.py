import yaml
import os
import re

def getFileInfo(fileName):
    fileInfo = fileName.replace('/', '.').split('.')
    l = len(fileInfo) - 1
    return {'file': fileInfo[l-1].replace('/', ''),\
            'ext': fileInfo[l].replace('/', '')}

def getFileData(fileName):
    file = open(fileName, 'r')
    data = file.read()
    file.close()
    return data

def writeFileData(fileName, fileData):
    file = open(fileName, 'w')
    file.write(fileData)
    file.close()

def changePhpData(fileName):
    data = getFileData(fileName)
    for replace in currentData['replace']:
        data = re.sub(r'' + replace['regex'], replace['replace'], data)
    writeFileData(fileName, data)
    print('Перезаписал %s' % (fileName))

def changeYmlData(fileName):
    data = getFileData(fileName)
    data = yaml.load(data)
    if 'api' in data:
        if isinstance(data['api'], list):
            if isinstance(currentData['api'], list):
                for currentV in currentData['api']:
                    if not (currentV in data['api']):
                        data['api'].append(currentV)
            else:
                add = True
                for v in data['api']:
                    if v == currentData['api']:
                        add = False
                        break
                if add:
                    data['api'].append(currentData['api'])
                    
        else:
            data['api'] = currentData['api']
    else:
        data['api'] = currentData['api']

    writeFileData(fileName, yaml.dump(data))
    print('Перезаписал plugin.yml')

def checkDir(path):
    if os.path.isdir(path):
        for name in os.listdir(path):
            if path[len(path)-1] != '/':
                path += '/'
            checkDir(path + name)
    else:
        ext = getFileInfo(path)
        if ext['ext'] == 'php':
            changePhpData(path)
        elif ext['ext'] == 'yml' or ext['ext'] == 'yaml':
            if ext['file'] == 'plugin':
                changeYmlData(path)

currentData = getFileData('settings.yml')
currentData = yaml.load(currentData)
print('Обрабатываю...')
checkDir('./')
print('Я закончил')
