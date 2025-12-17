"""
智能投喂算法模块

采用基于生物量的投喂模型，结合环境因子修正和多项式特征工程，
实现精准的投喂量计算。

算法核心:
1. 基础投喂量计算: F_base = W × r × t
2. 环境因子修正: F_adjusted = F_base × f(T) × f(DO) × f(pH)
3. 多项式特征展开: 引入二次项和交互项提高精度
4. 能量平衡优化: 考虑FCR和能量需求

"""

import numpy as np
from typing import Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class FishSpeciesParams:
    """鱼类品种参数"""
    name: str  # 品种名称
    optimal_temp: float  # 最适水温 (°C)
    temp_range: Tuple[float, float]  # 适宜温度范围
    optimal_do: float  # 最适溶解氧 (mg/L)
    min_do: float  # 最低溶解氧
    optimal_ph: Tuple[float, float]  # 最适pH范围
    base_feeding_rate: float  # 基础投喂率 (%)
    fcr: float  # 饲料转化率
    energy_requirement: float  # 能量需求 (kJ/kg体重/天)
    feed_energy_content: float  # 饲料能量含量 (kJ/kg)


# 预定义鱼类品种参数
FISH_SPECIES_PARAMS = {
    'yellow_croaker': FishSpeciesParams(
        name='大黄鱼',
        optimal_temp=22.0,
        temp_range=(16.0, 28.0),
        optimal_do=6.5,
        min_do=4.0,
        optimal_ph=(7.5, 8.5),
        base_feeding_rate=2.5,
        fcr=1.5,
        energy_requirement=100.0,
        feed_energy_content=1500.0
    ),
    'sea_bass': FishSpeciesParams(
        name='海鲈鱼',
        optimal_temp=25.0,
        temp_range=(18.0, 32.0),
        optimal_do=6.0,
        min_do=3.5,
        optimal_ph=(7.0, 8.5),
        base_feeding_rate=3.0,
        fcr=1.3,
        energy_requirement=120.0,
        feed_energy_content=1600.0
    ),
    'grouper': FishSpeciesParams(
        name='石斑鱼',
        optimal_temp=26.0,
        temp_range=(20.0, 30.0),
        optimal_do=5.5,
        min_do=4.0,
        optimal_ph=(7.5, 8.2),
        base_feeding_rate=2.0,
        fcr=1.6,
        energy_requirement=90.0,
        feed_energy_content=1400.0
    ),
    'tilapia': FishSpeciesParams(
        name='罗非鱼',
        optimal_temp=28.0,
        temp_range=(22.0, 35.0),
        optimal_do=5.0,
        min_do=3.0,
        optimal_ph=(6.5, 8.5),
        base_feeding_rate=4.0,
        fcr=1.2,
        energy_requirement=110.0,
        feed_energy_content=1450.0
    ),
    'default': FishSpeciesParams(
        name='通用鱼类',
        optimal_temp=24.0,
        temp_range=(18.0, 30.0),
        optimal_do=6.0,
        min_do=4.0,
        optimal_ph=(7.0, 8.5),
        base_feeding_rate=2.5,
        fcr=1.5,
        energy_requirement=100.0,
        feed_energy_content=1500.0
    )
}


