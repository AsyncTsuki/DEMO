import hilog from '@ohos.hilog';

/**
 * 日志级别
 */
export enum LogLevel {
  DEBUG = 3,
  INFO = 4,
  WARN = 5,
  ERROR = 6
}

/**
 * 日志工具类
 */
export class Logger {
  private static readonly DOMAIN = 0xFF00;
  private static readonly TAG = 'Fishery';

  /**
   * 调试日志
   */
  static debug(message: string, ...args: Object[]): void {
    hilog.debug(Logger.DOMAIN, Logger.TAG, message, ...args);
  }

  /**
   * 信息日志
   */
  static info(message: string, ...args: Object[]): void {
    hilog.info(Logger.DOMAIN, Logger.TAG, message, ...args);
  }

  /**
   * 警告日志
   */
  static warn(message: string, ...args: Object[]): void {
    hilog.warn(Logger.DOMAIN, Logger.TAG, message, ...args);
  }

  /**
   * 错误日志
   */
  static error(message: string, ...args: Object[]): void {
    hilog.error(Logger.DOMAIN, Logger.TAG, message, ...args);
  }

  /**
   * 带标签的日志
   */
  static logWithTag(tag: string, level: LogLevel, message: string, ...args: Object[]): void {
    switch (level) {
      case LogLevel.DEBUG:
        hilog.debug(Logger.DOMAIN, `${Logger.TAG}:${tag}`, message, ...args);
        break;
      case LogLevel.INFO:
        hilog.info(Logger.DOMAIN, `${Logger.TAG}:${tag}`, message, ...args);
        break;
      case LogLevel.WARN:
        hilog.warn(Logger.DOMAIN, `${Logger.TAG}:${tag}`, message, ...args);
        break;
      case LogLevel.ERROR:
        hilog.error(Logger.DOMAIN, `${Logger.TAG}:${tag}`, message, ...args);
        break;
    }
  }
}
