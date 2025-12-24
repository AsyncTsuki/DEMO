import { Logger } from '../utils/logger';
import { FeedingRecord } from '../common/types';

/**
 * 投喂器状态
 */
export enum FeederStatus {
  IDLE = 'idle',           // 空闲
  FEEDING = 'feeding',     // 投喂中
  ERROR = 'error'          // 故障
}

/**
 * 投喂器状态响应
 */
export interface FeederStatusResponse {
  status: FeederStatus;
  remaining: number;
  capacity: number;
}

/**
 * 投喂器控制类
 */
export class FeederController {
  private enabled: boolean = true;
  private status: FeederStatus = FeederStatus.IDLE;
  private capacity: number = 100.0;      // 饲料容量(kg)
  private remaining: number = 100.0;     // 剩余饲料(kg)
  private minAmount: number = 0.1;       // 最小投喂量(kg)
  private maxAmount: number = 10.0;      // 最大投喂量(kg)
  private speed: number = 0.5;           // 投喂速度(kg/s)

  constructor(capacity: number, minAmount: number, maxAmount: number, speed: number) {
    this.capacity = capacity;
    this.remaining = capacity;
    this.minAmount = minAmount;
    this.maxAmount = maxAmount;
    this.speed = speed;
  }

  /**
   * 执行投喂
   */
  async feed(amount: number): Promise<FeedingRecord> {
    const startTime = Date.now();
    Logger.info('Starting feeding: %{public}f kg', amount);

    // 检查投喂器状态
    if (!this.enabled) {
      Logger.error('Feeder is disabled');
      return this.createRecord(amount, 'failed', 0);
    }

    if (this.status === FeederStatus.FEEDING) {
      Logger.error('Feeder is busy');
      return this.createRecord(amount, 'failed', 0);
    }

    // 验证投喂量
    if (amount < this.minAmount || amount > this.maxAmount) {
      Logger.error('Invalid feeding amount: %{public}f kg', amount);
      return this.createRecord(amount, 'failed', 0);
    }

    // 检查饲料余量
    if (amount > this.remaining) {
      Logger.error('Insufficient feed: remaining %{public}f kg', this.remaining);
      return this.createRecord(amount, 'failed', 0);
    }

    try {
      // 设置为投喂中状态
      this.status = FeederStatus.FEEDING;

      // 模拟投喂过程(根据投喂速度计算时间)
      const feedingTime = (amount / this.speed) * 1000; // 转换为毫秒
      await this.delay(feedingTime);

      // 模拟投喂成功/失败(95%成功率)
      const success = Math.random() > 0.05;

      if (success) {
        this.remaining -= amount;
        Logger.info('Feeding completed: %{public}f kg, remaining: %{public}f kg', 
                   amount, this.remaining);
        
        // 检查是否需要补充饲料
        if (this.remaining < this.capacity * 0.2) {
          Logger.warn('Low feed level: %{public}f kg', this.remaining);
        }

        this.status = FeederStatus.IDLE;
        return this.createRecord(amount, 'success', Date.now() - startTime);
      } else {
        Logger.error('Feeding failed due to mechanical error');
        this.status = FeederStatus.ERROR;
        return this.createRecord(amount, 'failed', Date.now() - startTime);
      }
    } catch (err) {
      Logger.error('Feeding exception: %{public}s', JSON.stringify(err) || 'unknown error');
      this.status = FeederStatus.ERROR;
      return this.createRecord(amount, 'failed', Date.now() - startTime);
    }
  }

  /**
   * 补充饲料
   */
  refill(amount: number): void {
    const newRemaining = this.remaining + amount;
    this.remaining = Math.min(newRemaining, this.capacity);
    Logger.info('Feed refilled: %{public}f kg, remaining: %{public}f kg', 
               amount, this.remaining);
    
    // 如果之前是故障状态,补充饲料后恢复
    if (this.status === FeederStatus.ERROR) {
      this.status = FeederStatus.IDLE;
    }
  }

  /**
   * 获取投喂器状态
   */
  getStatus(): FeederStatusResponse {
    return {
      status: this.status,
      remaining: this.remaining,
      capacity: this.capacity
    };
  }

  /**
   * 启用投喂器
   */
  enable(): void {
    this.enabled = true;
    if (this.status === FeederStatus.ERROR) {
      this.status = FeederStatus.IDLE;
    }
    Logger.info('Feeder enabled');
  }

  /**
   * 禁用投喂器
   */
  disable(): void {
    this.enabled = false;
    Logger.info('Feeder disabled');
  }

  /**
   * 重置故障状态
   */
  reset(): void {
    if (this.status === FeederStatus.ERROR) {
      this.status = FeederStatus.IDLE;
      Logger.info('Feeder reset from error state');
    }
  }

  /**
   * 创建投喂记录
   */
  private createRecord(amount: number, status: string, duration: number): FeedingRecord {
    return {
      deviceId: '',  // 将由上层填充
      amount: amount,
      type: 'auto',
      operator: 'system',
      time: Date.now(),
      status: status
    };
  }

  /**
   * 延迟函数
   */
  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
