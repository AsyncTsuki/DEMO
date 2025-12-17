# API接口文档

## 1. 认证接口

### 1.1 用户登录
- **URL**: `/api/auth/login`
- **方法**: POST
- **参数**:
  ```json
  {
    "username": "string",  // 用户名
    "password": "string"   // 密码
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "token": "string",    // JWT令牌
    "username": "string", // 用户名
    "user_id": "integer"  // 用户ID
  }
  ```

### 1.2 用户注册
- **URL**: `/api/auth/register`
- **方法**: POST
- **参数**:
  ```json
  {
    "username": "string",  // 用户名
    "password": "string",  // 密码
    "email": "string"      // 邮箱
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "message": "注册成功"
  }
  ```

### 1.3 获取当前用户信息
- **URL**: `/api/auth/user`
- **方法**: GET
- **认证**: 需要JWT令牌
- **响应**:
  ```json
  {
    "success": true,
    "user": {
      "id": "integer",
      "username": "string",
      "email": "string",
      "created_at": "datetime"
    }
  }
  ```

### 1.4 用户退出登录
- **URL**: `/api/auth/logout`
- **方法**: POST
- **认证**: 需要JWT令牌
- **响应**:
  ```json
  {
    "success": true,
    "message": "退出成功"
  }
  ```

## 2. 环境监测接口

### 2.1 获取实时环境数据
- **URL**: `/api/environment/realtime`
- **方法**: GET
- **认证**: 需要JWT令牌
- **响应**:
  ```json
  {
    "success": true,
    "data": {
      "temperature": "float",      // 温度(°C)
      "dissolvedOxygen": "float",  // 溶解氧(mg/L)
      "ph": "float",               // pH值
      "waterFlow": "float"         // 水流量(m³/s)
    }
  }
  ```

### 2.2 获取环境数据历史记录
- **URL**: `/api/environment/history`
- **方法**: GET
- **认证**: 需要JWT令牌
- **参数**:
  ```json
  {
    "start_time": "string",  // 开始时间 (ISO格式)
    "end_time": "string",    // 结束时间 (ISO格式)
    "limit": "integer",      // 记录数量
    "offset": "integer"      // 偏移量
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "data": [
      {
        "id": "integer",
        "timestamp": "datetime",
        "temperature": "float",
        "dissolvedOxygen": "float",
        "ph": "float",
        "waterFlow": "float"
      }
    ],
    "total": "integer"  // 总记录数
  }
  ```

### 2.3 获取环境数据统计
- **URL**: `/api/environment/statistics`
- **方法**: GET
- **认证**: 需要JWT令牌
- **参数**:
  ```json
  {
    "start_time": "string",  // 开始时间 (ISO格式)
    "end_time": "string",    // 结束时间 (ISO格式)
    "interval": "string"      // 统计间隔 (hour, day, week, month)
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "data": {
      "temperature": {
        "avg": "float",
        "min": "float",
        "max": "float"
      },
      "dissolvedOxygen": {
        "avg": "float",
        "min": "float",
        "max": "float"
      },
      "ph": {
        "avg": "float",
        "min": "float",
        "max": "float"
      }
    }
  }
  ```

### 2.4 获取环境告警阈值配置
- **URL**: `/api/environment/thresholds`
- **方法**: GET
- **认证**: 需要JWT令牌
- **响应**:
  ```json
  {
    "success": true,
    "data": {
      "temperature": {
        "min": "float",
        "max": "float"
      },
      "dissolvedOxygen": {
        "min": "float",
        "max": "float"
      },
      "ph": {
        "min": "float",
        "max": "float"
      }
    }
  }
  ```

### 2.5 更新环境告警阈值配置
- **URL**: `/api/environment/thresholds`
- **方法**: PUT
- **认证**: 需要JWT令牌
- **参数**:
  ```json
  {
    "temperature": {
      "min": "float",
      "max": "float"
    },
    "dissolvedOxygen": {
      "min": "float",
      "max": "float"
    },
    "ph": {
      "min": "float",
      "max": "float"
    }
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "message": "阈值配置更新成功"
  }
  ```

## 3. 设备管理接口

### 3.1 获取设备列表
- **URL**: `/api/devices`
- **方法**: GET
- **认证**: 需要JWT令牌
- **参数**:
  ```json
  {
    "type": "string",  // 设备类型 (feeder, sensor, etc.)
    "status": "string" // 设备状态 (online, offline)
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "data": [
      {
        "id": "string",
        "name": "string",
        "type": "string",
        "status": "string",
        "active": "boolean",
        "location": "string",
        "created_at": "datetime"
      }
    ]
  }
  ```

