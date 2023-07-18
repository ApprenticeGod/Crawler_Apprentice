# 本机对应的虚拟环境是index，激活指令：conda activate c:\ZSJ\index，python版本为3.10
# 此程序通过某个网站爬取无广告的小说，作为练习爬虫的简单实践
# 有两种储存方式，一种是保存为本地的txt文件，另一种是保存至本地的MongoDB数据库，可通过函数的参数进行保存模式的切换
# 可用

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from pymongo import MongoClient

# 定义并初始化数据库类
class mongodb:

    def __init__(self,host,db,port = 27017):
        #:param host: str mongodb地址
        #:param db: str 数据库
        #:param port: int 端口,默认为27017
        host = host
        db = db
        self.port = port
        client = MongoClient(host=host,port=port)
        self.db = client[db]

    def insert_one(self,table,dic):
        #:param table: str 数据库中的集合
        #:param dic: dict 要插入的字典
        #:return: 返回包含一个ObjectId类型的对象
        collection = self.db[table]
        rep = collection.insert_one(dic)
        return rep

    def insert_many(self,table,lists):
        #:param table: str 数据库中的集合
        #:param dic: dict 要插入的列表，列表中的元素为字典
        #:return: 返回包含多个ObjectId类型的列表对象
        collection = self.db[table]
        rep = collection.insert_many(lists)
        return rep

# 存入数据库的字典列表
def save_text(id,title,text):
    dic_chapter={'id':id,'title':title,'text':text}
    db_list.append(dic_chapter)
    return db_list

# 存入mongoDB数据库
def save_DB(database,collection):
    db = mongodb(host='localhost',db = database)
    rep = db.insert_many(collection,db_list) 
    for i in rep.inserted_ids:
        print(i)
    print(r'小说已保存至MongoDB数据库!')

 # 将小说文本保存到txt文件中
def save_txt(file_path,Novel_text):
    #保存的文件路径
    file_path=file_path  
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(Novel_text))
    print(r'小说已保存为txt!')


# 小说内容爬虫
def text_crawler(web_url,novel_url,mode='txt'):
    if mode=='txt':
        global novel_text
    elif mode=='db':
        # 数据库字典
        global db_list
        db_list=[]
        id=0    

    # 设置请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    # 请求小说目录页面
    web_url = web_url      # 小说网站
    novel_url=novel_url    # 具体小说的目录路径，不同小说不同后两段数字
    response = requests.get(web_url+novel_url, headers=headers)
    response.encoding = 'utf-8'

    # 解析目录页面
    soup = BeautifulSoup(response.text, 'html.parser')
    chapter_list = soup.find_all('dd')
    novel_text = []

    # 遍历章节列表，显示下载进度
    for chapter in tqdm(chapter_list, desc='Downloading', unit='chapter'):
        #id=id+1
        chapter_title = chapter.a.text.strip()
        chapter_url = web_url + chapter.a['href']
        
        # 请求章节页面
        chapter_response = requests.get(chapter_url, headers=headers)
        chapter_response.encoding = 'utf-8'
        
        # 解析章节页面
        chapter_soup = BeautifulSoup(chapter_response.text, 'html.parser')
        chapter_content = chapter_soup.find('div', id='content')

        # 提取章节内容
        if chapter_content is not None:
            #  删除<p>标签，广告
            chapter_content.p.clear()
            # 处理剩余内容
            processed_content = chapter_content.text.strip()
            novel_text.append(chapter_title)
            novel_text.append(processed_content)
            # 如果要使用数据库存储文件，则将文本以字典形式放入列表
            if mode=='db':
                save_text(id,chapter_title,processed_content)

# 主函数，程序运行入口（养成习惯）
def main():
    #'db'将小说保存在mongDB数据库中，'txt'将小说保存在txt文件中
    save_Mode=input('请选择储存模式:\n')  # 键盘输入txt，保存为txt文件；键盘输入db，保存为数据库数据。默认为txt保存模式
    novel_name='杀死长生者.txt'           # 根据自己下载小说，自行命名
    text_crawler(web_url='https://www.ibiquges.com',novel_url='/118/118033/',mode=save_Mode)
    if save_Mode=='txt':
        save_txt(file_path=r'C:/Users/admin/Desktop/'+novel_name,Novel_text=novel_text)
    elif save_Mode=='db':
        # 数据集合collection用小说书名命名就行
        save_DB(database='Novel',collection='shasi')

# 如果当前活动文件为本文件，则执行主函数。（可写可不写，养成习惯）
if __name__=='__main__':
    main()

