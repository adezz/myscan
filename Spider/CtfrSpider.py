#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Spider.BaseSpider import *

abs_path = os.getcwd() + os.path.sep

class CrtrSpider(Spider):
    def __init__(self, target):
        super().__init__()
        self.crfr_list = list()
        self.target = target

    def write_file(self, web_lists, target, page):
        workbook = openpyxl.load_workbook(abs_path + str(target) + ".xlsx")
        worksheet = workbook.worksheets[page] # 打开的是证书的sheet
        index = 0
        while index < len(web_lists):
            web = list()
            web.append(web_lists[index]['ssl'])
            web.append(web_lists[index]['submain'])
            worksheet.append(web)
            index += 1
        workbook.save(abs_path + str(target) + ".xlsx")
        workbook.close()

    def spider(self):
        subdomains = []
        resp = requests.get("https://crt.sh/?q=%.{d}&output=json".format(d=self.target))
        if resp.status_code != 200:
            print("[X] Information not available!")
            exit(1)

        for (key, value) in enumerate(resp.json()):
            # subdomains.append(value['name_value'].split('\n'))
            try:
                subdomain_ssl = value['name_value'].split('\n')
                self.crfr_list.append(subdomain_ssl[1])

                # 把 ssl证书 和 子域名 放到一个字典中
                domain_info = {
                    'ssl': subdomain_ssl[0],
                    'submain': subdomain_ssl[1]
                }
            except:
                domain_info = {
                    'ssl': 'None',
                    'submain': subdomain_ssl[0]
                }

                # 一起放到列表中进行存储
            subdomains.append(domain_info)

        # 列表中的字典去重
        subdomains = Common_getUniqueList(subdomains)
        self.write_file(subdomains, self.target, 1)
        return list(set(self.crfr_list))

    def main(self):
        logging.info("Ctfr Spider Start")
        self.spider()
        return list(set(self.crfr_list))

if '__main__' == __name__:
    CrtrSpider(1).main('nbcc.cn')
