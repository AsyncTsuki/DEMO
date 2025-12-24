# MySQL数据库设计文档

## 1. 数据库概述

本数据库设计（名称：`fishery`）用于海洋渔业智能投喂系统，支持以下主要功能：
- 用户认证和管理
- 环境监测和告警
- 设备管理和控制
- 投喂计划和历史
- 告警通知
- 系统日志审计
- 鱼塘管理

**基本信息**：
- 字符集：utf8mb4
- 排序规则：utf8mb4_unicode_ci
- 存储引擎：InnoDB

---

## 2. 用户表 (users)

用于存储系统用户信息。

| 字段名 | 数据类型 | 约束 | 默认值 | 描述 |
|--------|----------|------|--------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | - | 用户ID |
| username | VARCHAR(50) | UNIQUE, NOT NULL, INDEX | - | 用户名 (4-50字符) |
| password_hash | VARCHAR(255) | NOT NULL | - | 密码哈希值 (Werkzeug生成) |
| email | VARCHAR(100) | UNIQUE, NOT NULL, INDEX | - | 邮箱地址 |
| created_at | DATETIME | NOT NULL, INDEX | CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL | CURRENT_TIMESTAMP | 更新时间 |

**索引**：
- username (UNIQUE)
- email (UNIQUE)
- created_at

---

## 3. 鱼塘表 (ponds)

用于管理各个养殖鱼塘的基本信息。

| 字段名 | 数据类型 | 约束 | 默认值 | 描述 |
|--------|----------|------|--------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | - | 鱼塘ID |
| name | VARCHAR(100) | NOT NULL | - | 鱼塘名称 |
| location | VARCHAR(200) | NOT NULL | - | 鱼塘位置 |
| area | FLOAT | NOT NULL | - | 鱼塘面积 (平方米) |
| depth | FLOAT | NOT NULL | - | 鱼塘深度 (米) |
| capacity | INT | NOT NULL | - | 容纳容量 (尾数) |
| fish_type | VARCHAR(50) | - | NULL | 养殖鱼种 |
| fish_count | INT | - | 0 | 当前鱼数量 |
| status | VARCHAR(20) | NOT NULL, INDEX | 'active' | 鱼塘状态 (active, inactive, maintenance) |
| created_at | DATETIME | NOT NULL, INDEX | CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL | CURRENT_TIMESTAMP | 更新时间 |
| notes | TEXT | - | NULL | 备注信息 |

**索引**：
- status
- created_at

---

## 4. 环境数据表 (environment_data)

用于存储实时环境监测数据，由设备端定期上报。

| 字段名 | 数据类型 | 约束 | 默认值 | 描述 |
|--------|----------|------|--------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | - | 记录ID |
| timestamp | DATETIME | NOT NULL, INDEX | CURRENT_TIMESTAMP | 数据采集时间 |
| temperature | FLOAT | NOT NULL | - | 水温 (°C) |
| dissolved_oxygen | FLOAT | NOT NULL | - | 溶解氧 (mg/L) |
| ph | FLOAT | NOT NULL | - | pH值 |
| water_flow | FLOAT | NOT NULL | - | 水流量 (m³/s) |
| created_at | DATETIME | NOT NULL | CURRENT_TIMESTAMP | 数据入库时间 |

**索引**：
- timestamp (用于历史查询)

**说明**：
- 该表为时间序列数据，会快速增长
- 可考虑定期分区或备份历史数据

---

## 5. 环境告警阈值表 (environment_thresholds)

用于存储环境参数的告警阈值配置。

| 字段名 | 数据类型 | 约束 | 默认值 | 描述 |
|--------|----------|------|--------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | - | 配置ID |
| temperature_min | FLOAT | NOT NULL | 18.0 | 温度最小值 (°C) |
| temperature_max | FLOAT | NOT NULL | 28.0 | 温度最大值 (°C) |
| dissolved_oxygen_min | FLOAT | NOT NULL | 5.0 | 溶解氧最小值 (mg/L) |
| dissolved_oxygen_max | FLOAT | NOT NULL | 8.0 | 溶解氧最大值 (mg/L) |
| ph_min | FLOAT | NOT NULL | 7.0 | pH最小值 |
| ph_max | FLOAT | NOT NULL | 8.0 | pH最大值 |
| updated_at | DATETIME | NOT NULL | CURRENT_TIMESTAMP | 更新时间 |

