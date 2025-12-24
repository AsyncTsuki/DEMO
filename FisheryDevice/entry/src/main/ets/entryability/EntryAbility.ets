import { UIAbility, Want, AbilityConstant } from '@kit.AbilityKit';
import { window } from '@kit.ArkUI';
import { Logger } from '../utils/logger';
import { StorageManager } from '../utils/storage';
import { DeviceManager } from '../service/device_manager';
import { DeviceConfig } from '../common/types';
import resourceManager from '@ohos.resourceManager';

/**
 * 应用主入口
 */
export default class EntryAbility extends UIAbility {
  private deviceManager: DeviceManager | null = null;

  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    Logger.info('Application onCreate');
    
    // 初始化存储
    this.initStorage();
    
    // 加载设备配置并启动设备管理器
    this.loadDeviceConfig();
  }

  onDestroy(): void {
    Logger.info('Application onDestroy');
    
    // 停止设备管理器
    if (this.deviceManager) {
      this.deviceManager.stop();
    }
  }

  onWindowStageCreate(windowStage: window.WindowStage): void {
    Logger.info('Ability onWindowStageCreate');

    windowStage.loadContent('pages/Index', (err) => {
      if (err.code) {
        Logger.error('Failed to load the content. Cause: %{public}s', JSON.stringify(err) || 'unknown error');
        return;
      }
      Logger.info('Succeeded in loading the content.');
    });
  }

  onWindowStageDestroy(): void {
    Logger.info('Ability onWindowStageDestroy');
  }

  onForeground(): void {
    Logger.info('Ability onForeground');
  }

  onBackground(): void {
    Logger.info('Ability onBackground');
  }

  /**
   * 初始化本地存储
   */
  private async initStorage(): Promise<void> {
    try {
      const storage = StorageManager.getInstance();
      await storage.init(this.context);
      Logger.info('Storage initialized');
    } catch (err) {
      Logger.error('Failed to init storage: %{public}s', JSON.stringify(err) || 'unknown error');
    }
  }

  /**
   * 加载设备配置
   */
  private async loadDeviceConfig(): Promise<void> {
    try {
      // 从rawfile加载配置文件
      const resMgr = this.context.resourceManager;
      const configData = await resMgr.getRawFileContent('device_config.json');
      const configStr = String.fromCharCode(...new Uint8Array(configData.buffer));
      const config: DeviceConfig = JSON.parse(configStr);
      
      Logger.info('Device config loaded: %{public}s', config.deviceId);
      
      // 启动设备管理器
      await this.startDeviceManager(config);
    } catch (err) {
      Logger.error('Failed to load device config: %{public}s', JSON.stringify(err) || 'unknown error');
    }
  }

  /**
   * 启动设备管理器
   */
  private async startDeviceManager(config: DeviceConfig): Promise<void> {
    try {
      this.deviceManager = DeviceManager.getInstance(config);
      await this.deviceManager.start();
      Logger.info('Device Manager started');
    } catch (err) {
      Logger.error('Failed to start Device Manager: %{public}s', JSON.stringify(err) || 'unknown error');
    }
  }
}