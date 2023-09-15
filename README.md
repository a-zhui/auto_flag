# 人脸自动贴国旗
> 使用opencv + dilb,通过dilb获取人脸关键点，然后简单的图像处理实现在右脸上贴国旗，刚好配合gradio写一个简单的demo
> ![img.png](images/img.png) 
> [gitee仓库地址](https://gitee.com/bocai123/auto_flag)


## 使用方式一：python虚拟环境
> 安装 miniconda/anaconda
```bash
##构建虚拟环境
conda create -n auto_flag python:3.10
conda activate auto_flag
git clone https://gitee.com/bocai123/auto_flag
cd auto_flag
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

```bash
##启动服务
uvicorn --host 0.0.0.0 --port 7860 main:app
```




## 使用方式二：docker
> 使用docker build构建镜像
```bash
##启动服务
git clone https://gitee.com/bocai123/auto_flag
cd auto_flag
docker build -t auto_flag .
```
>PS： 这里docker镜像构建的过程中在安装dilb时可能较为耗时,因为dilb编译较为耗时,等待2～3分钟即可
```bash
##启动服务
docker run -p 7860:7860 -d --rm --name auto_flag auto_flag:latest
```
>如果镜像构建失败,也可以使用dockerhub上的镜像,具体如下
> 
> 

```bash
##启动服务
docker run -p 7860:7860 -d --rm --name auto_flag bocai123/auto_flag:V1.0
```




