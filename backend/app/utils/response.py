from flask import jsonify

def success(data=None, msg="操作成功", code=200):
    return jsonify({
        "code": code,
        "msg": msg,
        "data": data
    }), code

def error(msg="操作失败", code=400, data=None):
    return jsonify({
        "code": code,
        "msg": msg,
        "data": data
    }), code
