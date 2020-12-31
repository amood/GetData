from core import *


def getActor(jsondata):
    if (jsondata is None) or (len(jsondata.strip()) == 0):
        return 'UNKONWN'
    if ',' or ',  ' in jsondata:
        jsondata = jsondata.replace(',', ' ').replace(',  ', ' ')
    return jsondata


def getlastserialvalue(oldfilename) -> str:
    result = ''
    # 处理含有-和_的数据
    if '-' in oldfilename:
        count = oldfilename.count('-')
        result = oldfilename.split('-')[count]
    if '_' in oldfilename:
        count = oldfilename.count('_')
        result = oldfilename.split('_')[count]

    # 处理CD[数字]-[字母]情况
    # pattern = r'CD\d+-\w+'
    pattern = r'\w+-[a-zA-Z]'
    matchobj = re.search(pattern, oldfilename, re.IGNORECASE)
    if matchobj:
        print(matchobj)

    return result


def get_part(filepath) -> str:

    #去掉路径
    basename = os.path.basename(filepath)

    # 去掉扩展名
    basename = os.path.splitext(basename)[0]

    # 处理文件名中含有多个.的情况
    basename  = re.sub('\.+', '', basename, re.IGNORECASE)

    try:
        # 处理-CD1
        pattern = r'-CD\d+'
        if re.search(pattern, basename):
            return re.findall(pattern, basename)[0]

        pattern = r'-cd\d+'
        if re.search(pattern, basename):
            return re.findall(pattern, basename)[0]
        # 处理-A
        pattern = r'-[a-zA-Z]$'
        if re.search(pattern, basename):
            return re.findall(pattern, basename)[0]
    except:
        print("[-]failed!Please rename the filename again!")
        return ''


def getfilename(filepath, json_data, conf: config.Config) -> str:
    filename = json_data['number'] + '-' + getActor(json_data['actor']) + '-' + json_data['title']

    # if len(serialvalue.strip()) > 0:
    #     filename += '-' + serialvalue

    # 处理文件名超长的问题
    extension = os.path.splitext(filepath)[1]
    if len(filename + extension) > 255:
        if conf.debug():
            print('[!]文件名超长' + filename + extension)
        length = 255 - len(extension)
        filename = filename[:length - 1]

    # 处理系列名称
    part = get_part(filepath)
    if len(part) == 0:
        filename = filename + extension
    else:
        filename = filename + part + extension

    return filename


def core_main_rename(file_path, number_th, conf: config.Config):
    # =======================================================================初始化所需变量
    multi_part = 0
    part = ''
    c_word = ''
    cn_sub = ''

    filepath = file_path  # 影片的路径
    number = number_th
    json_data = get_data_from_json(number, filepath, conf)  # 定义番号

    # Return if blank dict returned (data not found)
    if not json_data:
        return

    if json_data["number"] != number:
        # fix issue #119
        # the root cause is we normalize the search id
        # print_files() will use the normalized id from website,
        # but paste_file_to_folder() still use the input raw search id
        # so the solution is: use the normalized search id
        number = json_data["number"]
    tag = json_data['tag']
    # =======================================================================判断-C,-CD后缀
    if '-CD' in filepath or '-cd' in filepath:
        multi_part = 1
        part = get_part(filepath, conf.failed_folder())
    if '-c.' in filepath or '-C.' in filepath or '中文' in filepath or '字幕' in filepath:
        cn_sub = '1'
        c_word = '-C'  # 中文字幕影片后缀
    if '流出' in filepath:
        liuchu = '流出'

    # 调试模式检测
    if conf.debug():
        debug_print(json_data)

    resultfilename = conf.movie_folder() + '\\' + getfilename(filepath, json_data, conf)
    if conf.debug():
        print('[-]最终结果:' + resultfilename)
    os.rename(filepath, resultfilename)
