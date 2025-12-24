# 基于OpenHarmony的海洋渔业智能投喂系统

## 项目简介

这是一个完整的海洋渔业智能投喂系统,包含三个部分:
- **后端服务** (Flask + MySQL): 提供数据存储和业务逻辑
- **前端界面** (Vue 3 + Vuetify): 可视化监控和管理
- **OpenHarmony硬件层** (ArkTS + 硬件模拟器): 设备端数据采集和控制

## 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                      前端界面                             │
│                  Vue 3 + Vuetify                         │
│         (环境监控、投喂管理、数据可视化)                   │
└─────────────────┬───────────────────────────────────────┘
                  │ HTTP REST API
┌─────────────────▼───────────────────────────────────────┐
│                     后端服务                              │
│                  Flask + MySQL                           │
│      (用户认证、数据存储、设备管理、投喂算法)              │
└─────────────────┬───────────────────────────────────────┘
                  │ HTTP REST API
┌─────────────────▼───────────────────────────────────────┐
│              OpenHarmony设备层                            │
│            FisheryDevice项目 (ArkTS)                     │
│    (传感器模拟、投喂器控制、数据上报、指令接收)            │
└─────────────────────────────────────────────────────────┘
```

## 核心功能

### 1. 环境监测
- 水温传感器 (18-32°C)
- 溶解氧传感器 (3-12 mg/L)
- pH传感器 (6.5-8.5)
- 水流量传感器 (0.5-5.0 m³/s)

### 2. 智能投喂
- 基于生物量和环境因子的智能投喂算法
- 手动投喂控制
- 定时投喂计划
- 投喂历史记录

### 3. 告警管理
- 环境参数阈值告警
- 设备状态告警
- 实时告警推送

### 4. 数据统计
- 环境数据趋势图表
- 投喂数据分析
- 系统运行日志

## 快速开始

### 环境要求

- **后端**: Python 3.8+, MySQL 8.0+
- **前端**: Node.js 14+, pnpm
- **OpenHarmony**: DevEco Studio 3.1+, OpenHarmony SDK 3.2+

### 1. 启动后端服务

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_db.py

# 启动服务
python run.py
```

后端服务将在 `http://localhost:5000` 启动。

### 2. 启动前端界面

```bash
cd frontend

# 安装依赖
pnpm install

# 启动开发服务器
pnpm dev
```

前端界面将在 `http://localhost:5173` 启动。

### 3. OpenHarmony设备层

OpenHarmony应用已集成到 `FisheryDevice` 目录中。可使用DevEco Studio开发和调试。

#### 使用DevEco Studio:

1. **打开项目**
   - 启动DevEco Studio
   - 选择 `File` > `Open` > 浏览到 `FisheryDevice` 目录

2. **配置环境**
   - 确保OpenHarmony SDK已安装
   - 配置硬件模拟器或连接真实设备

3. **运行应用**
   - 点击 `Run` 按钮或按 `Shift+F10`
   - 等待编译、打包和安装完成

4. **查看日志**
   ```bash
   # 在DevEco Studio的Logcat窗口查看日志
   # 或使用hdc命令
   hdc_std shell hilog
   ```

## 项目结构

```
demo411/
├── backend/                    # 后端服务 (Flask + MySQL)
│   ├── app/
│   │   ├── models/            # 数据模型 (User, Device, Alert, Feeding等)
│   │   ├── routes/            # API路由 (auth, environment, devices, feeding, alerts, logs, statistics)
│   │   ├── services/          # 业务逻辑 (feeding_algorithm等)
│   │   └── utils/             # 工具类 (decorators, validators)
│   ├── config.py              # Flask配置文件
│   ├── requirements.txt       # Python依赖
│   ├── init_db.py             # 数据库初始化脚本
│   ├── run.py                 # 启动脚本
│   └── reset_and_init.bat     # Windows批处理脚本
│
├── frontend/                   # 前端界面 (Vue 3 + Vuetify)
│   ├── src/
│   │   ├── components/        # Vue组件 (cards, charts, forms)
│   │   ├── pages/             # 页面 (alerts, devices, feeding, logs, monitoring, statistics)
│   │   ├── services/          # API服务
│   │   ├── stores/            # Pinia状态管理
│   │   ├── plugins/           # 插件配置
│   │   ├── router/            # 路由配置
│   │   ├── layouts/           # 页面布局
│   │   ├── assets/            # 静态资源
│   │   ├── styles/            # 样式文件
│   │   ├── App.vue            # 根组件
│   │   └── main.js            # 入口文件
│   ├── package.json           # Node依赖
│   ├── vite.config.mjs        # Vite配置
│   ├── jsconfig.json          # JavaScript配置
│   └── index.html             # HTML模板
│
├── FisheryDevice/             # OpenHarmony设备层 (ArkTS)
│   ├── entry/
│   │   └── src/
│   │       └── main/
│   │           ├── ets/       # 源代码
│   │           └── resources/ # 资源文件
│   ├── oh-package.json5       # OpenHarmony项目配置
│   └── hvigorfile.ts          # 编译配置
│
├── API_DOCUMENTATION.md       # API接口文档
├── DATABASE_DESIGN.md         # 数据库设计文档
├── PROJECT_README.md          # 项目说明(本文件)
└── package.json               # 根项目配置
```