**说明**：
- 通常只有一条记录（全局配置）
- 根据阈值与 environment_data 对比生成告警

---

## 6. 设备表 (devices)

用于管理系统中的各类物联网设备。

| 字段名 | 数据类型 | 约束 | 默认值 | 描述 |
|--------|----------|------|--------|------|
| id | VARCHAR(50) | PRIMARY KEY | - | 设备ID (唯一标识) |
| name | VARCHAR(100) | NOT NULL | - | 设备名称 |
| type | VARCHAR(50) | NOT NULL, INDEX | - | 设备类型 (feeder, sensor等) |
| status | VARCHAR(20) | NOT NULL, INDEX | 'offline' | 设备状态 (online, offline) |
| active | BOOLEAN | NOT NULL | TRUE | 是否激活 |
| location | VARCHAR(100) | NOT NULL, INDEX | - | 设备位置 |
| created_at | DATETIME | NOT NULL | CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL | CURRENT_TIMESTAMP | 更新时间 |

**索引**：
- type
- status
- location

**关联**：
- 一对多关系：device_configs
- 一对多关系：feeding_plans
- 一对多关系：feeding_history

---

## 7. 设备配置表 (device_configs)

用于存储各设备的配置参数。

| 字段名 | 数据类型 | 约束 | 默认值 | 描述 |
|--------|----------|------|--------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | - | 配置ID |
| device_id | VARCHAR(50) | NOT NULL, FOREIGN KEY | - | 关联设备ID |
| config | JSON | NOT NULL | {} | 设备配置 (JSON格式) |
| created_at | DATETIME | NOT NULL | CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL | CURRENT_TIMESTAMP | 更新时间 |

**外键约束**：
- device_id -> devices.id (ON DELETE CASCADE)

---

## 8. 设备联动配置表 (device_linkage_config)

用于管理设备间的联动规则和自动化控制。

| 字段名 | 数据类型 | 约束 | 默认值 | 描述 |
|--------|----------|------|--------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | - | 配置ID |
| trigger_type | VARCHAR(50) | NOT NULL | 'time' | 触发类型 (time, manual, environment) |
| interval | INT | NOT NULL | 60 | 执行间隔 (分钟) |
| related_devices | JSON | NOT NULL | [] | 关联设备ID数组 (JSON) |
| auto_adjust | BOOLEAN | NOT NULL | FALSE | 是否启用自动调整 |
| temp_threshold | FLOAT | NOT NULL | 25.0 | 温度阈值触发点 (°C) |
| oxygen_threshold | FLOAT | NOT NULL | 6.0 | 溶解氧阈值触发点 (mg/L) |
| ph_threshold | FLOAT | NOT NULL | 7.5 | pH值阈值触发点 |
| updated_at | DATETIME | NOT NULL | CURRENT_TIMESTAMP | 更新时间 |

**说明**：
- 通常只有一条或少量记录
- 支持多种触发方式和自动化规则

---

## 9. 投喂计划表 (feeding_plans)

用于存储定时投喂计划。

| 字段名 | 数据类型 | 约束 | 默认值 | 描述 |
|--------|----------|------|--------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | - | 计划ID |
| name | VARCHAR(100) | NOT NULL | - | 计划名称 |
| device_id | VARCHAR(50) | NOT NULL, FOREIGN KEY, INDEX | - | 投喂设备ID |
| time | TIME | NOT NULL | - | 每日执行时间 |
| amount | FLOAT | NOT NULL | - | 投喂量 (kg) |
| status | VARCHAR(20) | NOT NULL, INDEX | 'active' | 计划状态 (active, inactive) |
| created_at | DATETIME | NOT NULL | CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL | CURRENT_TIMESTAMP | 更新时间 |

