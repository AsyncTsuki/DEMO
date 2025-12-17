# MySQL数据库设计文档

## 1. 数据库概述

本数据库设计（名称：fishery）用于海洋渔业智能投喂系统，支持用户认证、环境监测、设备管理、投喂管理、告警管理和日志管理等功能。

## 2. 用户表 (users)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 用户ID |
| username | VARCHAR(50) | UNIQUE, NOT NULL | 用户名 |
| password_hash | VARCHAR(255) | NOT NULL | 哈希后的密码 |
| email | VARCHAR(100) | UNIQUE, NOT NULL | 邮箱 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

## 3. 环境数据表 (environment_data)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 记录ID |
| timestamp | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 记录时间 |
| temperature | FLOAT | NOT NULL | 温度(°C) |
| dissolved_oxygen | FLOAT | NOT NULL | 溶解氧(mg/L) |
| ph | FLOAT | NOT NULL | pH值 |
| water_flow | FLOAT | NOT NULL | 水流量(m³/s) |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

## 4. 环境告警阈值表 (environment_thresholds)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | ID |
| temperature_min | FLOAT | NOT NULL | 温度最小值 |
| temperature_max | FLOAT | NOT NULL | 温度最大值 |
| dissolved_oxygen_min | FLOAT | NOT NULL | 溶解氧最小值 |
| dissolved_oxygen_max | FLOAT | NOT NULL | 溶解氧最大值 |
| ph_min | FLOAT | NOT NULL | pH最小值 |
| ph_max | FLOAT | NOT NULL | pH最大值 |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

## 5. 设备表 (devices)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | VARCHAR(50) | PRIMARY KEY | 设备ID |
| name | VARCHAR(100) | NOT NULL | 设备名称 |
| type | VARCHAR(50) | NOT NULL | 设备类型 (feeder, sensor, etc.) |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'offline' | 设备状态 (online, offline) |
| active | BOOLEAN | NOT NULL, DEFAULT TRUE | 是否激活 |
| location | VARCHAR(100) | NOT NULL | 设备位置 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

## 6. 设备配置表 (device_configs)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 配置ID |
| device_id | VARCHAR(50) | NOT NULL, FOREIGN KEY (device_id) REFERENCES devices(id) | 设备ID |
| config | JSON | NOT NULL | 设备配置 (JSON格式) |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

## 7. 设备联动配置表 (device_linkage_config)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 配置ID |
| trigger_type | VARCHAR(50) | NOT NULL | 触发类型 (time, manual, environment) |
| interval | INT | NOT NULL | 执行间隔 (分钟) |
| related_devices | JSON | NOT NULL | 关联设备 (JSON数组) |
| auto_adjust | BOOLEAN | NOT NULL | 是否自动调整 |
| temp_threshold | FLOAT | NOT NULL | 温度阈值 |
| oxygen_threshold | FLOAT | NOT NULL | 溶解氧阈值 |
| ph_threshold | FLOAT | NOT NULL | pH阈值 |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

## 8. 投喂计划表 (feeding_plans)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 计划ID |
| name | VARCHAR(100) | NOT NULL | 计划名称 |
| device_id | VARCHAR(50) | NOT NULL, FOREIGN KEY (device_id) REFERENCES devices(id) | 设备ID |
| time | TIME | NOT NULL | 执行时间 |
| amount | FLOAT | NOT NULL | 投喂量 (kg) |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'active' | 状态 (active, inactive) |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

## 9. 投喂历史表 (feeding_history)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 记录ID |
| device_id | VARCHAR(50) | NOT NULL, FOREIGN KEY (device_id) REFERENCES devices(id) | 设备ID |
| amount | FLOAT | NOT NULL | 投喂量 (kg) |
| time | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 执行时间 |
| type | VARCHAR(20) | NOT NULL | 类型 (auto, manual) |
| operator | VARCHAR(50) | NOT NULL | 操作人 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

## 10. 告警表 (alerts)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 告警ID |
| title | VARCHAR(100) | NOT NULL | 告警标题 |
| level | VARCHAR(20) | NOT NULL | 告警级别 (warning, error) |
| time | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 告警时间 |
| location | VARCHAR(100) | NOT NULL | 告警位置 |
| description | TEXT | NOT NULL | 告警描述 |
| resolved | BOOLEAN | NOT NULL, DEFAULT FALSE | 是否已处理 |
| resolved_at | DATETIME | NULL | 处理时间 |
| resolved_by | VARCHAR(50) | NULL | 处理人 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

