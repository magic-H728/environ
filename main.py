# 导入flask框架
import json
import time

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
    # 获取图片
    img = request.files.get('img')
    # filename为年+月+日+时+分+秒+图片名
    img.filename = str(time.strftime("%Y%m%d%H%M%S", time.localtime())) + '.jpg'
    print(img.filename)
    # 保存图片
    img.save('./environ/img/' + img.filename)
    # 拼接图片URL
    # imgURL = 'http://environ.magic-H.top/getImg?' + img.filename

    imgURL = 'http://150.158.18.74:4999/getImg?' + img.filename
    # 返回图片URL
    return imgURL


# 获取图片接口 /environ/img?159123456789.jpg
@app.route('/getImg', methods=['GET'])
def getImg():
    # 获取?所有参数
    args = request.args
    # 判断参数是否为空
    if args is None:
        return None
    # 获取图片名
    imgName = str(request.args).split("'")[1]
    # 使用flask的send_file方法发送图片
    return send_file('./environ/img/' + imgName)


# 数据上传接口
@app.route('/post', methods=['POST'])
def post():
    data = request.get_json()

    SQLData = {}
    SQLData['id'] = data['id']
    SQLData['special_info'] = data
    print(SQLData)
    insertDB(SQLData)
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
    app.run(host='0.0.0.0', port=80, debug=False)