**索引**：
- device_id
- status

**外键约束**：
- device_id -> devices.id (ON DELETE CASCADE)

**说明**：
- 基于 TIME 类型，系统会每日自动执行

---

## 10. 投喂历史表 (feeding_history)

用于记录所有投喂操作的历史，包括鱼群信息用于智能算法分析。

| 字段名 | 数据类型 | 约束 | 默认值 | 描述 |
|--------|----------|------|--------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | - | 记录ID |
| device_id | VARCHAR(50) | NOT NULL, FOREIGN KEY | - | 投喂设备ID |
| amount | FLOAT | NOT NULL | - | 投喂量 (kg) |
| time | DATETIME | NOT NULL | CURRENT_TIMESTAMP | 投喂执行时间 |
| timestamp | DATETIME | NOT NULL, INDEX | CURRENT_TIMESTAMP | 时间戳 (用于统计分析) |
| type | VARCHAR(20) | NOT NULL | - | 投喂类型 (auto, manual) |
| operator | VARCHAR(50) | NOT NULL | - | 操作人 (用户名或系统) |
| fish_type | VARCHAR(50) | - | NULL | 鱼种信息 |
| fish_count | INT | - | NULL | 鱼群数量 |
| average_weight | FLOAT | - | NULL | 平均体重 (克) |
| created_at | DATETIME | NOT NULL | CURRENT_TIMESTAMP | 创建时间 |

**索引**：
- timestamp (用于快速查询和统计)

**外键约束**：
- device_id -> devices.id (ON DELETE CASCADE)

**说明**：
- 该表为业务关键表，也会快速增长
- 包含智能投喂所需的鱼群信息参数

---

## 11. 告警表 (alerts)

用于存储系统生成的告警信息。

| 字段名 | 数据类型 | 约束 | 默认值 | 描述 |
|--------|----------|------|--------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | - | 告警ID |
| title | VARCHAR(100) | NOT NULL | - | 告警标题 |
| level | VARCHAR(20) | NOT NULL, INDEX | - | 告警级别 (warning, error) |
| time | DATETIME | NOT NULL, INDEX | CURRENT_TIMESTAMP | 告警发生时间 |
| location | VARCHAR(100) | NOT NULL | - | 告警位置/设备 |
| description | TEXT | NOT NULL | - | 告警详细描述 |
| resolved | BOOLEAN | NOT NULL, INDEX | FALSE | 是否已处理 |
| resolved_at | DATETIME | - | NULL | 处理时间 |
| resolved_by | VARCHAR(50) | - | NULL | 处理人 |
| created_at | DATETIME | NOT NULL | CURRENT_TIMESTAMP | 创建时间 |

**索引**：
- level
- time
- resolved

**说明**：
- 告警由系统自动生成，可由用户手动确认
- 支持告警分级和处理追溯

---

## 12. 告警通知设置表 (alert_notification_settings)

用于存储用户的告警通知偏好设置。

| 字段名 | 数据类型 | 约束 | 默认值 | 描述 |
|--------|----------|------|--------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | - | 设置ID |
| user_id | INT | NOT NULL, FOREIGN KEY | - | 用户ID |
| email | BOOLEAN | NOT NULL | TRUE | 是否邮件通知 |
| sms | BOOLEAN | NOT NULL | FALSE | 是否短信通知 |
| push | BOOLEAN | NOT NULL | TRUE | 是否推送通知 |
| updated_at | DATETIME | NOT NULL | CURRENT_TIMESTAMP | 更新时间 |

**外键约束**：
- user_id -> users.id (ON DELETE CASCADE)

**说明**：
- 每个用户对应一条记录
- 支持多种通知渠道

---

## 13. 系统日志表 (logs)

用于记录系统中的所有操作日志，用于审计和故障排查。

