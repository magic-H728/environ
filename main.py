# 导入flask框架
import json
import time
import requests
import pymysql
from flask import Flask, request, send_file

# 创建flask应用对象
# __name__表示当前的模块名字

app = Flask(__name__)


# 解决跨域问题
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


# /接口
@app.route('/', methods=['GET'])
def index():
    return 'Hello World!'


# 上传图片接口
@app.route('/uploadImg', methods=['POST'])
def uploadImg():
    # 将请求转发到另一个服务器
    url = 'http://150.158.18.74:4999/uploadImg'
    files = {'img': request.files.get('img')}
    imgURL = requests.post(url, files=files).text
    print(imgURL)
    return imgURL


# 获取图片接口 /environ/img?159123456789.jpg
# @app.route('/getImg', methods=['GET'])
# def getImg():
#     # 将请求转发到另一个服务器
#     url = 'http://150.158.18.74:4999/getImg'
#     args = request.args
#     img = requests.get(url, params=args).content
#     return img

# # 获取?所有参数
# args = request.args
# # 判断参数是否为空
# if args is None:
#     return None
# # 获取图片名
# imgName = str(request.args).split("'")[1]
# # 使用flask的send_file方法发送图片
# return send_file('./environ/img/' + imgName)


# 数据上传接口
@app.route('/post', methods=['POST'])
def post():
    # 将请求转发到另一个服务器
    url = 'http://150.158.18.74:4999/post'
    data = request.get_json()
    requests.post(url, json=data)
    return "Yes"


# 连接数据库
def connectDB():
    # 创建连接
    conn = pymysql.connect(
        host='150.158.18.74',
        port=3306,
        user='bio-bank',
        password='123456',
        db='bio-bank',
        charset='utf8'
    )
    # 创建游标
    cursor = conn.cursor()
    return conn, cursor


def insertDB(data):
    # 连接数据库
    conn, cursor = connectDB()

    # 插入数据
    special_info_json = json.dumps(data['special_info'])
    cursor.execute("INSERT INTO sample (id, special_info) VALUES (%s, %s)", (data['id'], special_info_json))

    # 提交
    conn.commit()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()


# 数据库查询
def selectDB():
    # 连接数据库
    conn, cursor = connectDB()

    # 全部查询
    sql = 'select * from environ'
    # 执行sql语句
    cursor.execute(sql)
    # 获取查询结果
    result = cursor.fetchall()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return result


# 启动flask程序
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4999, debug=False)
