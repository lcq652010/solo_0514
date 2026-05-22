-- 创建驾校管理系统数据库
CREATE DATABASE IF NOT EXISTS driving_school DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建数据库用户（可选）
-- CREATE USER 'driving_school'@'localhost' IDENTIFIED BY 'driving_school123';
-- GRANT ALL PRIVILEGES ON driving_school.* TO 'driving_school'@'localhost';
-- FLUSH PRIVILEGES;

-- 使用数据库
USE driving_school;

-- 查看表结构（Django迁移后执行）
-- SHOW TABLES;