## 技术栈

### 后端
- **Flask** 3.0.0 - Web框架
- **Flask-SQLAlchemy** 3.1.1 - ORM
- **Flask-Cors** 4.0.0 - 跨域资源共享
- **Flask-Session** 0.5.0 - Session管理
- **PyMySQL** 1.1.0 - MySQL驱动
- **Werkzeug** 3.0.1 - WSGI工具库
- **python-dotenv** 1.0.0 - 环境变量管理
- **numpy** 1.26.2 - 数值计算库
- **MySQL** 8.0+ - 数据库
- **Python** 3.8+ - 编程语言

### 前端
- **Vue** 3.5.21 - 前端框架
- **Vuetify** 3.10.1 - Material Design组件库
- **Vue Router** 4.5.1 - 路由管理
- **Pinia** 3.0.3 - 状态管理
- **Vite** - 现代化打包工具
- **ApexCharts** 5.3.5 - 数据图表库
- **Axios** 1.13.2 - HTTP客户端
- **Node.js** 14+ - JavaScript运行时

### OpenHarmony设备层
- **ArkTS** - OpenHarmony开发语言
- **DevEco Studio** - IDE开发工具和硬件模拟器
- **OpenHarmony SDK** - 平台SDK
- **硬件模拟器** - DevEco Studio内置模拟器或真实设备

## API接口

详细API文档请参考: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

主要接口:
- `/api/auth/*` - 用户认证
- `/api/environment/*` - 环境监测
- `/api/devices/*` - 设备管理
- `/api/feeding/*` - 投喂管理
- `/api/alerts/*` - 告警管理
- `/api/logs/*` - 日志管理

## 数据库设计

详细数据库设计请参考: [DATABASE_DESIGN.md](DATABASE_DESIGN.md)

主要表:
- `users` - 用户表
- `environment_data` - 环境数据表
- `devices` - 设备表
- `feeding_plans` - 投喂计划表
- `feeding_history` - 投喂历史表
- `alerts` - 告警表
- `logs` - 系统日志表

## 核心模块说明

### 后端模块

#### 1. 认证模块 (`routes/auth.py`)
- 用户注册和登录
- JWT令牌管理
- Session管理

#### 2. 环境监测模块 (`routes/environment.py`)
- 环境数据读取
- 环境阈值配置
- 环境告警

#### 3. 设备管理模块 (`routes/devices.py`)
- 设备注册和管理
- 设备状态查询
- 设备命令下发

#### 4. 投喂管理模块 (`routes/feeding.py`)
- 投喂计划管理
- 投喂记录
- 智能投喂算法 (`services/feeding_algorithm.py`)

#### 5. 告警管理模块 (`routes/alerts.py`)
- 告警配置
- 告警历史查询
- 告警统计

#### 6. 日志管理模块 (`routes/logs.py`)
- 系统日志记录
- 日志查询

#### 7. 数据统计模块 (`routes/statistics.py`)
- 数据聚合和统计
- 趋势分析

### 前端模块

#### 页面
- **Landing.vue** - 登录页面
- **monitoring.vue** - 监控仪表板
- **devices.vue** - 设备管理
- **feeding.vue** - 投喂管理
- **alerts.vue** - 告警查看
- **statistics.vue** - 数据统计
- **logs.vue** - 日志查询

