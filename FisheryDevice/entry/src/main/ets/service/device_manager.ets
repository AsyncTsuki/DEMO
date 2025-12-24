import { Logger } from '../utils/logger';
import { HttpClient } from '../network/http_client';
import {
  DeviceConfig,
  EnvironmentData,
  FeedingRecord,
  DeviceStatus,
  ApiResponse,
  DeviceStatusUpdateRequest,
  EnvironmentDataUploadRequest,
  FeedingRecordUploadRequest
} from '../common/types';
import { 
  TemperatureSensor, 
  OxygenSensor, 
  PhSensor, 
  WaterFlowSensor 
} from '../device/sensors';
import { FeederController } from '../device/feeder';

/**
 * 设备管理器
 * 负责传感器数据采集、投喂控制、数据上报等
 */
export class DeviceManager {
  private static instance: DeviceManager;
  private config: DeviceConfig;
  private httpClient: HttpClient;

  // 传感器
  private tempSensor: TemperatureSensor;
  private oxygenSensor: OxygenSensor;
  private phSensor: PhSensor;
  private flowSensor: WaterFlowSensor;

  // 投喂器
  private feeder: FeederController;

  // 定时器
  private dataCollectTimer: number = -1;
  private dataUploadTimer: number = -1;

  // 数据缓存
  private dataBuffer: EnvironmentData[] = [];

  private constructor(config: DeviceConfig) {
    this.config = config;
    
    // 初始化HTTP客户端
    this.httpClient = new HttpClient(
      config.server.host + config.server.apiPrefix,
      config.server.timeout,
      config.server.retryTimes
    );

    // 初始化传感器
    this.tempSensor = new TemperatureSensor(
      config.sensors.temperature.min,
      config.sensors.temperature.max
    );
    this.oxygenSensor = new OxygenSensor(
      config.sensors.dissolvedOxygen.min,
      config.sensors.dissolvedOxygen.max
    );
    this.phSensor = new PhSensor(
      config.sensors.ph.min,
      config.sensors.ph.max
    );
    this.flowSensor = new WaterFlowSensor(
      config.sensors.waterFlow.min,
      config.sensors.waterFlow.max
    );

    // 初始化投喂器
    this.feeder = new FeederController(
      config.feeder.capacity,
      config.feeder.minAmount,
      config.feeder.maxAmount,
      config.feeder.speed
    );
  }

  /**
   * 获取单例
   */
  static getInstance(config?: DeviceConfig): DeviceManager {
    if (!DeviceManager.instance && config) {
      DeviceManager.instance = new DeviceManager(config);
    }
    return DeviceManager.instance;
  }

  /**
   * 启动设备管理器
   */
  async start(): Promise<void> {
    Logger.info('Starting Device Manager...');

    try {
      // 注册设备
      await this.registerDevice();

      // 上报设备状态为在线
      await this.updateDeviceStatus('online');

      // 启动数据采集
      this.startDataCollection();

      // 启动数据上报
      this.startDataUpload();

      Logger.info('Device Manager started successfully');
    } catch (err) {
      Logger.error('Failed to start Device Manager: %{public}s', JSON.stringify(err) || 'unknown error');
      Logger.error('Device Manager start error occurred');
    }
  }

  /**
   * 停止设备管理器
   */
  async stop(): Promise<void> {
    Logger.info('Stopping Device Manager...');

    // 停止定时器
    if (this.dataCollectTimer !== -1) {
      clearInterval(this.dataCollectTimer);
      this.dataCollectTimer = -1;
    }
    if (this.dataUploadTimer !== -1) {
      clearInterval(this.dataUploadTimer);
      this.dataUploadTimer = -1;
    }

    // 上报剩余数据
    if (this.dataBuffer.length > 0) {
      await this.uploadData();
    }

    // 上报设备状态为离线
    await this.updateDeviceStatus('offline');

    Logger.info('Device Manager stopped');
  }

  /**
   * 注册设备
   */
  private async registerDevice(): Promise<void> {
    Logger.info('Registering device: %{public}s', this.config.deviceId);
    
    // 这里可以调用后端注册接口
    // 目前假设设备已在后端注册
  }

  /**
   * 更新设备状态
   */
  private async updateDeviceStatus(status: string): Promise<void> {
    try {
      const requestData: DeviceStatusUpdateRequest = { status };
      const response: ApiResponse<Object> = await this.httpClient.patch(
        `/devices/${this.config.deviceId}/status`,
        requestData
      );

      if (response.success) {
        Logger.info('Device status updated: %{public}s', status);
      } else {
        Logger.error('Failed to update device status: %{public}s', response.message || 'unknown error');
      }
    } catch (err) {
      Logger.error('Update device status error: %{public}s', JSON.stringify(err) || 'unknown error');
    }
  }

