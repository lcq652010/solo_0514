from app import app, db, Device, Fault, MaintenanceRecord
from datetime import datetime, date, timedelta

def init_demo_data():
    with app.app_context():
        db.create_all()
        print("数据库表创建成功！")
        print("正在初始化演示数据...")

        if Device.query.count() == 0:
            device1 = Device(
                device_code='WM001',
                device_name='智能水表-A区1号楼',
                device_model='NB-IoT-Smart-V2.0',
                communication_mode='NB-IoT',
                area='A区',
                pipeline='一号线',
                install_location='A区1号楼1单元101',
                install_date=date(2024, 1, 15),
                commissioning_date=date(2024, 2, 1),
                last_upload_time=datetime.now(),
                status='normal'
            )

            device2 = Device(
                device_code='WM002',
                device_name='智能水表-A区2号楼',
                device_model='LoRa-Water-Meter-V1.5',
                communication_mode='LoRa',
                area='A区',
                pipeline='一号线',
                install_location='A区2号楼2单元202',
                install_date=date(2024, 2, 20),
                commissioning_date=date(2024, 3, 10),
                last_upload_time=datetime.now() - timedelta(hours=2),
                status='fault'
            )

            device3 = Device(
                device_code='WM003',
                device_name='智能水表-B区1号楼',
                device_model='4G-Smart-Water-V3.0',
                communication_mode='4G',
                area='B区',
                pipeline='二号线',
                install_location='B区1号楼3单元303',
                install_date=date(2024, 3, 25),
                commissioning_date=date(2024, 4, 5),
                last_upload_time=datetime.now() - timedelta(hours=1),
                status='repairing'
            )

            device4 = Device(
                device_code='WM004',
                device_name='智能水表-C区商业楼',
                device_model='NB-IoT-Commercial-V1.0',
                communication_mode='NB-IoT',
                area='C区',
                pipeline='三号线',
                install_location='C区商业楼主管道',
                install_date=date(2024, 4, 10),
                commissioning_date=date(2024, 4, 20),
                last_upload_time=datetime.now(),
                status='normal'
            )

            device5 = Device(
                device_code='WM005',
                device_name='智能水表-B区2号楼',
                device_model='4G-Smart-Water-V3.0',
                communication_mode='4G',
                area='B区',
                pipeline='二号线',
                install_location='B区2号楼1单元101',
                install_date=date(2024, 5, 1),
                commissioning_date=date(2024, 5, 15),
                last_upload_time=datetime.now() - timedelta(days=2),
                status='fault'
            )

            device6 = Device(
                device_code='WM006',
                device_name='智能水表-C区住宅楼',
                device_model='LoRa-Water-Meter-V1.5',
                communication_mode='LoRa',
                area='C区',
                pipeline='三号线',
                install_location='C区2号楼2单元',
                install_date=date(2024, 5, 10),
                commissioning_date=date(2024, 5, 25),
                last_upload_time=datetime.now(),
                status='fixed'
            )

            db.session.add_all([device1, device2, device3, device4, device5, device6])
            db.session.commit()
            print("添加了6个设备")

        if Fault.query.count() == 0:
            device2 = Device.query.filter_by(device_code='WM002').first()
            device3 = Device.query.filter_by(device_code='WM003').first()
            device4 = Device.query.filter_by(device_code='WM004').first()
            device5 = Device.query.filter_by(device_code='WM005').first()

            fault1 = Fault(
                work_order_no=Fault.generate_work_order_no(),
                device_id=device2.id,
                fault_type='数据采集异常',
                fault_category='sensor',
                priority='high',
                fault_desc='水表数据无法正常上传，显示离线状态，影响居民用水监控',
                reporter='张三',
                status='pending'
            )
            db.session.add(fault1)
            db.session.commit()

            fault2 = Fault(
                work_order_no=Fault.generate_work_order_no(),
                device_id=device3.id,
                fault_type='传感器故障',
                fault_category='sensor',
                priority='medium',
                fault_desc='流量传感器读数异常，波动过大',
                reporter='李四',
                status='processing',
                handler='王工',
                handle_time=datetime.now()
            )
            db.session.add(fault2)
            db.session.commit()

            fault3 = Fault(
                work_order_no=Fault.generate_work_order_no(),
                device_id=device4.id,
                fault_type='通信模块故障',
                fault_category='communication',
                priority='high',
                fault_desc='商业楼水表通信中断，影响大面积商户用水计量，属民生紧急问题',
                reporter='赵经理',
                status='pending'
            )
            db.session.add(fault3)
            db.session.commit()

            fault4 = Fault(
                work_order_no=Fault.generate_work_order_no(),
                device_id=device2.id,
                fault_type='电池电量低',
                fault_category='power',
                priority='low',
                fault_desc='水表电池电量低于20%，需择机更换',
                reporter='系统',
                status='pending'
            )
            db.session.add(fault4)
            db.session.commit()

            fault5 = Fault(
                work_order_no=Fault.generate_work_order_no(),
                device_id=device5.id,
                fault_type='软件异常',
                fault_category='software',
                priority='medium',
                fault_desc='水表固件运行异常，偶尔出现数据丢失',
                reporter='系统监测',
                status='completed',
                handler='李工',
                handle_time=datetime.now() - timedelta(days=1),
                handle_note='已更新固件，设备恢复正常'
            )
            db.session.add(fault5)
            db.session.commit()
            print("添加了5个故障工单")

        if MaintenanceRecord.query.count() == 0:
            device1 = Device.query.filter_by(device_code='WM001').first()
            maintenance1 = MaintenanceRecord(
                device_id=device1.id,
                maintenance_type='例行巡检',
                operator='王工',
                maintenance_content='检查设备运行状态，清洁传感器',
                parts_replaced='无',
                cost=0.0,
                notes='设备运行正常'
            )
            db.session.add(maintenance1)
            db.session.commit()

            device6 = Device.query.filter_by(device_code='WM006').first()
            maintenance2 = MaintenanceRecord(
                device_id=device6.id,
                fault_id=5,
                maintenance_type='故障维修',
                operator='李工',
                maintenance_content='固件升级，重启设备',
                parts_replaced='无',
                cost=150.0,
                notes='设备已恢复正常'
            )
            db.session.add(maintenance2)
            db.session.commit()
            print("添加了2条运维记录")

        print("演示数据初始化完成！")
        print(f"当前设备数量: {Device.query.count()}")
        print(f"当前故障工单数量: {Fault.query.count()}")
        print(f"当前运维记录数量: {MaintenanceRecord.query.count()}")

if __name__ == '__main__':
    init_demo_data()