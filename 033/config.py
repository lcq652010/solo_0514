import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'water_meter.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

DEVICE_STATUS = {
    'normal': '正常',
    'fault': '故障',
    'repairing': '维修中',
    'fixed': '已修复'
}

FAULT_STATUS = {
    'pending': '待处理',
    'processing': '处理中',
    'completed': '已完成'
}