## 11. 系统日志表 (logs)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 日志ID |
| timestamp | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 日志时间 |
| level | VARCHAR(20) | NOT NULL | 日志级别 (INFO, WARNING, ERROR) |
| module | VARCHAR(50) | NOT NULL | 模块名称 |
| operator | VARCHAR(50) | NOT NULL | 操作人 |
| action | VARCHAR(100) | NOT NULL | 操作内容 |
| details | TEXT | NOT NULL | 详细信息 |
| ip | VARCHAR(50) | NOT NULL | IP地址 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

## 12. 索引设计

1. **用户表**：
   - username 列添加唯一索引
   - email 列添加唯一索引

2. **环境数据表**：
   - timestamp 列添加索引，用于快速查询历史数据

3. **设备表**：
   - type 列添加索引
   - status 列添加索引
   - location 列添加索引

4. **投喂计划表**：
   - device_id 列添加索引
   - status 列添加索引

5. **告警表**：
   - level 列添加索引
   - resolved 列添加索引
   - time 列添加索引

6. **系统日志表**：
   - timestamp 列添加索引
   - level 列添加索引
   - module 列添加索引

## 13. 数据库初始化SQL

```sql
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
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 创建环境数据表
CREATE TABLE IF NOT EXISTS environment_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    temperature FLOAT NOT NULL,
    dissolved_oxygen FLOAT NOT NULL,
    ph FLOAT NOT NULL,
    water_flow FLOAT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 创建环境告警阈值表
CREATE TABLE IF NOT EXISTS environment_thresholds (
    id INT PRIMARY KEY AUTO_INCREMENT,
    temperature_min FLOAT NOT NULL,
    temperature_max FLOAT NOT NULL,
    dissolved_oxygen_min FLOAT NOT NULL,
    dissolved_oxygen_max FLOAT NOT NULL,
    ph_min FLOAT NOT NULL,
    ph_max FLOAT NOT NULL,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 创建设备表
CREATE TABLE IF NOT EXISTS devices (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'offline',
    active BOOLEAN NOT NULL DEFAULT TRUE,
    location VARCHAR(100) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 创建设备配置表
CREATE TABLE IF NOT EXISTS device_configs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    device_id VARCHAR(50) NOT NULL,
    config JSON NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
);

-- 创建设备联动配置表
CREATE TABLE IF NOT EXISTS device_linkage_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    trigger_type VARCHAR(50) NOT NULL,
    interval INT NOT NULL,
    related_devices JSON NOT NULL,
    auto_adjust BOOLEAN NOT NULL,
    temp_threshold FLOAT NOT NULL,
    oxygen_threshold FLOAT NOT NULL,
    ph_threshold FLOAT NOT NULL,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

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
    FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
);

-- 创建投喂历史表
CREATE TABLE IF NOT EXISTS feeding_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    device_id VARCHAR(50) NOT NULL,
    amount FLOAT NOT NULL,
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    type VARCHAR(20) NOT NULL,
    operator VARCHAR(50) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
);

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
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

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
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_environment_data_timestamp ON environment_data(timestamp);
CREATE INDEX idx_devices_type ON devices(type);
CREATE INDEX idx_devices_status ON devices(status);
CREATE INDEX idx_devices_location ON devices(location);
CREATE INDEX idx_feeding_plans_device_id ON feeding_plans(device_id);
CREATE INDEX idx_feeding_plans_status ON feeding_plans(status);
CREATE INDEX idx_alerts_level ON alerts(level);
CREATE INDEX idx_alerts_resolved ON alerts(resolved);
CREATE INDEX idx_alerts_time ON alerts(time);
CREATE INDEX idx_logs_timestamp ON logs(timestamp);
CREATE INDEX idx_logs_level ON logs(level);
CREATE INDEX idx_logs_module ON logs(module);

-- 插入默认环境阈值
INSERT INTO environment_thresholds (temperature_min, temperature_max, dissolved_oxygen_min, dissolved_oxygen_max, ph_min, ph_max) 
VALUES (18.0, 28.0, 5.0, 8.0, 7.0, 8.0) ON DUPLICATE KEY UPDATE id = id;
```

## 14. 数据迁移建议

使用Flask-Migrate进行数据库迁移管理，方便版本控制和部署。

## 15. 安全建议

1. 使用参数化查询防止SQL注入
2. 密码使用强哈希算法（如bcrypt）
3. 定期备份数据库
4. 限制数据库用户权限
5. 启用SSL加密传输