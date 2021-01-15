# kerl-machine-learn

**Anaconda(环境管理工具)**

****1.查看基本信息****：
 
 `conda info`
![condaInfo](./img/conda-info.png) 


****2.新建虚拟环境****：

`conda create -n machine-lean python=3.6`
   
 ![condaCreate](./img/conda-create.png) 
 

****3.查看虚拟环境****：

`conda env list`

 ![condaEnv](./img/conda-env.png) 
 
****4.激活环境****：

`activate your_env_name`

![condaActivate](./img/conda-activate.png) 

****5.退出环境****：

`deactivate`

![condaDeactivate](./img/conda-deactivate.png) 

****6.配置国内镜像****:

`conda config --add channels http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/`

`conda config --add channels http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge `

`conda config --add channels http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/`

**Python**

***Pip(依赖包管理工具)***

****1.查看环境已安装的依赖包****：

`pip list`
![pipList](./img/pip-list.png)

  可以使用`python -m pip install --upgrade pip`更新pip
  
****2.导出依赖包****：

*****2.1 只导出安装包信息*****：

`pip freeze > requirements.txt`

![pipFreeze](./img/pip-freeze.png)

*****2.2 导出安装包whl文件*****：

`pip download -r requirements.txt
`
![pipDownload](./img/pip-download.png)

****3.导入依赖包****：

联网情况下：

`pip install -r requirements.txt`

没联网情况下：

`pip install -r requirements.txt -d local_dir`


****5.安装依赖包****:

******5.1 联网安装******:

`pip install Django==1.7`

******5.2 离线安装******:

需要预先下载whl文件

`pip install *.whl
`

需要预先下载tar包

`pip install Flask-WTF-0.10.0.tar.gz
`

**Django**
  
*****0.项目vs应用*****

`项目和应用有啥区别？应用是一个专门做某件事的网络应用程序——比如博客系统，或者公共记录的数据库，或者简单的投票程序。项目则是一个网站使用的配置和应用的集合。项目可以包含很多个应用。应用可以被很多个项目使用。
`

*****1.查看当前安装的Django版本*****

`python -m django --version
`

*****2.运行服务*****

`python manage.py runserver 0.0.0.0:port`

0.0.0.0表示可以被其他机器访问

`python manage.py runserver`

默认绑定到8000端口 

*****3.创建应用*****

`python manage.py startapp polls`

目录如下:

![pollsDir](./img/polls-dir.png)

可能会出现name 'os' is not defined.解决方法:在setting.py文件中增加 import os

*****4.定义视图*****

******4.1******
在polls/view.py中追加如下代码：

![pollsViewIndex](./img/poll-view-index.png)

******4.2******
在polls目录下,新建urls.py文件,并追加如下代码：

![pollsUrls](./img/polls-urls.png)

******4.3******
在项目中同名的根目录下的urls.py追加如下代码：

![rootUrls](./img/root-urls.png)

******4.4******
接收参数

*******4.4.1 GET*******

在polls/views.py中追加如下代码

![pollViewsDetail](./img/polls-views-detail.png)

在polls/urls.py中追加如下代码:

![pollUrlsDetail](./img/polls-urls-detail.png)

其中,int是参数的数据类型,question_id对应views方法的参数名

*******4.4.1 POST*******

在polls/views.py追加如下代码:

![pollsPost](./img/polls_request_post.png)

在polls/urls.py追加如下代码：
![pollsUrlPost](./img/poll-urls-post.png)

其中json是一个模块,需要import json



*****5.Model*****

******5.1安装依赖******

1. 安装pymysql依赖包

   `pip install pymysql`
2. 在项目同名根目录的_init_.py添加如下代码:

![initMySql](./img/mysql_init.png)

******5.2配置参数******

在项目同名目录下settings.py追加如下代码(需要提前创建数据库):

![mysqlConfig](./img/polls-model-database.png)

******5.3生成MODEL类******

在具体应用下面的models.py定义class类,我这里的应用是polls。
在polls目录下的models.py追加如下代码:

![questionModel](./img/question_model.png)

Django中的model类需要继承models.Model类。

具体FiledType参考
`https://docs.djangoproject.com/zh-hans/2.0/ref/models/fields/`
 

******5.4生成数据库表******

 (1) 生成数据库表的命令是

`python manage.py migrate`

注意：migrate 命令只会为在 INSTALLED_APPS 里声明了的应用进行数据库迁移。



 (2)在项目同名根目录下的settings.py文件追加如下代码：
 
 ![installedApps](./img/installed_apps_config.png)
 
 (3) 进行迁移
 
    生成迁移文件 makemigrations
    
 ![makemigrations](./img/makemigrations.png)
     
     真正迁移
     
 ![migrate](./img/migrete.png)
 
 (4)查看数据库中的表
 
   会生成自身需要的表
  ![tables](./img/tables.png)
    
 
  (5) 注意，每次在models中新增字段的时候，都需要重新执行第三步



******5.5 实际应用******

*******5.5.1 保存数据*******

在polls/views.py文件中追加如下代码:

![saveQuestion](./img/saveQuestion.png)


*******5.5.2 查询数据*******

在polls/views.py文件追加如下代码:

![getQuestionById](./img/getById.png)


![page](./img/page1.png)



*******5.5.3 导出以及导入数据*******

conda env export > environment.yaml // 导出当前环境的包信息

conda env create -f environment.yaml // 用配置文件创建新的虚拟环境