#### 组件
- **cards/** - 信息卡片组件
- **charts/** - 数据图表组件
- **forms/** - 表单组件

### OpenHarmony设备层模块

- **传感器模拟** - 模拟水温、溶解氧、pH等传感器
- **数据采集** - 定时采集和上报数据
- **投喂控制** - 控制投喂器执行投喂
- **设备管理** - 设备注册、状态上报、指令接收

## 快速参考

### 数据库初始化

```bash
cd backend
# 方式1: 使用Python脚本
python init_db.py

# 方式2: 使用批处理脚本(Windows)
reset_and_init.bat
```

### API端点列表

| 功能 | 基础路径 | 说明 |
|------|----------|------|
| 认证 | `/api/auth` | 用户登录、注册、信息查询 |
| 环境 | `/api/environment` | 环境数据采集、阈值管理 |
| 设备 | `/api/devices` | 设备注册、状态查询、命令 |
| 投喂 | `/api/feeding` | 投喂计划、历史记录、算法 |
| 告警 | `/api/alerts` | 告警配置、历史查询、统计 |
| 日志 | `/api/logs` | 系统日志查询 |
| 统计 | `/api/statistics` | 数据聚合和趋势分析 |

详细文档见 [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## 测试场景

### 1. 环境数据采集测试
- 启动设备端应用
- 观察日志,确认数据采集正常
- 在前端查看实时数据更新

### 2. 投喂功能测试
- 在前端创建投喂计划
- 手动触发投喂
- 验证设备端执行投喂
- 检查投喂历史记录

### 3. 告警功能测试
- 模拟环境参数异常
- 验证告警触发
- 检查告警列表

### 4. 多设备测试
- 在DevEco Studio中启动多个硬件模拟器实例
- 配置不同设备ID
- 验证多设备数据采集

## 生产部署

### 后端部署

```bash
cd backend

# 安装生产依赖
pip install -r requirements.txt
pip install gunicorn

# 使用Gunicorn启动(多工作进程)
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# 或使用Waitress
pip install waitress
waitress-serve --port=5000 run:app
```

修改 `backend/config.py` 的生产配置:
```python
SESSION_COOKIE_SECURE = True  # HTTPS环境下
```

### 前端部署

```bash
cd frontend

# 构建生产版本
pnpm install
pnpm build

# 输出在dist目录，部署到Web服务器(Nginx、Apache等)
```

Nginx配置示例:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### OpenHarmony设备部署

部署到真实OpenHarmony设备:
1. 配置实际硬件传感器接口
2. 更新后端API地址配置
3. 编译并安装应用
4. 根据实际环境调整算法参数

## 扩展功能规划

### 已实现
- ✅ 用户认证系统(注册、登录、Session管理)
- ✅ 环境数据采集和实时监测
- ✅ 智能投喂算法
- ✅ 设备管理和命令下发
- ✅ 告警系统(环境阈值告警、设备告警)
- ✅ 数据可视化(图表展示、趋势分析)
- ✅ OpenHarmony设备层(传感器模拟、数据上报)
- ✅ 系统日志和操作审计

### 计划中功能
- ⏳ WebSocket实时通信(提升数据推送实时性)
- ⏳ MQTT协议支持(支持更多IoT设备)
- ⏳ 设备OTA升级功能
- ⏳ 机器学习优化投喂算法
- ⏳ 移动端应用(小程序或App)
- ⏳ 多池塘管理
- ⏳ 视频监控集成
- ⏳ 数据导出功能(Excel、PDF报表)

## 常见问题

### Q1: MySQL连接错误
A: 
- 确保MySQL服务已启动
- 检查 `backend/config.py` 中的数据库配置
- 默认配置: `mysql+pymysql://root:root@localhost:3306/fishery?charset=utf8mb4`
- 修改用户名/密码后需要重新初始化数据库

### Q2: 前端无法连接后端
A: 
- 检查后端服务是否在 `http://localhost:5000` 运行
- 检查CORS配置是否包含前端地址
- 打开浏览器开发工具查看网络请求错误

### Q3: 数据未上报(OpenHarmony设备)
A: 
- 在DevEco Studio的Logcat查看设备日志确认采集是否正常
- 检查网络连接和后端地址配置
- 确保后端API接口可访问
- 模拟器访问宿主机使用 `10.0.2.2` 或直接使用宿主机IP

### Q4: 环境数据异常
A: 
- 检查 `backend/services/feeding_algorithm.py` 中的算法参数
- 验证数据库中的环境阈值配置
- 检查是否有异常告警

### Q5: 如何修改后端端口
A: 
- 编辑 `backend/run.py` 中的 `app.run()` 参数
- 修改 `port=5000` 为其他端口号
- 同时更新前端配置中的API地址

## 项目文档

- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - 详细API接口文档
- [DATABASE_DESIGN.md](DATABASE_DESIGN.md) - 数据库设计文档

## 贡献指南

欢迎提交Issue和Pull Request!

### 开发流程

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 许可证

MIT License - 详见LICENSE文件

## 联系信息

- 项目路径: `c:\Users\19113\Desktop\demo411`
- 问题反馈: 提交Issue到项目仓库
- 技术支持: 查看相关文档或提交Issue

## 致谢

感谢以下开源项目和社区的支持:

- [OpenHarmony](https://www.openharmony.cn/) - 开源操作系统
- [Flask](https://flask.palletsprojects.com/) - Python Web框架
- [Vue.js](https://vuejs.org/) - JavaScript框架
- [Vuetify](https://vuetifyjs.com/) - Material Design组件库
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python ORM