| 字段名 | 数据类型 | 约束 | 默认值 | 描述 |
|--------|----------|------|--------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | - | 日志ID |
| timestamp | DATETIME | NOT NULL, INDEX | CURRENT_TIMESTAMP | 日志时间 |
| level | VARCHAR(20) | NOT NULL, INDEX | - | 日志级别 (INFO, WARNING, ERROR) |
| module | VARCHAR(50) | NOT NULL, INDEX | - | 模块名称 |
| operator | VARCHAR(50) | NOT NULL | - | 操作人 (用户名或系统) |
| action | VARCHAR(100) | NOT NULL | - | 操作内容 |
| details | TEXT | NOT NULL | - | 详细信息 |
| ip | VARCHAR(50) | NOT NULL | - | 操作者IP地址 |
| created_at | DATETIME | NOT NULL | CURRENT_TIMESTAMP | 创建时间 |

**索引**：
- timestamp (用于时间范围查询)
- level
- module

**说明**：
- 为审计和问题追溯关键表
- 建议定期备份和归档历史日志

---

## 14. 索引策略

### 性能优化索引

1. **用户表 (users)**：
   - 主键索引：id
   - 唯一索引：username, email
   - 查询优化：支持用户登录和查询

2. **环境数据表 (environment_data)**：
   - 主键索引：id
   - 时间索引：timestamp (用于时间范围查询)
   - 用途：快速查询历史环境数据

3. **设备表 (devices)**：
   - 主键索引：id
   - 功能索引：type, status, location
   - 用途：快速过滤和查询设备

4. **投喂计划表 (feeding_plans)**：
   - 主键索引：id
   - 外键索引：device_id
   - 功能索引：status
   - 用途：支持设备和状态查询

5. **投喂历史表 (feeding_history)**：
   - 主键索引：id
   - 时间索引：timestamp (用于统计)
   - 外键索引：device_id
   - 用途：快速统计和时间序列查询

6. **告警表 (alerts)**：
   - 主键索引：id
   - 功能索引：level, resolved
   - 时间索引：time
   - 用途：告警级别、状态和时间范围查询

7. **日志表 (logs)**：
   - 主键索引：id
   - 时间索引：timestamp
   - 功能索引：level, module
   - 用途：日志查询、故障排查、审计追溯

---

## 15. 数据库维护建议

### 备份策略
- 每日进行完整备份
- 保留7天的增量备份
- 关键表 (users, alerts, logs) 保留至少30天

### 优化建议
- 定期分析表统计信息
- 对大表 (environment_data, feeding_history, logs) 进行分区或归档
- 每月进行一次OPTIMIZE TABLE操作

### 容量规划
- environment_data：约 2880 条/天 (每30秒一条)
- feeding_history：约 10-50 条/天
- alerts：约 5-20 条/天
- logs：约 100-500 条/天

---

## 16. SQL建表语句参考

