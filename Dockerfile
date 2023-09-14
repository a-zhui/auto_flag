# 设置基础镜像为 Python 3.10.1
FROM python:3.10.1

LABEL authors="bocai"

# 在容器中创建并切换到工作目录
WORKDIR /app

# 将当前目录下的所有文件复制到容器中的工作目录
COPY . .

# 安装项目依赖,设置阿里云软件源
RUN  sed -i s@/security.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list && sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list

#安装opencv依赖的共享库
RUN apt-get update && apt-get install libgl1 -y
#安装python依赖,安装dlib时需要编译，这一部可能较为耗时
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/


# 容器对外暴露的端口号（根据具体项目需要进行修改）
EXPOSE 7860

# 容器启动时执行的命令,是以”/bin/sh -c”的方法执行的命令。
CMD uvicorn --host 0.0.0.0 --port 7860 main:app





