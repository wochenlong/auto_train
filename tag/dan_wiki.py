import re
import requests
import urllib.parse
from bs4 import BeautifulSoup

url = "https://danbooru.donmai.us/wiki_pages/list_of_blue_archive_characters"
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    # 使用BeautifulSoup解析网页内容
    soup = BeautifulSoup(response.content, 'html.parser')

    # 查找指定的<div>标签
    wiki_page_body = soup.find('div', id='wiki-page-body')

    if wiki_page_body:
        # 打印<div>标签内的文本
        text = str(wiki_page_body)

        # 定义一个正则表达式模式来匹配形如 "ganyu_(genshin_impact)" 的字符串
        pattern = r'href="/wiki_pages/([^"]*)"'

        # 使用正则表达式查找匹配的部分
        matches = re.findall(pattern, text)

        # 将匹配到的角色名输出为所需形式
        output = ',\n'.join(['"{}"'.format(urllib.parse.unquote(match)) for match in matches])

        text = output

        # 使用正则表达式将所有/wiki_pages/替换为空字符串
        cleaned_text = re.sub("/wiki_pages/", "", text)

        print(cleaned_text)

        # 将结果写入文件
        with open(r'F:\data\all\danganronpa\characters.txt', 'w') as file:
            file.write(cleaned_text)
    else:
        print("没有找到指定的<div>标签")
else:
    print("无法获取网页内容，状态码:", response.status_code)
