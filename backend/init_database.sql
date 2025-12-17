-- 海洋渔业智能投喂系统 - MySQL数据库初始化脚本
-- 运行前请确保已安装MySQL并有足够权限

-- 创建数据库
CREATE DATABASE IF NOT EXISTS fishery DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE fishery;

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_users_username (username),
    INDEX idx_users_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建环境数据表
CREATE TABLE IF NOT EXISTS environment_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    temperature FLOAT NOT NULL,
    dissolved_oxygen FLOAT NOT NULL,
    ph FLOAT NOT NULL,
    water_flow FLOAT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_environment_data_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建环境告警阈值表
CREATE TABLE IF NOT EXISTS environment_thresholds (
    id INT PRIMARY KEY AUTO_INCREMENT,
    temperature_min FLOAT NOT NULL DEFAULT 18.0,
    temperature_max FLOAT NOT NULL DEFAULT 28.0,
    dissolved_oxygen_min FLOAT NOT NULL DEFAULT 5.0,
    dissolved_oxygen_max FLOAT NOT NULL DEFAULT 8.0,
    ph_min FLOAT NOT NULL DEFAULT 7.0,
    ph_max FLOAT NOT NULL DEFAULT 8.0,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建设备表
CREATE TABLE IF NOT EXISTS devices (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'offline',
    active BOOLEAN NOT NULL DEFAULT TRUE,
    location VARCHAR(100) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_devices_type (type),
    INDEX idx_devices_status (status),
    INDEX idx_devices_location (location)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建设备配置表
CREATE TABLE IF NOT EXISTS device_configs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    device_id VARCHAR(50) NOT NULL,
    config JSON NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE,
    INDEX idx_device_configs_device_id (device_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建设备联动配置表
CREATE TABLE IF NOT EXISTS device_linkage_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    trigger_type VARCHAR(50) NOT NULL DEFAULT 'time',
    `interval` INT NOT NULL DEFAULT 60,
    related_devices JSON NOT NULL,
    auto_adjust BOOLEAN NOT NULL DEFAULT FALSE,
    temp_threshold FLOAT NOT NULL DEFAULT 25.0,
    oxygen_threshold FLOAT NOT NULL DEFAULT 6.0,
    ph_threshold FLOAT NOT NULL DEFAULT 7.5,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建投喂计划表
CREATE TABLE IF NOT EXISTS feeding_plans (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    device_id VARCHAR(50) NOT NULL,
    time TIME NOT NULL,
    amount FLOAT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE,
    INDEX idx_feeding_plans_device_id (device_id),
    INDEX idx_feeding_plans_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建投喂历史表
CREATE TABLE IF NOT EXISTS feeding_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    device_id VARCHAR(50) NOT NULL,
    amount FLOAT NOT NULL,
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    type VARCHAR(20) NOT NULL,
    operator VARCHAR(50) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE,
    INDEX idx_feeding_history_device_id (device_id),
    INDEX idx_feeding_history_time (time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建告警表
CREATE TABLE IF NOT EXISTS alerts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    level VARCHAR(20) NOT NULL,
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    location VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    resolved BOOLEAN NOT NULL DEFAULT FALSE,
    resolved_at DATETIME NULL,
    resolved_by VARCHAR(50) NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_alerts_level (level),
    INDEX idx_alerts_resolved (resolved),
    INDEX idx_alerts_time (time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建告警通知设置表
CREATE TABLE IF NOT EXISTS alert_notification_settings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    email BOOLEAN NOT NULL DEFAULT TRUE,
    sms BOOLEAN NOT NULL DEFAULT FALSE,
    push BOOLEAN NOT NULL DEFAULT TRUE,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_alert_notification_settings_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建系统日志表
CREATE TABLE IF NOT EXISTS logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    level VARCHAR(20) NOT NULL,
    module VARCHAR(50) NOT NULL,
    operator VARCHAR(50) NOT NULL,
    action VARCHAR(100) NOT NULL,
    details TEXT NOT NULL,
    ip VARCHAR(50) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_logs_timestamp (timestamp),
    INDEX idx_logs_level (level),
    INDEX idx_logs_module (module)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入默认环境阈值
INSERT INTO environment_thresholds (temperature_min, temperature_max, dissolved_oxygen_min, dissolved_oxygen_max, ph_min, ph_max) 
VALUES (18.0, 28.0, 5.0, 8.0, 7.0, 8.0);

-- 插入示例设备
INSERT INTO devices (id, name, type, status, location) VALUES
('feeder-001', '智能投喂机1号', 'feeder', 'online', 'A区1号网箱'),
('feeder-002', '智能投喂机2号', 'feeder', 'online', 'A区2号网箱'),
('feeder-003', '智能投喂机3号', 'feeder', 'offline', 'B区1号网箱'),
('sensor-001', '水质传感器1号', 'sensor', 'online', 'A区监测点'),
('sensor-002', '水质传感器2号', 'sensor', 'online', 'B区监测点'),
('camera-001', '水下摄像头1号', 'camera', 'online', 'A区1号网箱');

-- 插入设备联动配置
INSERT INTO device_linkage_config (trigger_type, `interval`, related_devices, auto_adjust, temp_threshold, oxygen_threshold, ph_threshold)
VALUES ('environment', 30, '["feeder-001", "feeder-002", "sensor-001"]', TRUE, 25.0, 6.0, 7.5);

COMMIT;