class SmartFeedingAlgorithm:
    """智能投喂算法类"""
    
    def __init__(self):
        # 多项式系数 (通过历史数据拟合得到)
        self.poly_coefficients = {
            'temp': [1.0, -0.02, 0.001],  # 温度多项式系数
            'do': [0.5, 0.08, -0.005],    # 溶解氧多项式系数
            'ph': [0.2, 0.1, -0.01],      # pH多项式系数
            'interaction': {
                'temp_do': 0.015,          # 温度-溶解氧交互项
                'temp_ph': 0.008,          # 温度-pH交互项
                'do_ph': 0.012             # 溶解氧-pH交互项
            }
        }
    
    def get_species_params(self, fish_type: str) -> FishSpeciesParams:
        """获取鱼类品种参数"""
        return FISH_SPECIES_PARAMS.get(fish_type, FISH_SPECIES_PARAMS['default'])
    
    def calculate_temperature_factor(self, temp: float, params: FishSpeciesParams) -> float:
        """
        计算温度修正因子
        
        采用二次多项式模型，以最适温度为中心的高斯型分布
        f(T) = exp(-((T - T_opt)^2) / (2 * sigma^2))
        """
        t_opt = params.optimal_temp
        t_min, t_max = params.temp_range
        
        # 计算标准差（基于温度范围）
        sigma = (t_max - t_min) / 4
        
        # 高斯型温度响应函数
        factor = np.exp(-((temp - t_opt) ** 2) / (2 * sigma ** 2))
        
        # 添加边界惩罚
        if temp < t_min:
            penalty = 0.5 * ((t_min - temp) / t_min)
            factor = max(0.1, factor - penalty)
        elif temp > t_max:
            penalty = 0.5 * ((temp - t_max) / t_max)
            factor = max(0.1, factor - penalty)
        
        return np.clip(factor, 0.1, 1.0)
    
    def calculate_dissolved_oxygen_factor(self, do: float, params: FishSpeciesParams) -> float:
        """
        计算溶解氧修正因子
        
        采用Sigmoid型曲线，低于最低DO时急剧下降
        f(DO) = 1 / (1 + exp(-k * (DO - DO_crit)))
        """
        do_opt = params.optimal_do
        do_min = params.min_do
        
        # 临界点设为最低DO和最适DO的中点
        do_crit = (do_min + do_opt) / 2
        k = 2.0  # 曲线陡度
        
        # Sigmoid函数
        factor = 1.0 / (1.0 + np.exp(-k * (do - do_crit)))
        
        # 高于最适值时略微下调（过饱和可能有害）
        if do > do_opt * 1.5:
            factor *= 0.95
        
        # 极低溶解氧惩罚
        if do < do_min:
            factor *= max(0.1, do / do_min)
        
        return np.clip(factor, 0.1, 1.0)
    
    def calculate_ph_factor(self, ph: float, params: FishSpeciesParams) -> float:
        """
        计算pH修正因子
        
        采用梯形函数，在最适范围内为1，超出范围线性下降
        """
        ph_min, ph_max = params.optimal_ph
        
        if ph_min <= ph <= ph_max:
            return 1.0
        elif ph < ph_min:
            # 线性下降，每偏离0.5个pH单位下降20%
            deviation = ph_min - ph
            factor = max(0.2, 1.0 - 0.4 * deviation)
        else:
            deviation = ph - ph_max
            factor = max(0.2, 1.0 - 0.4 * deviation)
        
        return factor
    
    def calculate_interaction_terms(self, temp: float, do: float, ph: float,
                                   temp_factor: float, do_factor: float, ph_factor: float) -> float:
        """
        计算环境因子交互项
        
        使用多项式展开方法生成二次交互特征
        """
        coeffs = self.poly_coefficients['interaction']
        
        # 标准化环境参数
        temp_norm = (temp - 20) / 10
        do_norm = (do - 6) / 2
        ph_norm = (ph - 7.5) / 0.5
        
        # 计算交互项
        interaction = (
            coeffs['temp_do'] * temp_norm * do_norm +
            coeffs['temp_ph'] * temp_norm * ph_norm +
            coeffs['do_ph'] * do_norm * ph_norm
        )
        
        # 限制交互项影响范围
        return np.clip(1.0 + interaction, 0.8, 1.2)
    
    def calculate_polynomial_features(self, temp: float, do: float, ph: float) -> np.ndarray:
        """
        生成多项式特征向量
        
        包含一次项、二次项和交互项
        """
        # 标准化
        temp_norm = (temp - 24) / 6
        do_norm = (do - 6) / 2
        ph_norm = (ph - 7.5) / 0.5
        
        # 特征向量: [1, T, DO, pH, T^2, DO^2, pH^2, T*DO, T*pH, DO*pH]
        features = np.array([
            1.0,           # 截距项
            temp_norm,     # 温度
            do_norm,       # 溶解氧
            ph_norm,       # pH
            temp_norm ** 2,  # 温度二次项
            do_norm ** 2,    # 溶解氧二次项
            ph_norm ** 2,    # pH二次项
            temp_norm * do_norm,   # 温度-溶解氧交互
            temp_norm * ph_norm,   # 温度-pH交互
            do_norm * ph_norm      # 溶解氧-pH交互
        ])
        
        return features
    
    def calculate_energy_based_feeding(self, biomass: float, params: FishSpeciesParams,
                                       env_factor: float, time_interval: float = 1.0) -> float:
        """
        基于能量平衡的投喂量计算
        
        F = (W × E_req × t × env_factor) / (FCR × E_feed)
        """
        feeding_amount = (biomass * params.energy_requirement * time_interval * env_factor) / \
                        (params.fcr * params.feed_energy_content)
        
        return feeding_amount
    
    def calculate_feeding_amount(self, fish_count: int, average_weight: float,
                                 fish_type: str = 'default',
                                 temperature: float = 24.0,
                                 dissolved_oxygen: float = 6.0,
                                 ph: float = 7.5,
                                 time_interval: float = 1.0) -> Dict:
        """
        计算建议投喂量（主要接口）
        
        参数:
            fish_count: 鱼类数量
            average_weight: 平均体重 (kg)
            fish_type: 鱼类品种
            temperature: 当前水温 (°C)
            dissolved_oxygen: 当前溶解氧 (mg/L)
            ph: 当前pH值
            time_interval: 投喂间隔 (天)
        
        返回:
            包含投喂量、投喂类型和原因说明的字典
        """
        # 获取品种参数
        params = self.get_species_params(fish_type)
        
        # 计算总生物量
        biomass = fish_count * average_weight  # kg
        
        # 计算基础投喂量
        base_feeding = biomass * (params.base_feeding_rate / 100) * time_interval
        
        # 计算各环境因子
        temp_factor = self.calculate_temperature_factor(temperature, params)
        do_factor = self.calculate_dissolved_oxygen_factor(dissolved_oxygen, params)
        ph_factor = self.calculate_ph_factor(ph, params)
        
        # 计算交互项修正
        interaction_factor = self.calculate_interaction_terms(
            temperature, dissolved_oxygen, ph,
            temp_factor, do_factor, ph_factor
        )
        
        # 综合环境修正因子
        env_factor = temp_factor * do_factor * ph_factor * interaction_factor
        
        # 环境修正后的投喂量
        adjusted_feeding = base_feeding * env_factor
        
        # 基于能量平衡的投喂量
        energy_feeding = self.calculate_energy_based_feeding(
            biomass, params, env_factor, time_interval
        )
        
        # 综合两种方法（加权平均）
        final_feeding = 0.6 * adjusted_feeding + 0.4 * energy_feeding
        
        # 确定投喂类型和原因
        feeding_type, reason = self._determine_feeding_recommendation(
            env_factor, temp_factor, do_factor, ph_factor,
            temperature, dissolved_oxygen, ph, params
        )
        
        return {
            'amount': round(final_feeding, 2),
            'type': feeding_type,
            'reason': reason,
            'details': {
                'biomass': round(biomass, 2),
                'base_feeding': round(base_feeding, 2),
                'temp_factor': round(temp_factor, 3),
                'do_factor': round(do_factor, 3),
                'ph_factor': round(ph_factor, 3),
                'env_factor': round(env_factor, 3),
                'adjusted_feeding': round(adjusted_feeding, 2),
                'energy_feeding': round(energy_feeding, 2),
                'fish_species': params.name
            }
        }
    
    def _determine_feeding_recommendation(self, env_factor: float,
                                         temp_factor: float, do_factor: float, ph_factor: float,
                                         temp: float, do: float, ph: float,
                                         params: FishSpeciesParams) -> Tuple[str, str]:
        """确定投喂推荐类型和原因"""
        
        reasons = []
        
        # 分析温度
        if temp_factor < 0.7:
            if temp < params.optimal_temp:
                reasons.append(f'水温偏低({temp}°C)，低于最适温度{params.optimal_temp}°C')
            else:
                reasons.append(f'水温偏高({temp}°C)，高于最适温度{params.optimal_temp}°C')
        
        # 分析溶解氧
        if do_factor < 0.7:
            reasons.append(f'溶解氧不足({do}mg/L)，建议值>{params.optimal_do}mg/L')
        
        # 分析pH
        if ph_factor < 0.8:
            ph_min, ph_max = params.optimal_ph
            reasons.append(f'pH值({ph})偏离最适范围{ph_min}-{ph_max}')
        
        # 确定投喂类型
        if env_factor >= 0.85:
            feeding_type = '正常投喂'
            if not reasons:
                reasons.append('环境条件良好，可正常投喂')
        elif env_factor >= 0.6:
            feeding_type = '减量投喂'
            if not reasons:
                reasons.append('环境条件一般，建议适当减少投喂量')
        else:
            feeding_type = '暂停投喂'
            if not reasons:
                reasons.append('环境条件较差，建议暂停投喂并检查水质')
        
        return feeding_type, '；'.join(reasons)


# 创建全局算法实例
feeding_algorithm = SmartFeedingAlgorithm()


def calculate_feeding(fish_count: int, average_weight: float,
                     fish_type: str = 'default',
                     env_data: Optional[Dict] = None) -> Dict:
    """
    便捷接口：计算建议投喂量
    """
    if env_data is None:
        env_data = {}
    
    return feeding_algorithm.calculate_feeding_amount(
        fish_count=fish_count,
        average_weight=average_weight,
        fish_type=fish_type,
        temperature=env_data.get('temperature', 24.0),
        dissolved_oxygen=env_data.get('dissolvedOxygen', 6.0),
        ph=env_data.get('ph', 7.5)
    )