```sql
-- 创建数据库
CREATE DATABASE IF NOT EXISTS fishery 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE fishery;

-- 用户表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 鱼塘表
CREATE TABLE ponds (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(200) NOT NULL,
    area FLOAT NOT NULL,
    depth FLOAT NOT NULL,
    capacity INT NOT NULL,
    fish_type VARCHAR(50),
    fish_count INT DEFAULT 0,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    notes TEXT,
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 环境数据表
CREATE TABLE environment_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    temperature FLOAT NOT NULL,
    dissolved_oxygen FLOAT NOT NULL,
    ph FLOAT NOT NULL,
    water_flow FLOAT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 环境告警阈值表
CREATE TABLE environment_thresholds (
    id INT PRIMARY KEY AUTO_INCREMENT,
    temperature_min FLOAT NOT NULL DEFAULT 18.0,
    temperature_max FLOAT NOT NULL DEFAULT 28.0,
    dissolved_oxygen_min FLOAT NOT NULL DEFAULT 5.0,
    dissolved_oxygen_max FLOAT NOT NULL DEFAULT 8.0,
    ph_min FLOAT NOT NULL DEFAULT 7.0,
    ph_max FLOAT NOT NULL DEFAULT 8.0,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 设备表
CREATE TABLE devices (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'offline',
    active BOOLEAN NOT NULL DEFAULT TRUE,
    location VARCHAR(100) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_type (type),
    INDEX idx_status (status),
    INDEX idx_location (location)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 设备配置表
CREATE TABLE device_configs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    device_id VARCHAR(50) NOT NULL,
    config JSON NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE,
    INDEX idx_device_id (device_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 设备联动配置表
CREATE TABLE device_linkage_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    trigger_type VARCHAR(50) NOT NULL DEFAULT 'time',
    interval INT NOT NULL DEFAULT 60,
    related_devices JSON NOT NULL DEFAULT '[]',
    auto_adjust BOOLEAN NOT NULL DEFAULT FALSE,
    temp_threshold FLOAT NOT NULL DEFAULT 25.0,
    oxygen_threshold FLOAT NOT NULL DEFAULT 6.0,
    ph_threshold FLOAT NOT NULL DEFAULT 7.5,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 投喂计划表
CREATE TABLE feeding_plans (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    device_id VARCHAR(50) NOT NULL,
    time TIME NOT NULL,
    amount FLOAT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE,
    INDEX idx_device_id (device_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 投喂历史表
CREATE TABLE feeding_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    device_id VARCHAR(50) NOT NULL,
    amount FLOAT NOT NULL,
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    type VARCHAR(20) NOT NULL,
    operator VARCHAR(50) NOT NULL,
    fish_type VARCHAR(50),
    fish_count INT,
    average_weight FLOAT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE,
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 告警表
CREATE TABLE alerts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    level VARCHAR(20) NOT NULL,
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    location VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    resolved BOOLEAN NOT NULL DEFAULT FALSE,
    resolved_at DATETIME,
    resolved_by VARCHAR(50),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_level (level),
    INDEX idx_time (time),
    INDEX idx_resolved (resolved)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 告警通知设置表
CREATE TABLE alert_notification_settings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    email BOOLEAN NOT NULL DEFAULT TRUE,
    sms BOOLEAN NOT NULL DEFAULT FALSE,
    push BOOLEAN NOT NULL DEFAULT TRUE,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 日志表
CREATE TABLE logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    level VARCHAR(20) NOT NULL,
    module VARCHAR(50) NOT NULL,
    operator VARCHAR(50) NOT NULL,
    action VARCHAR(100) NOT NULL,
    details TEXT NOT NULL,
    ip VARCHAR(50) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_timestamp (timestamp),
    INDEX idx_level (level),
    INDEX idx_module (module)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入默认环境阈值
INSERT INTO environment_thresholds (temperature_min, temperature_max, dissolved_oxygen_min, dissolved_oxygen_max, ph_min, ph_max) 
VALUES (18.0, 28.0, 5.0, 8.0, 7.0, 8.0) 
ON DUPLICATE KEY UPDATE id = id;
```

---

## 17. ER 图关系

```
users (1) -------- (N) alert_notification_settings
                            |
devices (1) -------- (N) device_configs
    |                  |
    |                  device_linkage_config
    |
    +------- (N) feeding_plans
    |
    +------- (N) feeding_history

ponds (1) -------- (N) [fish_count]

environment_data
environment_thresholds

alerts

logs
```

---

## 18. 注意事项

1. **字符集**：所有文本字段使用 UTF8MB4，支持emoji和多语言
2. **时间戳**：使用 DATETIME 格式，精确到秒
3. **JSON 字段**：MySQL 5.7.8+ 原生支持，用于灵活的数据结构
4. **外键约束**：使用 ON DELETE CASCADE，删除父记录时自动删除子记录
5. **分布式考虑**：所有表均具备独立ID和时间戳，便于数据同步
6. **隐私保护**：不存储明文密码，使用密码哈希算法（Werkzeug）
7. **投喂历史**：包含鱼群参数（fish_type, fish_count, average_weight），用于支持智能投喂算法
8. **告警通知**：每个用户可以独立配置多种通知渠道（邮件、短信、推送）
