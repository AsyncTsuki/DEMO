import { Logger } from '../utils/logger';

/**
 * 传感器基类
 */
export abstract class BaseSensor {
  protected enabled: boolean = true;
  protected minValue: number = 0;
  protected maxValue: number = 100;
  protected currentValue: number = 0;
  protected baseValue: number = 50;

  constructor(min: number, max: number) {
    this.minValue = min;
    this.maxValue = max;
    this.baseValue = (min + max) / 2;
    this.currentValue = this.baseValue;
  }

  /**
   * 启用传感器
   */
  enable(): void {
    this.enabled = true;
    Logger.info('%{public}s enabled', this.constructor.name);
  }

  /**
   * 禁用传感器
   */
  disable(): void {
    this.enabled = false;
    Logger.info('%{public}s disabled', this.constructor.name);
  }

  /**
   * 读取传感器数据
   * 使用正弦波 + 随机噪声模拟真实传感器
   */
  read(): number {
    if (!this.enabled) {
      return 0;
    }

    // 正弦波模拟周期性变化
    const time = Date.now() / 1000;
    const period = 300; // 5分钟周期
    const amplitude = (this.maxValue - this.minValue) * 0.15; // 振幅为范围的15%
    const sine = Math.sin(2 * Math.PI * time / period) * amplitude;

    // 随机噪声
    const noise = (Math.random() - 0.5) * (this.maxValue - this.minValue) * 0.05;

    // 计算当前值
    this.currentValue = this.baseValue + sine + noise;

    // 限制在范围内
    this.currentValue = Math.max(this.minValue, Math.min(this.maxValue, this.currentValue));

    return parseFloat(this.currentValue.toFixed(2));
  }

  /**
   * 设置基准值
   */
  setBaseValue(value: number): void {
    this.baseValue = Math.max(this.minValue, Math.min(this.maxValue, value));
  }

  /**
   * 获取传感器状态
   */
  getStatus(): boolean {
    return this.enabled;
  }
}

/**
 * 水温传感器
 * 范围: 18-32°C
 */
export class TemperatureSensor extends BaseSensor {
  constructor(min: number = 18.0, max: number = 32.0) {
    super(min, max);
    this.baseValue = 25.0; // 默认25°C
  }

  /**
   * 读取水温
   */
  readTemperature(): number {
    const temp = this.read();
    Logger.debug(`Temperature: ${temp} °C`);
    return temp;
  }
}

/**
 * 溶解氧传感器
 * 范围: 3-12 mg/L
 */
export class OxygenSensor extends BaseSensor {
  constructor(min: number = 3.0, max: number = 12.0) {
    super(min, max);
    this.baseValue = 7.0; // 默认7.0 mg/L
  }

  /**
   * 读取溶解氧
   */
  readOxygen(): number {
    const oxygen = this.read();
    Logger.debug(`Dissolved Oxygen: ${oxygen} mg/L`);
    return oxygen;
  }
}

/**
 * pH传感器
 * 范围: 6.5-8.5
 */
export class PhSensor extends BaseSensor {
  constructor(min: number = 6.5, max: number = 8.5) {
    super(min, max);
    this.baseValue = 7.5; // 默认7.5
  }

  /**
   * 读取pH值
   */
  readPh(): number {
    const ph = this.read();
    Logger.debug(`pH: ${ph}`);
    return ph;
  }
}

/**
 * 水流传感器
 * 范围: 0.5-5.0 m³/s
 */
export class WaterFlowSensor extends BaseSensor {
  constructor(min: number = 0.5, max: number = 5.0) {
    super(min, max);
    this.baseValue = 2.0; // 默认2.0 m³/s
  }

  /**
   * 读取水流量
   */
  readFlow(): number {
    const flow = this.read();
    Logger.debug(`Water Flow: ${flow} m³/s`);
    return flow;
  }
}
