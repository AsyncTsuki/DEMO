/**
 * 设备配置管理
 */
export interface DeviceConfig {
  deviceId: string;           // 设备ID
  deviceName: string;         // 设备名称
  deviceType: string;         // 设备类型
  location: string;           // 设备位置
  server: ServerConfig;       // 服务器配置
  sensors: SensorConfig;      // 传感器配置
  feeder: FeederConfig;       // 投喂器配置
  upload: UploadConfig;       // 上传配置
}

export interface ServerConfig {
  host: string;               // 后端地址
  apiPrefix: string;          // API前缀
  timeout: number;            // 超时时间(ms)
  retryTimes: number;         // 重试次数
}

export interface SensorItemConfig {
  enabled: boolean;
  min: number;
  max: number;
  interval: number;
}

export interface SensorConfig {
  temperature: SensorItemConfig;
  dissolvedOxygen: SensorItemConfig;
  ph: SensorItemConfig;
  waterFlow: SensorItemConfig;
}

export interface FeederConfig {
  enabled: boolean;
  capacity: number;           // 饲料容量(kg)
  minAmount: number;          // 最小投喂量(kg)
  maxAmount: number;          // 最大投喂量(kg)
  speed: number;              // 投喂速度(kg/s)
}

export interface UploadConfig {
  interval: number;           // 上传间隔(ms)
  batchSize: number;          // 批量上传大小
  retryInterval: number;      // 重试间隔(ms)
}

/**
 * 设备状态更新请求
 */
export interface DeviceStatusUpdateRequest {
  status: string;
}

/**
 * 环境数据上报请求
 */
export interface EnvironmentDataUploadRequest {
  temperature: number;
  dissolved_oxygen: number;
  ph: number;
  water_flow: number;
  timestamp: string;
}

/**
 * 投喂记录上报请求
 */
export interface FeedingRecordUploadRequest {
  device_id: string;
  amount: number;
  type: string;
  operator: string;
  time: string;
  status: string;
}

/**
 * 环境数据结构
 */
export interface EnvironmentData {
  temperature: number;        // 水温(°C)
  dissolvedOxygen: number;    // 溶解氧(mg/L)
  ph: number;                 // pH值
  waterFlow: number;          // 水流量(m³/s)
  timestamp: number;          // 时间戳
}

/**
 * 投喂记录结构
 */
export interface FeedingRecord {
  deviceId: string;
  amount: number;             // 投喂量(kg)
  type: string;               // 类型: auto/manual
  operator: string;           // 操作者
  time: number;               // 时间戳
  status: string;             // 状态: success/failed
}

export interface SensorStatusConfig {
  temperature: boolean;
  dissolvedOxygen: boolean;
  ph: boolean;
  waterFlow: boolean;
}

export interface FeederStatusConfig {
  online: boolean;
  capacity: number;         // 剩余饲料(kg)
}

/**
 * 设备状态
 */
export interface DeviceStatus {
  deviceId: string;
  status: string;             // online/offline
  lastUpdate: number;         // 最后更新时间
  sensorStatus: SensorStatusConfig;
  feederStatus: FeederStatusConfig;
}

/**
 * API响应结构
 */
export interface ApiResponse<T = Object> {
  success: boolean;
  message?: string;
  data?: T;
  code?: string;
}

/**
 * 默认配置
 */
export const DEFAULT_CONFIG: DeviceConfig = {
  deviceId: 'DEVICE_001',
  deviceName: '1号池塘传感器',
  deviceType: 'sensor',
  location: '1号池塘',
  server: {
    host: 'http://localhost:5000',
    apiPrefix: '/api',
    timeout: 5000,
    retryTimes: 3
  },
  sensors: {
    temperature: {
      enabled: true,
      min: 18.0,
      max: 32.0,
      interval: 30000  // 30秒
    },
    dissolvedOxygen: {
      enabled: true,
      min: 3.0,
      max: 12.0,
      interval: 30000
    },
    ph: {
      enabled: true,
      min: 6.5,
      max: 8.5,
      interval: 30000
    },
    waterFlow: {
      enabled: true,
      min: 0.5,
      max: 5.0,
      interval: 30000
    }
  },
  feeder: {
    enabled: true,
    capacity: 100.0,
    minAmount: 0.1,
    maxAmount: 10.0,
    speed: 0.5  // 0.5kg/s
  },
  upload: {
    interval: 30000,      // 30秒上传一次
    batchSize: 10,
    retryInterval: 5000
  }
};
