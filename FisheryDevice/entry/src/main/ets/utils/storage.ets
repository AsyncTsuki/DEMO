import preferences from '@ohos.data.preferences';
import { Logger } from './logger';

/**
 * 本地存储管理
 */
export class StorageManager {
  private static instance: StorageManager;
  private preferences: preferences.Preferences | null = null;
  private readonly STORE_NAME = 'fishery_device';

  private constructor() {}

  /**
   * 获取单例
   */
  static getInstance(): StorageManager {
    if (!StorageManager.instance) {
      StorageManager.instance = new StorageManager();
    }
    return StorageManager.instance;
  }

  /**
   * 初始化存储
   */
  async init(context: Context): Promise<void> {
    try {
      this.preferences = await preferences.getPreferences(context, this.STORE_NAME);
      Logger.info('Storage initialized successfully');
    } catch (err) {
      Logger.error('Failed to init storage: %{public}s', JSON.stringify(err) || 'unknown error');
      Logger.error('Storage init error occurred');
    }
  }

  /**
   * 保存数据
   */
  async save(key: string, value: Object): Promise<void> {
    if (!this.preferences) {
      Logger.error('Storage not initialized');
      return;
    }
    try {
      const valueStr = typeof value === 'string' ? value as string : JSON.stringify(value);
      await this.preferences.put(key, valueStr);
      await this.preferences.flush();
      Logger.debug('Saved data: %{public}s', key);
    } catch (err) {
      Logger.error('Failed to save data: %{public}s', JSON.stringify(err) || 'unknown error');
      Logger.error('Save data error occurred');
    }
  }

  /**
   * 读取数据
   */
  async get(key: string, defaultValue?: Object): Promise<Object> {
    if (!this.preferences) {
      Logger.error('Storage not initialized');
      return defaultValue || '';
    }
    try {
      const value = await this.preferences.get(key, defaultValue || '');
      if (typeof value === 'string' && value.startsWith('{')) {
        return JSON.parse(value as string);
      }
      return value;
    } catch (err) {
      Logger.error('Failed to get data: %{public}s', JSON.stringify(err) || 'unknown error');
      return defaultValue || '';
    }
  }

  /**
   * 删除数据
   */
  async remove(key: string): Promise<void> {
    if (!this.preferences) {
      Logger.error('Storage not initialized');
      return;
    }
    try {
      await this.preferences.delete(key);
      await this.preferences.flush();
      Logger.debug('Removed data: %{public}s', key);
    } catch (err) {
      Logger.error('Failed to remove data: %{public}s', JSON.stringify(err) || 'unknown error');
      Logger.error('Remove data error occurred');
    }
  }

  /**
   * 清空所有数据
   */
  async clear(): Promise<void> {
    if (!this.preferences) {
      Logger.error('Storage not initialized');
      return;
    }
    try {
      await this.preferences.clear();
      await this.preferences.flush();
      Logger.info('Storage cleared');
    } catch (err) {
      Logger.error('Failed to clear storage: %{public}s', JSON.stringify(err) || 'unknown error');
      Logger.error('Clear storage error occurred');
    }
  }

  /**
   * 检查键是否存在
   */
  async has(key: string): Promise<boolean> {
    if (!this.preferences) {
      Logger.error('Storage not initialized');
      return false;
    }
    try {
      return await this.preferences.has(key);
    } catch (err) {
      Logger.error('Failed to check key: %{public}s', JSON.stringify(err) || 'unknown error');
      return false;
    }
  }
}
