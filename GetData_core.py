from WebCrawler import javdb7
from core import *


def getStr(jsondata):
    if (jsondata is None) or (len(jsondata.strip()) == 0):
        return 'UNKONWN'
    if ',' or ',  ' in jsondata:
        jsondata = jsondata.replace(',', ' ').replace(',  ', ' ')
    r = '[’!"#$%&\'()*+,./:;<=>?@[\\]^`{|}~\n。！，…]+'

    jsondata = re.sub(r, '', jsondata, re.IGNORECASE)

    return jsondata


def get_part(filepath) -> str:
    # 去掉路径
    basename = os.path.basename(filepath)

    # 去掉扩展名
    basename = os.path.splitext(basename)[0]

    # 处理文件名中含有多个.的情况
    basename = re.sub(r'\.+', '', basename, re.IGNORECASE)

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

        # 处理-1
        pattern = r'-\d$'
        if re.search(pattern, basename):
            return re.findall(pattern, basename)[0]



    except:
        print("[-]failed!Please rename the filename again!")
    return ''


def getfilename(filepath, json_data, conf: config.Config) -> str:
    filename = json_data['number'] + '-' + getStr(json_data['actor']) + '-' + getStr(json_data['title'])

    # if len(serialvalue.strip()) > 0:
    #     filename += '-' + serialvalue

    # 处理文件名超长的问题
    extension = os.path.splitext(filepath)[1]
    if len(filename + extension) > 255:
        if conf.debug():
            print('[!]文件名超长' + filename + extension)
        length = 255 - len(extension)
        filename = filename[:length - 1]

    # 英文字母转换为大写
    filename = filename.upper()

    # 处理系列名称
    part = get_part(filepath)
    if len(part) == 0:
        filename = filename + extension
    else:
        filename = filename + part + extension

    return filename


