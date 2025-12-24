import { DeviceManager } from '../service/device_manager';
import { Logger } from '../utils/logger';

/**
 * 主页面
 */
@Entry
@Component
struct Index {
  @State deviceStatus: string = '初始化中...';
  @State temperature: number = 0;
  @State dissolvedOxygen: number = 0;
  @State ph: number = 0;
  @State waterFlow: number = 0;
  @State feederCapacity: number = 0;
  @State feedAmount: string = '1.0';

  private deviceManager: DeviceManager | null = null;
  private updateTimer: number = -1;

  aboutToAppear() {
    Logger.info('Index page aboutToAppear');
    
    // 延迟获取设备管理器实例，确保 EntryAbility 已初始化
    setTimeout(() => {
      this.deviceManager = DeviceManager.getInstance();
      if (this.deviceManager) {
        Logger.info('Device Manager instance obtained');
        // 启动数据更新定时器
        this.startUpdateTimer();
      } else {
        Logger.error('Failed to get Device Manager instance');
      }
    }, 1000);
  }

  aboutToDisappear() {
    Logger.info('Index page aboutToDisappear');
    
    // 清除定时器
    if (this.updateTimer !== -1) {
      clearInterval(this.updateTimer);
      this.updateTimer = -1;
    }
  }

  /**
   * 启动数据更新定时器
   */
  private startUpdateTimer(): void {
    this.updateTimer = setInterval(() => {
      this.updateData();
    }, 2000);  // 每2秒更新一次界面
  }

  /**
   * 更新界面数据
   */
  private updateData(): void {
    if (!this.deviceManager) {
      return;
    }

    try {
      // 获取当前环境数据
      const envData = this.deviceManager.getCurrentEnvironmentData();
      this.temperature = envData.temperature;
      this.dissolvedOxygen = envData.dissolvedOxygen;
      this.ph = envData.ph;
      this.waterFlow = envData.waterFlow;

      // 获取设备状态
      const status = this.deviceManager.getDeviceStatus();
      this.deviceStatus = status.status === 'online' ? '在线' : '离线';
      this.feederCapacity = status.feederStatus.capacity;
    } catch (err) {
      Logger.error('Failed to update data: %{public}s', JSON.stringify(err) || 'unknown error');
    }
  }

  /**
   * 执行投喂
   */
  private async executeFeed(): Promise<void> {
    if (!this.deviceManager) {
      return;
    }

    try {
      const amount = parseFloat(this.feedAmount);
      if (isNaN(amount) || amount <= 0) {
        Logger.error('Invalid feed amount');
        return;
      }

      Logger.info('Executing feed: %{public}f kg', amount);
      await this.deviceManager.executeFeed(amount);
    } catch (err) {
      Logger.error('Failed to execute feed: %{public}s', JSON.stringify(err) || 'unknown error');
    }
  }

  build() {
    Column() {
      // 标题
      Text('海洋渔业智能投喂系统')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .margin({ top: 20, bottom: 10 })

      // 设备状态
      Text(`设备状态: ${this.deviceStatus}`)
        .fontSize(16)
        .margin({ bottom: 20 })

      // 环境数据卡片
      Column() {
        Text('环境数据')
          .fontSize(20)
          .fontWeight(FontWeight.Medium)
          .margin({ bottom: 10 })

        Row() {
          Column() {
            Text('水温')
              .fontSize(14)
              .fontColor('#666666')
            Text(`${this.temperature.toFixed(1)}°C`)
              .fontSize(18)
              .fontWeight(FontWeight.Bold)
              .margin({ top: 5 })
          }
          .layoutWeight(1)

          Column() {
            Text('溶解氧')
              .fontSize(14)
              .fontColor('#666666')
            Text(`${this.dissolvedOxygen.toFixed(1)} mg/L`)
              .fontSize(18)
              .fontWeight(FontWeight.Bold)
              .margin({ top: 5 })
          }
          .layoutWeight(1)
        }
        .width('100%')
        .margin({ bottom: 15 })

        Row() {
          Column() {
            Text('pH值')
              .fontSize(14)
              .fontColor('#666666')
            Text(`${this.ph.toFixed(1)}`)
              .fontSize(18)
              .fontWeight(FontWeight.Bold)
              .margin({ top: 5 })
          }
          .layoutWeight(1)

          Column() {
            Text('水流量')
              .fontSize(14)
              .fontColor('#666666')
            Text(`${this.waterFlow.toFixed(1)} m³/s`)
              .fontSize(18)
              .fontWeight(FontWeight.Bold)
              .margin({ top: 5 })
          }
          .layoutWeight(1)
        }
        .width('100%')
      }
      .width('90%')
      .padding(20)
      .backgroundColor('#F5F5F5')
      .borderRadius(10)
      .margin({ bottom: 20 })

      // 投喂控制卡片
      Column() {
        Text('投喂控制')
          .fontSize(20)
          .fontWeight(FontWeight.Medium)
          .margin({ bottom: 10 })

        Text(`剩余饲料: ${this.feederCapacity.toFixed(1)} kg`)
          .fontSize(16)
          .margin({ bottom: 15 })

        Row() {
          Text('投喂量(kg):')
            .fontSize(16)
            .layoutWeight(1)

          TextInput({ text: this.feedAmount })
            .width(120)
            .type(InputType.Number)
            .onChange((value: string) => {
              this.feedAmount = value;
            })
        }
        .width('100%')
        .margin({ bottom: 15 })

        Button('执行投喂')
          .width('100%')
          .onClick(() => {
            this.executeFeed();
          })
      }
      .width('90%')
      .padding(20)
      .backgroundColor('#F5F5F5')
      .borderRadius(10)
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#FFFFFF')
  }
}
