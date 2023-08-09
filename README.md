# Crawler_Apprentice
## Try to figure web-crawler out
### 用这个仓库，放一些爬虫练手的代码


***novel_download.py*** 是一个简陋的爬取小说小程序
声明：仅作为学习、练习使用，未用于获取不正当利益。所爬取小说已经在官网全订正版。

**本机使用的Anaconda虚拟环境，在指定路径创建虚拟环境的指令：**  ```conda create --prefix /path/env_name env_name python=python的版本号  ```
(**如果不指定路径的话：** ```conda create --name env_name python=python的版本号)```    
**激活conda虚拟环境：**  ```conda activate path/env_name```    
***novel_download.py*** 所需的依赖：使用```pip install 依赖包名称``` 安装对应的依赖
- ```requests```  *(用于向网页发送请求，获取响应)*
- ```bs4```  *(用于将网页返回的html报文解析成DOM结构树的形式，生成BeautifulSoup对象)*
- ```tqdm```  *(用于在终端展示出进度条)*
- ```pymongo```  *(用于操作MongoDB数据库，如果不需要存入数据库，可以不装这个包，把文件里的对应代码段删掉就行)*
