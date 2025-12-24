# 基于OpenHarmony的海洋渔业智能投喂系统

## 项目简介

这是一个完整的海洋渔业智能投喂系统,包含三个部分:
- **后端服务** (Flask + MySQL): 提供数据存储和业务逻辑
- **前端界面** (Vue 3 + Vuetify): 可视化监控和管理
- **OpenHarmony硬件层** (ArkTS + QEMU): 设备端数据采集和控制

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

前端界面将在 `http://localhost:3000` 启动。

### 3. 启动OpenHarmony设备层

项目已集成到 `FisheryDevice` 目录中。

#### 使用DevEco Studio开发:

1. **打开项目**
   - 启动DevEco Studio
   - 打开 `C:\Users\19113\Desktop\demo411\FisheryDevice`

2. **配置设备**
   - 选择本地模拟器或远程模拟器
   - 或连接真实设备

3. **运行应用**
   - 点击运行按钮 ▶️
   - 等待编译和安装

4. **查看日志**
   ```bash
   # 在DevEco Studio中查看日志
   # 或使用hdc命令
   hdc shell hilog | findstr "Fishery"
   ```

## 项目结构

```
demo411/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── models/            # 数据模型
│   │   ├── routes/            # API路由
│   │   ├── services/          # 业务逻辑
│   │   └── utils/             # 工具类
│   ├── config.py              # 配置文件
│   ├── requirements.txt       # Python依赖
│   └── run.py                 # 启动脚本
│
├── frontend/                   # 前端界面
│   ├── src/
│   │   ├── components/        # Vue组件
│   │   ├── pages/             # 页面
│   │   ├── services/          # API服务
│   │   └── stores/            # 状态管理
│   ├── package.json           # Node依赖
│   └── vite.config.mjs        # Vite配置
│
├── FisheryDevice/             # OpenHarmony设备层
│   └── entry/
│       └── src/
│           └── main/
│               ├── ets/
│               │   ├── common/          # 公共类型定义
│               │   ├── utils/           # 工具类(日志、存储)
│               │   ├── device/          # 设备层(传感器、投喂器)
│               │   ├── network/         # 网络层(HTTP客户端)
│               │   ├── service/         # 业务层(设备管理器)
│               │   ├── entryability/    # 应用入口
│               │   └── pages/           # 页面
│               └── resources/
│                   └── rawfile/
│                       └── device_config.json  # 设备配置
│
├── API_DOCUMENTATION.md       # API接口文档
├── DATABASE_DESIGN.md         # 数据库设计文档
└── PROJECT_README.md          # 项目说明(本文件)
```

## 技术栈

### 后端
- Flask 2.3+
- SQLAlchemy 2.0+
- MySQL 8.0+
- JWT认证
- Flask-CORS

### 前端
- Vue 3
- Vuetify 3
- Vite
- Pinia (状态管理)
- Chart.js (图表)
- Axios (HTTP客户端)

### OpenHarmony设备层
- ArkTS (OpenHarmony开发语言)
- DevEco Studio (IDE)
- OpenHarmony SDK API 20
- 本地或远程模拟器
- HTTP网络通信

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

## OpenHarmony设备层特性

### 传感器模拟
- 使用正弦波 + 随机噪声模拟真实传感器数据
- 支持参数配置(范围、频率、基准值)
- 可注入异常数据测试告警功能

### 数据采集与上报
- 定时采集环境数据(默认30秒)
- 批量缓存数据减少网络请求
- 断线重传机制保证数据完整性
- 重试机制提高可靠性

### 投喂控制
- 模拟真实投喂过程(速度、延迟)
- 饲料余量管理
- 投喂成功/失败模拟
- 自动上报投喂记录

### 设备管理
- 自动注册设备
- 定时上报设备状态
- 远程接收控制指令
- 故障检测与恢复

## 开发调试

### 后端调试
```bash
cd backend
python run.py  # 开发模式,自动重载
```

### 前端调试
```bash
cd frontend
pnpm dev  # 热重载开发服务器
```

### OpenHarmony调试
```bash
# 查看实时日志
hdc_std shell hilog | findstr "Fishery"

# 查看设备列表
hdc_std list targets

# 重新安装应用
hdc_std install -r app.hap
```

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
- 启动多个QEMU实例
- 配置不同设备ID
- 验证多设备数据采集

## 部署

### 后端部署
```bash
# 使用生产级WSGI服务器
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### 前端部署
```bash
cd frontend
pnpm build  # 构建生产版本
# 将dist目录部署到Web服务器
```

### OpenHarmony设备部署
- 使用真实OpenHarmony设备替代QEMU
- 配置实际传感器硬件接口
- 部署到池塘现场

## 扩展功能

### 已实现
- ✅ 环境数据采集
- ✅ 智能投喂算法
- ✅ 设备管理
- ✅ 告警系统
- ✅ 数据可视化
- ✅ OpenHarmony设备层

### 计划中
- ⏳ MQTT协议支持(提升实时性)
- ⏳ 设备OTA升级
- ⏳ 机器学习优化投喂算法
- ⏳ 移动端App
- ⏳ 多池塘管理
- ⏳ 视频监控集成

## 常见问题

### Q1: QEMU无法启动?
A: 检查镜像文件路径、QEMU版本,参考 [QEMU_GUIDE.md](openharmony/QEMU_GUIDE.md) 排查。

### Q2: 设备无法连接后端?
A: 
- 检查后端服务是否运行
- 验证网络配置(防火墙、IP地址)
- QEMU访问宿主机使用 `10.0.2.2`

### Q3: 数据未上报?
A: 
- 查看设备日志确认采集是否正常
- 检查网络连接
- 验证API接口地址配置

### Q4: 如何添加新的传感器?
A: 
- 在 `openharmony/device/sensors.ets` 中创建新传感器类
- 继承 `BaseSensor` 基类
- 在 `DeviceManager` 中注册并使用

## 贡献

欢迎提交Issue和Pull Request!

## 许可证

MIT License

## 联系方式

- 项目地址: c:\Users\19113\Desktop\demo411
- 文档: 见项目根目录的各个MD文件

## 致谢

- OpenHarmony社区
- Vue.js团队
- Vuetify团队
- Flask社区