  /**
   * 启动数据采集
   */
  private startDataCollection(): void {
    const interval = this.config.sensors.temperature.interval;
    
    Logger.info('Starting data collection (interval: %{public}d ms)', interval);

    this.dataCollectTimer = setInterval(() => {
      this.collectData();
    }, interval);

    // 立即采集一次
    this.collectData();
  }

  /**
   * 采集环境数据
   */
  private collectData(): void {
    const data: EnvironmentData = {
      temperature: this.tempSensor.readTemperature(),
      dissolvedOxygen: this.oxygenSensor.readOxygen(),
      ph: this.phSensor.readPh(),
      waterFlow: this.flowSensor.readFlow(),
      timestamp: Date.now()
    };

    // 添加到缓存
    this.dataBuffer.push(data);

    Logger.debug('Data collected, buffer size: %{public}d', this.dataBuffer.length);

    // 如果缓存满了,立即上传
    if (this.dataBuffer.length >= this.config.upload.batchSize) {
      this.uploadData();
    }
  }

  /**
   * 启动数据上报
   */
  private startDataUpload(): void {
    const interval = this.config.upload.interval;
    
    Logger.info('Starting data upload (interval: %{public}d ms)', interval);

    this.dataUploadTimer = setInterval(() => {
      if (this.dataBuffer.length > 0) {
        this.uploadData();
      }
    }, interval);
  }

  /**
   * 上传环境数据
   */
  private async uploadData(): Promise<void> {
    if (this.dataBuffer.length === 0) {
      return;
    }

    // 取出要上传的数据
    const dataToUpload = this.dataBuffer.splice(0, this.config.upload.batchSize);

    try {
      // 上传最新的一条数据(后端接口设计为单条)
      const latestData = dataToUpload[dataToUpload.length - 1];
      
      const requestData: EnvironmentDataUploadRequest = {
        temperature: latestData.temperature,
        dissolved_oxygen: latestData.dissolvedOxygen,
        ph: latestData.ph,
        water_flow: latestData.waterFlow,
        timestamp: new Date(latestData.timestamp).toISOString()
      };
      
      const response: ApiResponse<Object> = await this.httpClient.post('/environment/data', requestData);

      if (response.success) {
        Logger.info('Environment data uploaded successfully');
      } else {
        Logger.error('Failed to upload data: %{public}s', response.message || 'unknown error');
        // 上传失败,重新加入缓存
        this.dataBuffer.unshift(...dataToUpload);
      }
    } catch (err) {
      Logger.error('Upload data error: %{public}s', JSON.stringify(err) || 'unknown error');
      // 上传失败,重新加入缓存
      this.dataBuffer.unshift(...dataToUpload);
    }
  }

  /**
   * 执行投喂
   */
  async executeFeed(amount: number): Promise<void> {
    Logger.info('Executing feed: %{public}f kg', amount);

    try {
      // 执行投喂
      const record = await this.feeder.feed(amount);
      record.deviceId = this.config.deviceId;

      // 上报投喂记录
      await this.uploadFeedingRecord(record);
    } catch (err) {
      Logger.error('Feed execution error: %{public}s', JSON.stringify(err) || 'unknown error');
      Logger.error('Feed execution error occurred');
    }
  }

  /**
   * 上报投喂记录
   */
  private async uploadFeedingRecord(record: FeedingRecord): Promise<void> {
    try {
      const requestData: FeedingRecordUploadRequest = {
        device_id: record.deviceId,
        amount: record.amount,
        type: record.type,
        operator: record.operator,
        time: new Date(record.time).toISOString(),
        status: record.status
      };
      
      const response: ApiResponse<Object> = await this.httpClient.post('/feeding/history', requestData);

      if (response.success) {
        Logger.info('Feeding record uploaded successfully');
      } else {
        Logger.error('Failed to upload feeding record: %{public}s', response.message || 'unknown error');
      }
    } catch (err) {
      Logger.error('Upload feeding record error: %{public}s', JSON.stringify(err) || 'unknown error');
    }
  }

  /**
   * 获取设备状态
   */
  getDeviceStatus(): DeviceStatus {
    const feederStatus = this.feeder.getStatus();
    
    return {
      deviceId: this.config.deviceId,
      status: 'online',
      lastUpdate: Date.now(),
      sensorStatus: {
        temperature: this.tempSensor.getStatus(),
        dissolvedOxygen: this.oxygenSensor.getStatus(),
        ph: this.phSensor.getStatus(),
        waterFlow: this.flowSensor.getStatus()
      },
      feederStatus: {
        online: feederStatus.status !== 'error',
        capacity: feederStatus.remaining
      }
    };
  }

  /**
   * 获取当前环境数据
   */
  getCurrentEnvironmentData(): EnvironmentData {
    return {
      temperature: this.tempSensor.readTemperature(),
      dissolvedOxygen: this.oxygenSensor.readOxygen(),
      ph: this.phSensor.readPh(),
      waterFlow: this.flowSensor.readFlow(),
      timestamp: Date.now()
    };
  }
}
