# -*- coding: utf-8 -*-
import os
import re
import io
import argparse

regex_url = re.compile('(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-zA-Z0-9]+([\-\.]{1}[a-zA-Z0-9]+)*\.[a-z0-9]{2,5}(:[0-9]{1,5})?(\/.*)?')
regex_ipv4 = re.compile('(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[1-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])')
regex_ipv6 = re.compile('^(?:(?:[0-9A-Fa-f]{1,4}:){6}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|::(?:[0-9A-Fa-f]{1,4}:){5}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){4}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){3}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,2}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){2}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,3}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}:(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,4}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,5}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}|(?:(?:[0-9A-Fa-f]{1,4}:){,6}[0-9A-Fa-f]{1,4})?::)$')
list_extension = ['.php', '.json', '.txt', '.ctp', '.log']
black_ip = ['127.0.0.1']

def get_url(file):
    try:
        if (('.php' in str(file)) or ('.json' in str(file)) or ('.txt' in str(file)) or ('.ctp' in str(file)) or ('.log' in str(file))): # change extensions here
            ip = []
            url = []
            for i, line in enumerate(io.open(file, 'r+', encoding="utf-8")):
                for match1 in re.finditer(regex_url, line):
                    url.append(str('Found url on line %s: %s' % (i+1, match1.group())))
                for match2 in re.finditer(regex_ipv4, line):
                    ip.append(str('Found ip on line %s: %s' % (i+1, match2.group())))
            write_log(ip, url, file)
    except Exception as ex:
        print ex
    
    # try:
    #     for exten in list_extension:
    #         if exten in str(file):
    #             ip = []
    #             url = []
    #             for i, line in enumerate(io.open(file, 'r+', encoding="utf-8")):
    #                 for match in re.finditer(regex_url, line):
    #                     url.append(str('Found on line %s: %s' % (i+1, match.group())))
    #                 for match in re.finditer(regex_ipv4, line):
    #                     ip.append(str('Found on line %s: %s' % (i+1, match.group())))
    #             write_log(ip, url, file)
    #         else:
    #             continue
    # except Exception as ex:
    # print ex
     
def write_log(ip, url, file):
    with open('log_url_ip.txt', 'a+') as f:
        f.write('\n')
        f.write('===================={0}======================\n'.format(file))
        for i in ip:
            f.write(i)
            f.write('\n')
        for u in url:
            f.write(u)
            f.write('\n')
        f.write('\n')

def main():

    # parser = argparse.ArgumentParser(description='Get URL and IP from source code')
    # parser.add_argument('-p', help='Path Folder')
    # args = parser.parse_args()
    path = str(raw_input('Path: '))
    # path = str(args.p)
    for root, dirs, files in os.walk(path):
        for i in files:
            print str(os.path.join(root, i))
            get_url(str(os.path.join(root, i)))

if __name__ == "__main__":
    main()