def get_data_from_json(file_number, filepath, conf: config.Config):  # 从JSON返回元数据
    """
    iterate through all services and fetch the data
    """

    func_mapping = {
        "airav": airav.main,
        "avsox": avsox.main,
        "fc2": fc2.main,
        "fanza": fanza.main,
        "javdb": javdb.main,
        "javbus": javbus.main,
        "mgstage": mgstage.main,
        "jav321": jav321.main,
        "xcity": xcity.main,
        "javlib": javlib.main,
        "dlsite": dlsite.main,
        "javdb7": javdb7.main,
    }

    # default fetch order list, from the beginning to the end
    sources = conf.sources().split(',')

    # if the input file name matches certain rules,
    # move some web service to the beginning of the list
    if "avsox" in sources and (re.match(r"^\d{5,}", file_number) or
                               "HEYZO" in file_number or "heyzo" in file_number or "Heyzo" in file_number
    ):
        # if conf.debug() == True:
        #     print('[+]select avsox')
        sources.insert(0, sources.pop(sources.index("avsox")))
    elif "mgstage" in sources and (re.match(r"\d+\D+", file_number) or
                                   "siro" in file_number or "SIRO" in file_number or "Siro" in file_number
    ):
        # if conf.debug() == True:
        # print('[+]select fanza')
        sources.insert(0, sources.pop(sources.index("mgstage")))
    elif "fc2" in sources and ("fc2" in file_number or "FC2" in file_number
    ):
        # if conf.debug() == True:
        #     print('[+]select fc2')
        sources.insert(0, sources.pop(sources.index("fc2")))
    elif "dlsite" in sources and (
            "RJ" in file_number or "rj" in file_number or "VJ" in file_number or "vj" in file_number
    ):
        # if conf.debug() == True:
        #     print('[+]select dlsite')
        sources.insert(0, sources.pop(sources.index("dlsite")))

    json_data = {}
    for source in sources:
        try:
            if conf.debug() == True:
                print('[+]select', source)
            json_data = json.loads(func_mapping[source](file_number))
            # if any service return a valid return, break
            if get_data_state(json_data):
                break
        except:
            break

    # Return if data not found in all sources
    if not json_data:
        print('[-]Movie Data not found!')
        # moveFailedFolder(filepath, conf.failed_folder())
        return

    # ================================================网站规则添加结束================================================

    title = json_data.get('title')
    actor_list = str(json_data.get('actor')).strip("[ ]").replace("'", '').split(',')  # 字符串转列表
    actor_list = [actor.strip() for actor in actor_list]  # 去除空白
    release = json_data.get('release')
    number = json_data.get('number')
    studio = json_data.get('studio')
    source = json_data.get('source')
    runtime = json_data.get('runtime')
    outline = json_data.get('outline')
    label = json_data.get('label')
    series = json_data.get('series')
    year = json_data.get('year')

    if json_data.get('cover_small') == None:
        cover_small = ''
    else:
        cover_small = json_data.get('cover_small')

    if json_data.get('trailer') == None:
        trailer = ''
    else:
        trailer = json_data.get('trailer')

    if json_data.get('extrafanart') == None:
        extrafanart = ''
    else:
        extrafanart = json_data.get('extrafanart')

    imagecut = json_data.get('imagecut')
    tag = str(json_data.get('tag')).strip("[ ]").replace("'", '').replace(" ", '').split(',')  # 字符串转列表 @
    actor = str(actor_list).strip("[ ]").replace("'", '').replace(" ", '')

    if title == '' or number == '':
        print('[-]Movie Data not found!')
        # moveFailedFolder(filepath, conf.failed_folder())
        return

    # if imagecut == '3':
    #     DownloadFileWithFilename()

    # ====================处理异常字符====================== #\/:*?"<>|
    title = title.replace('\\', '')
    title = title.replace('/', '')
    title = title.replace(':', '')
    title = title.replace('*', '')
    title = title.replace('?', '')
    title = title.replace('"', '')
    title = title.replace('<', '')
    title = title.replace('>', '')
    title = title.replace('|', '')
    release = release.replace('/', '-')
    tmpArr = cover_small.split(',')
    if len(tmpArr) > 0:
        cover_small = tmpArr[0].strip('\"').strip('\'')

    # ====================处理异常字符 END================== #\/:*?"<>|

    # ===  替换Studio片假名
    studio = studio.replace('アイエナジー', 'Energy')
    studio = studio.replace('アイデアポケット', 'Idea Pocket')
    studio = studio.replace('アキノリ', 'AKNR')
    studio = studio.replace('アタッカーズ', 'Attackers')
    studio = re.sub('アパッチ.*', 'Apache', studio)
    studio = studio.replace('アマチュアインディーズ', 'SOD')
    studio = studio.replace('アリスJAPAN', 'Alice Japan')
    studio = studio.replace('オーロラプロジェクト・アネックス', 'Aurora Project Annex')
    studio = studio.replace('クリスタル映像', 'Crystal 映像')
    studio = studio.replace('グローリークエスト', 'Glory Quest')
    studio = studio.replace('ダスッ！', 'DAS！')
    studio = studio.replace('ディープス', 'DEEP’s')
    studio = studio.replace('ドグマ', 'Dogma')
    studio = studio.replace('プレステージ', 'PRESTIGE')
    studio = studio.replace('ムーディーズ', 'MOODYZ')
    studio = studio.replace('メディアステーション', '宇宙企画')
    studio = studio.replace('ワンズファクトリー', 'WANZ FACTORY')
    studio = studio.replace('エスワン ナンバーワンスタイル', 'S1')
    studio = studio.replace('エスワンナンバーワンスタイル', 'S1')
    studio = studio.replace('SODクリエイト', 'SOD')
    studio = studio.replace('サディスティックヴィレッジ', 'SOD')
    studio = studio.replace('V＆Rプロダクツ', 'V＆R PRODUCE')
    studio = studio.replace('V＆RPRODUCE', 'V＆R PRODUCE')
    studio = studio.replace('レアルワークス', 'Real Works')
    studio = studio.replace('マックスエー', 'MAX-A')
    studio = studio.replace('ピーターズMAX', 'PETERS MAX')
    studio = studio.replace('プレミアム', 'PREMIUM')
    studio = studio.replace('ナチュラルハイ', 'NATURAL HIGH')
    studio = studio.replace('マキシング', 'MAXING')
    studio = studio.replace('エムズビデオグループ', 'M’s Video Group')
    studio = studio.replace('ミニマム', 'Minimum')
    studio = studio.replace('ワープエンタテインメント', 'WAAP Entertainment')
    studio = re.sub('.*/妄想族', '妄想族', studio)
    studio = studio.replace('/', ' ')
    # ===  替换Studio片假名 END

    location_rule = eval(conf.location_rule())

    if 'actor' in conf.location_rule() and len(actor) > 100:
        print(conf.location_rule())
        location_rule = eval(conf.location_rule().replace("actor", "'多人作品'"))
    maxlen = conf.max_title_len()
    if 'title' in conf.location_rule() and len(title) > maxlen:
        shorttitle = title[0:maxlen]
        location_rule = location_rule.replace(title, shorttitle)

    # 返回处理后的json_data
    json_data['title'] = title
    json_data['actor'] = actor
    json_data['release'] = release
    json_data['cover_small'] = cover_small
    json_data['tag'] = tag
    json_data['location_rule'] = location_rule
    json_data['year'] = year
    json_data['actor_list'] = actor_list
    if conf.is_transalte():
        translate_values = conf.transalte_values().split(",")
        for translate_value in translate_values:
            json_data[translate_value] = translate(json_data[translate_value])

    if conf.is_trailer():
        if trailer:
            json_data['trailer'] = trailer
        else:
            json_data['trailer'] = ''
    else:
        json_data['trailer'] = ''

    if conf.is_extrafanart():
        if extrafanart:
            json_data['extrafanart'] = extrafanart
        else:
            json_data['extrafanart'] = ''
    else:
        json_data['extrafanart'] = ''

    naming_rule = ""
    for i in conf.naming_rule().split("+"):
        if i not in json_data:
            naming_rule += i.strip("'").strip('"')
        else:
            naming_rule += json_data.get(i)
    json_data['naming_rule'] = naming_rule
    return json_data


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
