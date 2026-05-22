-- 创建数据库
CREATE DATABASE IF NOT EXISTS hotel_management DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE hotel_management;

-- 初始化客房数据
INSERT INTO room (room_number, room_type, price, status, floor, capacity, description, create_time, update_time) VALUES
('101', 'single', 188.00, 'available', 1, 1, '标准单人间，配备空调、电视、独立卫浴', NOW(), NOW()),
('102', 'single', 188.00, 'available', 1, 1, '标准单人间，配备空调、电视、独立卫浴', NOW(), NOW()),
('103', 'double', 288.00, 'available', 1, 2, '标准双人间，两张单人床，配备空调、电视、独立卫浴', NOW(), NOW()),
('104', 'double', 288.00, 'available', 1, 2, '标准双人间，两张单人床，配备空调、电视、独立卫浴', NOW(), NOW()),
('201', 'double', 328.00, 'available', 2, 2, '豪华双人间，大床，配备空调、电视、独立卫浴、迷你吧', NOW(), NOW()),
('202', 'double', 328.00, 'available', 2, 2, '豪华双人间，大床，配备空调、电视、独立卫浴、迷你吧', NOW(), NOW()),
('203', 'suite', 588.00, 'available', 2, 3, '商务套房，卧室+客厅，配备空调、电视、独立卫浴、办公区', NOW(), NOW()),
('204', 'suite', 588.00, 'available', 2, 3, '商务套房，卧室+客厅，配备空调、电视、独立卫浴、办公区', NOW(), NOW()),
('301', 'deluxe', 888.00, 'available', 3, 4, '豪华套房，主卧+客厅+餐厅，配备空调、电视、独立卫浴、观景阳台', NOW(), NOW()),
('302', 'deluxe', 888.00, 'available', 3, 4, '豪华套房，主卧+客厅+餐厅，配备空调、电视、独立卫浴、观景阳台', NOW(), NOW());