### 3.2 获取单个设备信息
- **URL**: `/api/devices/{deviceId}`
- **方法**: GET
- **认证**: 需要JWT令牌
- **响应**:
  ```json
  {
    "success": true,
    "data": {
      "id": "string",
      "name": "string",
      "type": "string",
      "status": "string",
      "active": "boolean",
      "location": "string",
      "created_at": "datetime",
      "last_updated": "datetime"
    }
  }
  ```

### 3.3 更新设备状态
- **URL**: `/api/devices/{deviceId}/status`
- **方法**: PATCH
- **认证**: 需要JWT令牌
- **参数**:
  ```json
  {
    "status": "string"  // 新状态 (online, offline)
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "message": "设备状态更新成功"
  }
  ```

### 3.4 保存设备配置
- **URL**: `/api/devices/{deviceId}/config`
- **方法**: PUT
- **认证**: 需要JWT令牌
- **参数**:
  ```json
  {
    "config": {}
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "message": "设备配置保存成功"
  }
  ```

### 3.5 获取设备配置
- **URL**: `/api/devices/{deviceId}/config`
- **方法**: GET
- **认证**: 需要JWT令牌
- **响应**:
  ```json
  {
    "success": true,
    "data": {
      "config": {}
    }
  }
  ```

### 3.6 获取设备联动配置
- **URL**: `/api/devices/linkage`
- **方法**: GET
- **认证**: 需要JWT令牌
- **响应**:
  ```json
  {
    "success": true,
    "data": {
      "triggerType": "string",
      "interval": "integer",
      "relatedDevices": ["string"],
      "autoAdjust": "boolean",
      "tempThreshold": "float",
      "oxygenThreshold": "float",
      "phThreshold": "float"
    }
  }
  ```

### 3.7 保存设备联动配置
- **URL**: `/api/devices/linkage`
- **方法**: PUT
- **认证**: 需要JWT令牌
- **参数**:
  ```json
  {
    "triggerType": "string",
    "interval": "integer",
    "relatedDevices": ["string"],
    "autoAdjust": "boolean",
    "tempThreshold": "float",
    "oxygenThreshold": "float",
    "phThreshold": "float"
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "message": "设备联动配置保存成功"
  }
  ```

## 4. 投喂管理接口

### 4.1 获取投喂计划列表
- **URL**: `/api/feeding/plans`
- **方法**: GET
- **认证**: 需要JWT令牌
- **参数**:
  ```json
  {
    "device_id": "string",  // 设备ID
    "status": "string"      // 状态 (active, inactive)
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "data": [
      {
        "id": "integer",
        "name": "string",
        "device_id": "string",
        "time": "string",
        "amount": "float",
        "status": "string",
        "created_at": "datetime"
      }
    ]
  }
  ```

### 4.2 创建投喂计划
- **URL**: `/api/feeding/plans`
- **方法**: POST
- **认证**: 需要JWT令牌
- **参数**:
  ```json
  {
    "name": "string",
    "device_id": "string",
    "time": "string",
    "amount": "float",
    "status": "string"
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "message": "投喂计划创建成功"
  }
  ```

### 4.3 更新投喂计划
- **URL**: `/api/feeding/plans/{planId}`
- **方法**: PUT
- **认证**: 需要JWT令牌
- **参数**:
  ```json
  {
    "name": "string",
    "device_id": "string",
    "time": "string",
    "amount": "float",
    "status": "string"
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "message": "投喂计划更新成功"
  }
  ```

### 4.4 删除投喂计划
- **URL**: `/api/feeding/plans/{planId}`
- **方法**: DELETE
- **认证**: 需要JWT令牌
- **响应**:
  ```json
  {
    "success": true,
    "message": "投喂计划删除成功"
  }
  ```

### 4.5 执行手动投喂
- **URL**: `/api/feeding/execute`
- **方法**: POST
- **认证**: 需要JWT令牌
- **参数**:
  ```json
  {
    "deviceId": "string",
    "amount": "float"
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "message": "投喂指令已发送"
  }
  ```

### 4.6 计算建议投喂量
- **URL**: `/api/feeding/calculate`
- **方法**: GET
- **认证**: 需要JWT令牌
- **参数**:
  ```json
  {
    "fishCount": "integer",
    "averageWeight": "float",
    "fishType": "string"
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "data": {
      "amount": "float",
      "type": "string",
      "reason": "string"
    }
  }
  ```

### 4.7 获取投喂历史记录
- **URL**: `/api/feeding/history`
- **方法**: GET
- **认证**: 需要JWT令牌
- **参数**:
  ```json
  {
    "device_id": "string",  // 设备ID
    "start_time": "string", // 开始时间
    "end_time": "string"    // 结束时间
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "data": [
      {
        "id": "integer",
        "device_id": "string",
        "amount": "float",
        "time": "datetime",
        "type": "string",
        "operator": "string"
      }
    ]
  }
  ```

