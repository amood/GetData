import os
import sys

from AV_Data_Capture import get_number, argparse_function
from GetData_Config import GetDataConfig
from GetData_core import *


def renname_data(file_path: str, c: config.Config, debug):
    # Normalized number, eg: 111xxx-222.mp4 -> xxx-222.mp4
    # n_number = get_number(debug, file_path)
    n_number = get_number(debug, file_path)

    try:
        print("[!]Making Data for [{}], the number is [{}]".format(file_path, n_number))
        core_main_rename(file_path, n_number, c)
        print("[*]======================================================")
    except Exception as err:
        print("[-] [{}] ERROR:".format(file_path))
        print('[-]', err)


def movie_lists(root, escape_folder, c: config.Config):
    for folder in escape_folder:
        if folder in root:
            return []
    total = []
    file_type = c.media_type().upper()
    dirs = os.listdir(root)
    for entry in dirs:
        f = os.path.join(root, entry)
        if os.path.isdir(f):
            total += movie_lists(f, escape_folder, c)
        elif (len(os.path.splitext(f)[1].upper()) > 0) and (os.path.splitext(f)[1].upper() in file_type):
            total.append(f)
    return total


def exectute():
    version = '4.3.2'

    # Parse command line args
    single_file_path, config_file, custom_number, auto_exit = argparse_function(version)

    # Read config.ini

    conf = GetDataConfig(path=config_file)

    os.chdir(os.getcwd())

    movielist = movie_lists(conf.movie_folder(), re.split("[,，]", conf.escape_folder()), conf)

    count = 0
    count_all = str(len(movielist))
    print('[+]Find', count_all, 'movies')
    if conf.debug():
        print('[+]' + ' DEBUG MODE ON '.center(54, '-'))
    if conf.soft_link():
        print('[!] --- Soft link mode is ENABLE! ----')
    for movie_file in movielist:  # 遍历电影列表 交给core处理
        count = count + 1
        percentage = str(count / int(count_all) * 100)[:4] + '%'
        print('[!] - ' + percentage + ' [' + str(count) + '/' + count_all + '] -')
        renname_data(movie_file, conf, conf.debug())

    print("[+]All finished!!!")
    if conf.auto_exit():
        sys.exit(0)
    if auto_exit:
        sys.exit(0)
    input("Press enter key exit, you can check the error message before you exit...")
    sys.exit(0)


if __name__ == '__main__':
    exectute()
