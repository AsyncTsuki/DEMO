# API接口文档

## 认证说明

本项目采用 **Session + Cookie** 的认证方式。用户登录后，服务器会创建 Session 并通过 Cookie 返回给客户端。后续所有需要认证的请求会自动通过 Cookie 携带 Session 信息。

**CORS 配置**:
- 允许跨域请求，支持以下来源：
  - `http://localhost:5173` (开发环境前端)
  - `http://127.0.0.1:5173`
  - `http://localhost:3000` (其他接口)

---

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
    "message": "登录成功",
    "username": "string", // 用户名
    "user_id": "integer"  // 用户ID
  }
  ```
- **说明**: 登录成功后，会在服务器端设置 Session Cookie，后续请求需要自动携带该 Cookie

### 1.2 用户注册
- **URL**: `/api/auth/register`
- **方法**: POST
- **参数**:
  ```json
  {
    "username": "string",  // 用户名 (4-50字符)
    "password": "string",  // 密码 (6-100字符)
    "email": "string"      // 邮箱 (有效邮箱格式)
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
- **认证**: 需要 Session Cookie
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
- **认证**: 需要 Session Cookie
- **响应**:
  ```json
  {
    "success": true,
    "message": "退出成功"
  }
  ```

---

## 2. 环境监测接口

### 2.1 接收设备上报的环境数据
- **URL**: `/api/environment/data`
- **方法**: POST
- **认证**: 无需认证（设备端可直接调用）
- **参数**:
  ```json
  {
    "temperature": "float",      // 温度(°C)
    "dissolved_oxygen": "float", // 溶解氧(mg/L)
    "ph": "float",               // pH值
    "water_flow": "float"        // 水流量(m³/s)
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "message": "数据上报成功"
  }
  ```

### 2.2 获取实时环境数据
- **URL**: `/api/environment/realtime`
- **方法**: GET
- **认证**: 需要 Session Cookie
- **响应**:
  ```json
  {
    "success": true,
    "data": {
      "temperature": "float",      // 温度(°C)
      "dissolved_oxygen": "float", // 溶解氧(mg/L)
      "ph": "float",               // pH值
      "water_flow": "float"        // 水流量(m³/s)
    }
  }
  ```

### 2.3 获取环境数据历史记录
- **URL**: `/api/environment/history`
- **方法**: GET
- **认证**: 需要 Session Cookie
- **参数**:
  ```json
  {
    "start_time": "string",  // 开始时间 (ISO格式, 可选)
    "end_time": "string",    // 结束时间 (ISO格式, 可选)
    "limit": "integer",      // 记录数量 (默认100)
    "offset": "integer"      // 偏移量 (默认0)
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
        "dissolved_oxygen": "float",
        "ph": "float",
        "water_flow": "float"
      }
    ],
    "total": "integer"  // 总记录数
  }
  ```

### 2.4 获取环境告警阈值配置
- **URL**: `/api/environment/thresholds`
- **方法**: GET
- **认证**: 需要 Session Cookie
- **响应**:
  ```json
  {
    "success": true,
    "data": {
      "temperature_min": "float",
      "temperature_max": "float",
      "dissolved_oxygen_min": "float",
      "dissolved_oxygen_max": "float",
      "ph_min": "float",
      "ph_max": "float"
    }
  }
  ```

### 2.5 更新环境告警阈值配置
- **URL**: `/api/environment/thresholds`
- **方法**: PUT
- **认证**: 需要 Session Cookie
- **参数**:
  ```json
  {
    "temperature_min": "float",
    "temperature_max": "float",
    "dissolved_oxygen_min": "float",
    "dissolved_oxygen_max": "float",
    "ph_min": "float",
    "ph_max": "float"
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "message": "阈值配置更新成功"
  }
  ```

---

## 3. 设备管理接口

### 3.1 获取设备列表
- **URL**: `/api/devices`
- **方法**: GET
- **认证**: 需要 Session Cookie
- **参数**:
  ```json
  {
    "type": "string",   // 设备类型 (可选)
    "status": "string"  // 设备状态 (online/offline, 可选)
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
        "created_at": "datetime"
      }
    ]
  }
  ```

### 3.2 获取单个设备信息
- **URL**: `/api/devices/{deviceId}`
- **方法**: GET
- **认证**: 需要 Session Cookie
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
      "created_at": "datetime",
      "updated_at": "datetime"
    }
  }
  ```

### 3.3 更新设备状态
- **URL**: `/api/devices/{deviceId}/status`
- **方法**: PATCH
- **认证**: 需要 Session Cookie
- **参数**:
  ```json
  {
    "status": "string"  // 新状态 (online/offline)
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "message": "设备状态更新成功"
  }
  ```

### 3.4 获取设备配置
- **URL**: `/api/devices/{deviceId}/config`
- **方法**: GET
- **认证**: 需要 Session Cookie
- **响应**:
  ```json
  {
    "success": true,
    "data": {
      "config": "object"
    }
  }
  ```

### 3.5 保存设备配置
- **URL**: `/api/devices/{deviceId}/config`
- **方法**: PUT
- **认证**: 需要 Session Cookie
- **参数**:
  ```json
  {
    "config": "object"
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "message": "设备配置保存成功"
  }
  ```

---

## 4. 投喂管理接口

### 4.1 获取投喂计划列表
- **URL**: `/api/feeding/plans`
- **方法**: GET
- **认证**: 需要 Session Cookie
- **参数**:
  ```json
  {
    "device_id": "string",  // 设备ID (可选)
    "status": "string"      // 状态 (可选)
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
- **认证**: 需要 Session Cookie
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
- **认证**: 需要 Session Cookie
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
- **认证**: 需要 Session Cookie
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
- **认证**: 需要 Session Cookie
- **参数**:
  ```json
  {
    "device_id": "string",
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

### 4.6 获取投喂历史记录
- **URL**: `/api/feeding/history`
- **方法**: GET
- **认证**: 需要 Session Cookie
- **参数**:
  ```json
  {
    "device_id": "string",  // 设备ID (可选)
    "start_time": "string", // 开始时间 (可选)
    "end_time": "string"    // 结束时间 (可选)
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

---

## 5. 告警管理接口

### 5.1 获取告警列表
- **URL**: `/api/alerts`
- **方法**: GET
- **认证**: 需要 Session Cookie
- **参数**:
  ```json
  {
    "level": "string",      // 告警级别 (可选)
    "resolved": "boolean",  // 是否已处理 (可选)
    "start_time": "string", // 开始时间 (可选)
    "end_time": "string"    // 结束时间 (可选)
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
        "description": "string",
        "resolved": "boolean"
      }
    ]
  }
  ```

### 5.2 获取单个告警详情
- **URL**: `/api/alerts/{alertId}`
- **方法**: GET
- **认证**: 需要 Session Cookie
- **响应**:
  ```json
  {
    "success": true,
    "data": {
      "id": "integer",
      "title": "string",
      "level": "string",
      "time": "datetime",
      "description": "string",
      "resolved": "boolean",
      "resolved_at": "datetime"
    }
  }
  ```

### 5.3 标记告警为已处理
- **URL**: `/api/alerts/{alertId}/resolve`
- **方法**: PATCH
- **认证**: 需要 Session Cookie
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
- **认证**: 需要 Session Cookie
- **响应**:
  ```json
  {
    "success": true,
    "data": {
      "total": "integer",
      "unresolved": "integer",
      "warning": "integer",
      "error": "integer"
    }
  }
  ```

---

## 6. 日志管理接口

### 6.1 获取系统日志列表
- **URL**: `/api/logs`
- **方法**: GET
- **认证**: 需要 Session Cookie
- **参数**:
  ```json
  {
    "level": "string",      // 日志级别 (INFO/WARNING/ERROR, 可选)
    "module": "string",     // 模块名称 (可选)
    "start_time": "string", // 开始时间 (可选)
    "end_time": "string",   // 结束时间 (可选)
    "page": "integer",      // 页码 (默认1)
    "per_page": "integer"   // 每页数量 (默认50)
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
    ],
    "total": "integer"
  }
  ```

### 6.2 获取单个日志详情
- **URL**: `/api/logs/{logId}`
- **方法**: GET
- **认证**: 需要 Session Cookie
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

### 6.3 获取日志统计数据
- **URL**: `/api/logs/statistics`
- **方法**: GET
- **认证**: 需要 Session Cookie
- **参数**:
  ```json
  {
    "start_time": "string", // 开始时间 (可选)
    "end_time": "string"    // 结束时间 (可选)
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

---

## 7. 数据统计接口

### 7.1 获取系统总览统计
- **URL**: `/api/statistics/overview`
- **方法**: GET
- **认证**: 需要 Session Cookie
- **响应**:
  ```json
  {
    "success": true,
    "data": {
      "totalDevices": "integer",      // 设备总数
      "onlineDevices": "integer",     // 在线设备数
      "totalFeedings": "integer",     // 投喂次数
      "totalAlerts": "integer",       // 告警总数
      "unresolvedAlerts": "integer",  // 未处理告警数
      "totalMonitoring": "integer"    // 监测数据总数
    }
  }
  ```

### 7.2 获取鱼塘趋势数据
- **URL**: `/api/statistics/pond/trend`
- **方法**: GET
- **认证**: 需要 Session Cookie
- **参数**:
  ```json
  {
    "period": "string"  // 时间周期 (7d, 30d, 3m, 默认7d)
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "data": {
      "labels": ["string"],      // 日期标签
      "counts": ["integer"],     // 对应计数
      "statistics": {
        "totalPonds": "integer",
        "newThisMonth": "integer",
        "utilizationRate": "float"
      }
    }
  }
  ```

### 7.3 获取设备状态统计
- **URL**: `/api/statistics/device/status`
- **方法**: GET
- **认证**: 需要 Session Cookie
- **响应**:
  ```json
  {
    "success": true,
    "data": {
      "online": "integer",   // 在线设备数
      "offline": "integer"   // 离线设备数
    }
  }
  ```

### 7.4 获取投喂统计数据
- **URL**: `/api/statistics/feeding`
- **方法**: GET
- **认证**: 需要 Session Cookie
- **参数**:
  ```json
  {
    "start_time": "string",  // 开始时间 (可选)
    "end_time": "string",    // 结束时间 (可选)
    "device_id": "string"    // 设备ID (可选)
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "data": {
      "totalFeedings": "integer",    // 投喂次数
      "totalAmount": "float",        // 投喂总量
      "averageAmount": "float",      // 平均投喂量
      "successRate": "float"         // 成功率
    }
  }
  ```

### 7.5 获取环境数据统计
- **URL**: `/api/statistics/environment`
- **方法**: GET
- **认证**: 需要 Session Cookie
- **参数**:
  ```json
  {
    "start_time": "string",  // 开始时间 (可选)
    "end_time": "string"     // 结束时间 (可选)
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

---

## 错误响应格式

所有API接口在出错时都会返回统一的错误响应格式：

```json
{
  "success": false,
  "message": "错误信息描述",
  "code": "HTTP状态码（可选）"
}
```

### 常见错误代码

| 状态码 | 说明 | 示例 |
|--------|------|------|
| 400 | 请求参数错误 | 缺少必填参数、参数类型不符 |
| 401 | 未授权 | 未登录或 Session 失效 |
| 403 | 权限不足 | 无权访问该资源 |
| 404 | 资源不存在 | 指定ID的资源不存在 |
| 500 | 服务器内部错误 | 数据库错误、系统异常 |

---

## 使用示例

### 登录示例 (Python Requests)
```python
import requests

# 登录
response = requests.post('http://localhost:5000/api/auth/login', 
    json={
        'username': 'admin',
        'password': 'password123'
    })

if response.json()['success']:
    # 后续请求会自动携带 Cookie
    user_response = requests.get('http://localhost:5000/api/auth/user', 
        cookies=response.cookies)
```

### 获取设备列表示例 (JavaScript Fetch)
```javascript
// 假设已登录
const response = await fetch('http://localhost:5000/api/devices', {
    method: 'GET',
    credentials: 'include'  // 自动携带 Cookie
});

const data = await response.json();
if (data.success) {
    console.log('设备列表:', data.data);
}
```

---

## 常见问题

**Q: 如何处理 Session 过期？**
A: 当收到 401 错误时，表示 Session 已过期，需要重新登录。

**Q: CORS 跨域请求时如何包含 Cookie？**
A: 需要在请求中设置 `credentials: 'include'` (JavaScript) 或 `withCredentials: true` (Axios)。

**Q: API 响应中的日期格式是什么？**
A: 所有日期时间均采用 ISO 8601 格式，例如：`2024-01-01T12:30:00`。
