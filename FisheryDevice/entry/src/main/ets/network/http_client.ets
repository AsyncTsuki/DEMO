import http from '@ohos.net.http';
import { Logger } from '../utils/logger';
import { ApiResponse } from '../common/types';

/**
 * HTTP客户端
 */
export class HttpClient {
  private baseUrl: string;
  private timeout: number;
  private retryTimes: number;

  constructor(baseUrl: string, timeout: number = 5000, retryTimes: number = 3) {
    this.baseUrl = baseUrl;
    this.timeout = timeout;
    this.retryTimes = retryTimes;
  }

  /**
   * GET请求
   */
  async get<T>(path: string, params?: Record<string, Object>): Promise<ApiResponse<T>> {
    const url = this.buildUrl(path, params);
    return this.request<T>('GET', url);
  }

  /**
   * POST请求
   */
  async post<T>(path: string, data?: Object): Promise<ApiResponse<T>> {
    const url = this.buildUrl(path);
    return this.request<T>('POST', url, data);
  }

  /**
   * PUT请求
   */
  async put<T>(path: string, data?: Object): Promise<ApiResponse<T>> {
    const url = this.buildUrl(path);
    return this.request<T>('PUT', url, data);
  }

  /**
   * PATCH请求
   */
  async patch<T>(path: string, data?: Object): Promise<ApiResponse<T>> {
    const url = this.buildUrl(path);
    return this.request<T>('PATCH', url, data);
  }

  /**
   * DELETE请求
   */
  async delete<T>(path: string): Promise<ApiResponse<T>> {
    const url = this.buildUrl(path);
    return this.request<T>('DELETE', url);
  }

  /**
   * 执行HTTP请求
   */
  private async request<T>(
    method: string,
    url: string,
    data?: Object,
    retryCount: number = 0
  ): Promise<ApiResponse<T>> {
    const httpRequest = http.createHttp();

    try {
      Logger.debug('HTTP %{public}s: %{public}s', method, url);
      
      const options: http.HttpRequestOptions = {
        method: method as http.RequestMethod,
        header: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        readTimeout: this.timeout,
        connectTimeout: this.timeout
      };

      // 添加请求体
      if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
        options.extraData = JSON.stringify(data);
      }

      const response = await httpRequest.request(url, options);
      
      // 解析响应
      const responseCode = response.responseCode;
      const responseBody = response.result;

      Logger.debug('HTTP Response: %{public}d', responseCode);

      if (responseCode >= 200 && responseCode < 300) {
        // 成功响应
        const result: Object = typeof responseBody === 'string' 
          ? JSON.parse(responseBody as string) 
          : responseBody;
        
        return result as ApiResponse<T>;
      } else {
        // HTTP错误
        Logger.error('HTTP Error: %{public}d', responseCode);
        return {
          success: false,
          message: `HTTP Error: ${responseCode}`,
          code: `${responseCode}`
        };
      }
    } catch (err) {
      Logger.error('HTTP Request failed: %{public}s', JSON.stringify(err) || 'unknown error');

      // 重试机制
      if (retryCount < this.retryTimes) {
        Logger.info('Retrying... (%{public}d/%{public}d)', retryCount + 1, this.retryTimes);
        await this.delay(1000 * (retryCount + 1)); // 指数退避
        return this.request<T>(method, url, data, retryCount + 1);
      }

      return {
        success: false,
        message: 'Network error',
        code: 'NETWORK_ERROR'
      };
    } finally {
      httpRequest.destroy();
    }
  }

  /**
   * 构建完整URL
   */
  private buildUrl(path: string, params?: Record<string, Object>): string {
    let url = this.baseUrl + path;

    if (params) {
      const queryString = Object.entries(params)
        .map((entry: [string, Object]) => {
          const key = entry[0];
          const value = entry[1];
          return `${encodeURIComponent(key)}=${encodeURIComponent(String(value))}`;
        })
        .join('&');
      
      if (queryString) {
        url += '?' + queryString;
      }
    }

    return url;
  }

  /**
   * 延迟函数
   */
  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * 更新基础URL
   */
  setBaseUrl(baseUrl: string): void {
    this.baseUrl = baseUrl;
  }

  /**
   * 更新超时时间
   */
  setTimeout(timeout: number): void {
    this.timeout = timeout;
  }

  /**
   * 更新重试次数
   */
  setRetryTimes(retryTimes: number): void {
    this.retryTimes = retryTimes;
  }
}
