from app import app

if __name__ == '__main__':
    print("=" * 60)
    print("传统珐琅彩鼻烟壶定制订单管理系统")
    print("=" * 60)
    print("服务启动中...")
    print("访问地址: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)