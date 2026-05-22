from datetime import datetime
from app import app
from models import db, Device, ExceptionReport, WorkOrder


def init_test_data():
    with app.app_context():
        print('开始初始化测试数据...')
        
        device1 = Device(
            device_code='RFID-001',
            device_name='A区入口RFID识别终端',
            wharf_code='WH-001',
            crane_location='Q01#桥吊',
            sn_code='SN202401001',
            work_zone='A作业区',
            location='港口A区入口闸口',
            install_date=datetime(2024, 1, 15).date(),
            status='normal',
            signal_strength=85,
            remarks='主要负责A区入口集装箱识别'
        )
        
        device2 = Device(
            device_code='RFID-002',
            device_name='B区出口RFID识别终端',
            wharf_code='WH-001',
            crane_location='L05#龙门吊',
            sn_code='SN202401002',
            work_zone='B作业区',
            location='港口B区出口闸口',
            install_date=datetime(2024, 2, 20).date(),
            status='fault',
            signal_strength=30,
            remarks='需要检修读卡器'
        )
        
        device3 = Device(
            device_code='RFID-003',
            device_name='C区堆场RFID识别终端',
            wharf_code='WH-002',
            crane_location='L08#龙门吊',
            sn_code='SN202401003',
            work_zone='C作业区',
            location='港口C区堆场入口',
            install_date=datetime(2024, 3, 10).date(),
            status='signal_error',
            signal_strength=25,
            remarks='信号较弱，需检查天线'
        )
        
        device4 = Device(
            device_code='RFID-004',
            device_name='D区码头RFID识别终端',
            wharf_code='WH-002',
            crane_location='Q03#桥吊',
            sn_code='SN202401004',
            work_zone='D作业区',
            location='港口D区码头岸桥',
            install_date=datetime(2024, 4, 5).date(),
            status='offline',
            signal_strength=0,
            remarks='网络连接中断'
        )
        
        db.session.add_all([device1, device2, device3, device4])
        db.session.flush()
        
        exception1 = ExceptionReport(
            device_id=device2.id,
            exception_type='miss_read',
            description='连续5次漏读RFID标签',
            container_code='CONT-20240501-001',
            rfid_data='EPC:1234567890,TID:0987654321'
        )
        
        exception2 = ExceptionReport(
            device_id=device3.id,
            exception_type='wrong_read',
            description='读取数据错误，疑似误读',
            container_code='CONT-20240501-002',
            rfid_data='EPC:ABCDEF123456,TID:654321FEDCBA'
        )
        
        exception3 = ExceptionReport(
            device_id=device4.id,
            exception_type='comm_interrupt',
            description='设备通信中断，心跳超时',
            container_code=None,
            rfid_data=None
        )
        
        exception4 = ExceptionReport(
            device_id=device1.id,
            exception_type='power_failure',
            description='设备供电异常，电压波动超过阈值',
            container_code=None,
            rfid_data=None
        )
        
        db.session.add_all([exception1, exception2, exception3, exception4])
        db.session.flush()
        
        order1 = WorkOrder(
            order_no='WO202405160001',
            device_id=device2.id,
            exception_id=exception1.id,
            title='RFID-002读卡器故障维修',
            description='设备连续无法读取RFID标签，需检查硬件设备',
            priority='high',
            status='pending',
            assign_to='张工',
            created_by='系统管理员'
        )
        
        order2 = WorkOrder(
            order_no='WO202405160002',
            device_id=device3.id,
            exception_id=exception2.id,
            title='RFID-003信号异常排查',
            description='信号强度异常偏低，需检查天线及周围环境',
            priority='medium',
            status='processing',
            assign_to='李工',
            started_at=datetime.now(),
            created_by='系统管理员'
        )
        
        order3 = WorkOrder(
            order_no='WO202405160003',
            device_id=device4.id,
            title='RFID-004网络恢复',
            description='设备离线，需排查网络连接问题',
            priority='urgent',
            status='pending',
            assign_to='王工',
            created_by='系统管理员'
        )
        
        db.session.add_all([order1, order2, order3])
        db.session.commit()
        
        print('测试数据初始化完成!')
        print(f'  - 设备: {Device.query.count()} 台')
        print(f'  - 异常记录: {ExceptionReport.query.count()} 条')
        print(f'  - 工单: {WorkOrder.query.count()} 个')


if __name__ == '__main__':
    init_test_data()