## 5. 告警管理接口

### 5.1 获取告警列表
- **URL**: `/api/alerts`
- **方法**: GET
- **认证**: 需要JWT令牌
- **参数**:
  ```json
  {
    "level": "string",      // 告警级别 (warning, error)
    "resolved": "boolean",  // 是否已处理
    "start_time": "string", // 开始时间
    "end_time": "string"    // 结束时间
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "data": [
      {
        "id": "integer",
        "title": "string",
        "level": "string",
        "time": "datetime",
        "location": "string",
        "description": "string",
        "resolved": "boolean"
      }
    ]
  }
  ```

### 5.2 获取单个告警详情
- **URL**: `/api/alerts/{alertId}`
- **方法**: GET
- **认证**: 需要JWT令牌
- **响应**:
  ```json
  {
    "success": true,
    "data": {
      "id": "integer",
      "title": "string",
      "level": "string",
      "time": "datetime",
      "location": "string",
      "description": "string",
      "resolved": "boolean",
      "resolved_at": "datetime",
      "resolved_by": "string"
    }
  }
  ```

### 5.3 标记告警为已处理
- **URL**: `/api/alerts/{alertId}/resolve`
- **方法**: PATCH
- **认证**: 需要JWT令牌
- **响应**:
  ```json
  {
    "success": true,
    "message": "告警已标记为已处理"
  }
  ```

### 5.4 获取告警统计数据
- **URL**: `/api/alerts/statistics`
- **方法**: GET
- **认证**: 需要JWT令牌
- **响应**:
  ```json
  {
    "success": true,
    "data": {
      "total": "integer",
      "warning": "integer",
      "error": "integer",
      "resolved": "integer"
    }
  }
  ```

### 5.5 获取未处理的告警数量
- **URL**: `/api/alerts/unresolved/count`
- **方法**: GET
- **认证**: 需要JWT令牌
- **响应**:
  ```json
  {
    "success": true,
    "data": {
      "count": "integer"
    }
  }
  ```

### 5.6 配置告警通知设置
- **URL**: `/api/alerts/notifications`
- **方法**: PUT
- **认证**: 需要JWT令牌
- **参数**:
  ```json
  {
    "email": "boolean",
    "sms": "boolean",
    "push": "boolean"
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "message": "告警通知设置更新成功"
  }
  ```

## 6. 日志管理接口

### 6.1 获取系统日志列表
- **URL**: `/api/logs`
- **方法**: GET
- **认证**: 需要JWT令牌
- **参数**:
  ```json
  {
    "level": "string",      // 日志级别 (INFO, WARNING, ERROR)
    "module": "string",     // 模块名称
    "start_time": "string", // 开始时间
    "end_time": "string"    // 结束时间
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "data": [
      {
        "id": "integer",
        "timestamp": "datetime",
        "level": "string",
        "module": "string",
        "operator": "string",
        "action": "string",
        "details": "string",
        "ip": "string"
      }
    ]
  }
  ```

### 6.2 获取单个日志详情
- **URL**: `/api/logs/{logId}`
- **方法**: GET
- **认证**: 需要JWT令牌
- **响应**:
  ```json
  {
    "success": true,
    "data": {
      "id": "integer",
      "timestamp": "datetime",
      "level": "string",
      "module": "string",
      "operator": "string",
      "action": "string",
      "details": "string",
      "ip": "string"
    }
  }
  ```

### 6.3 搜索日志
- **URL**: `/api/logs/search`
- **方法**: GET
- **认证**: 需要JWT令牌
- **参数**:
  ```json
  {
    "keyword": "string",    // 搜索关键词
    "start_time": "string", // 开始时间
    "end_time": "string"    // 结束时间
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "data": [
      {
        "id": "integer",
        "timestamp": "datetime",
        "level": "string",
        "module": "string",
        "operator": "string",
        "action": "string",
        "details": "string",
        "ip": "string"
      }
    ]
  }
  ```

### 6.4 获取日志统计数据
- **URL**: `/api/logs/statistics`
- **方法**: GET
- **认证**: 需要JWT令牌
- **参数**:
  ```json
  {
    "start_time": "string", // 开始时间
    "end_time": "string"    // 结束时间
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "data": {
      "info": "integer",
      "warning": "integer",
      "error": "integer",
      "total": "integer"
    }
  }
  ```

## 7. 错误响应格式

所有API接口在出错时都会返回统一的错误响应格式：

```json
{
  "success": false,
  "message": "错误信息描述",
  "code": "错误代码（可选）"
}
```

常见错误代码：
- 400: 请求参数错误
- 401: 未授权
- 403: 权限不足
- 404: 资源不存在
- 500: 服务器内部错误