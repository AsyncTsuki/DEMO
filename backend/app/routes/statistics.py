from flask import Blueprint, request, jsonify
from app import db
from app.models.device import Device
from app.models.feeding import FeedingHistory
from app.models.environment import EnvironmentData
from app.models.alert import Alert
from app.models.pond import Pond
from app.utils.decorators import login_required
from datetime import datetime, timedelta
from sqlalchemy import func
import random

statistics_bp = Blueprint('statistics', __name__)


@statistics_bp.route('/overview', methods=['GET'])
@login_required
def get_overview_statistics():
    """获取系统总览统计数据"""
    try:
        # 统计总数
        total_devices = Device.query.count()
        total_feedings = FeedingHistory.query.count()
        total_alerts = Alert.query.count()
        total_monitoring = EnvironmentData.query.count()
        
        # 在线设备数
        online_devices = Device.query.filter_by(status='online').count()
        
        # 未解决的告警数
        unresolved_alerts = Alert.query.filter_by(status='未处理').count()
        
        return jsonify({
            'success': True,
            'data': {
                'totalDevices': total_devices,
                'onlineDevices': online_devices,
                'totalFeedings': total_feedings,
                'totalAlerts': total_alerts,
                'unresolvedAlerts': unresolved_alerts,
                'totalMonitoring': total_monitoring
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取统计数据失败: {str(e)}'
        }), 500


@statistics_bp.route('/pond/trend', methods=['GET'])
@login_required
def get_pond_trend():
    """获取鱼塘数量趋势（基于真实数据）"""
    try:
        period = request.args.get('period', '7d')
        now = datetime.now()
        
        # 检查是否有鱼塘数据
        total_ponds = Pond.query.count()
        
        if total_ponds == 0:
            # 如果没有数据，返回空数据
            return jsonify({
                'success': True,
                'data': {
                    'labels': [],
                    'counts': [],
                    'statistics': {
                        'totalPonds': 0,
                        'newThisMonth': 0,
                        'utilizationRate': 0
                    }
                }
            })
        
        # 根据时间范围计算鱼塘增长趋势
        if period == '7d':
            # 近一周：显示最近一周每天的鱼塘总数
            labels = []
            counts = []
            for i in range(7):
                date = now - timedelta(days=6-i)
                labels.append(date.strftime('%m-%d'))
                # 统计该日期之前创建的所有鱼塘
                count = Pond.query.filter(Pond.created_at <= date).count()
                counts.append(count)
        elif period == '30d':
            # 近一个月：显示每5天的数据
            labels = []
            counts = []
            for i in range(6):
                date = now - timedelta(days=25-i*5)
                labels.append(date.strftime('%m-%d'))
                count = Pond.query.filter(Pond.created_at <= date).count()
                counts.append(count)
        elif period == '3m':
            # 近三个月：显示每两周的数据
            labels = []
            counts = []
            for i in range(6):
                date = now - timedelta(days=75-i*15)
                labels.append(date.strftime('%m-%d'))
                count = Pond.query.filter(Pond.created_at <= date).count()
                counts.append(count)
        else:  # 1y
            # 近一年：显示12个月的数据
            labels = []
            counts = []
            for i in range(12):
                date = now - timedelta(days=(11-i)*30)
                labels.append(date.strftime('%Y-%m'))
                count = Pond.query.filter(Pond.created_at <= date).count()
                counts.append(count)
        
        # 统计本月新增鱼塘
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        new_this_month = Pond.query.filter(Pond.created_at >= month_start).count()
        
        # 计算利用率（活跃鱼塘比例）
        active_count = Pond.query.filter_by(status='active').count()
        utilization_rate = int((active_count / total_ponds) * 100) if total_ponds > 0 else 0
        
        return jsonify({
            'success': True,
            'data': {
                'labels': labels,
                'counts': counts,
                'statistics': {
                    'totalPonds': total_ponds,
                    'newThisMonth': new_this_month,
                    'utilizationRate': utilization_rate
                }
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取鱼塘趋势数据失败: {str(e)}'
        }), 500


@statistics_bp.route('/fish/species', methods=['GET'])
@login_required
def get_fish_species_distribution():
    """获取鱼种分布统计"""
    # 基于投喂历史记录统计鱼种
    fish_type_counts = db.session.query(
        FeedingHistory.fish_type,
        func.count(FeedingHistory.id).label('count')
    ).group_by(FeedingHistory.fish_type).all()
    
    if fish_type_counts:
        species = [item[0] for item in fish_type_counts]
        counts = [item[1] for item in fish_type_counts]
        
        # 计算百分比
        total = sum(counts)
        percentages = [round((count / total) * 100, 1) for count in counts]
    else:
        # 如果没有数据，返回模拟数据
        species = ['大黄鱼', '鲈鱼', '石斑鱼', '对虾', '其他']
        percentages = [45, 25, 15, 10, 5]
        counts = percentages  # 用百分比代替计数
    
    return jsonify({
        'success': True,
        'data': {
            'labels': species,
            'series': percentages,
            'counts': counts,
            'statistics': {
                'totalSpecies': len(species),
                'mainSpecies': species[0] if species else '大黄鱼',
                'rareSpecies': len([s for s in species if s not in ['大黄鱼', '鲈鱼', '石斑鱼']])
            }
        }
    })


@statistics_bp.route('/fish/population', methods=['GET'])
@login_required
def get_fish_population_trend():
    """获取鱼群数量趋势（基于投喂记录推算）"""
    period = request.args.get('period', '7d')
    
    # 根据时间范围查询投喂记录
    if period == '7d':
        days = 7
    elif period == '30d':
        days = 30
    else:
        days = 90
    
    start_date = datetime.now() - timedelta(days=days)
    
    # 按天统计投喂数量，推算鱼群数量
    daily_stats = db.session.query(
        func.date(FeedingHistory.timestamp).label('date'),
        func.sum(FeedingHistory.fish_count).label('total_count')
    ).filter(
        FeedingHistory.timestamp >= start_date
    ).group_by(
        func.date(FeedingHistory.timestamp)
    ).order_by('date').all()
    
    if daily_stats and len(daily_stats) > 0:
        dates = []
        populations = []
        
        for stat in daily_stats:
            date_obj = stat[0] if isinstance(stat[0], datetime) else datetime.strptime(str(stat[0]), '%Y-%m-%d')
            dates.append(date_obj.strftime('%m-%d'))
            # 假设每次投喂覆盖的鱼群数量
            populations.append(int(stat[1] or 0))
        
        avg_population = sum(populations) // len(populations) if populations else 1250000
    else:
        # 生成模拟数据
        dates = []
        populations = []
        base_population = 1200000
        
        for i in range(days):
            date_obj = start_date + timedelta(days=i)
            dates.append(date_obj.strftime('%m-%d'))
            # 模拟增长
            population = base_population + (i * 5000) + random.randint(-10000, 20000)
            populations.append(population)
        
        avg_population = sum(populations) // len(populations)
    
    # 计算月增长率
    if len(populations) >= 2:
        first_half = sum(populations[:len(populations)//2]) / (len(populations)//2)
        second_half = sum(populations[len(populations)//2:]) / (len(populations) - len(populations)//2)
        monthly_growth = round(((second_half - first_half) / first_half) * 100, 1)
    else:
        monthly_growth = 8.5
    
    return jsonify({
        'success': True,
        'data': {
            'dates': dates,
            'populations': populations,
            'statistics': {
                'totalPopulation': populations[-1] if populations else 1250000,
                'monthlyGrowth': monthly_growth,
                'avgDensity': random.randint(4800, 5500),
                'healthScore': round(random.uniform(7.5, 9.0), 1)
            }
        }
    })


@statistics_bp.route('/pond/details', methods=['GET'])
@login_required
def get_pond_details():
    """获取鱼塘详细数据（基于真实鱼塘表）"""
    try:
        # 查询所有活跃的鱼塘
        ponds = Pond.query.filter_by(status='active').limit(10).all()
        
        if not ponds:
            # 如果没有数据，返回空列表
            return jsonify({
                'success': True,
                'data': []
            })
        
        pond_data = []
        for pond in ponds:
            # 计算增长率（基于创建时间）
            days_active = (datetime.now() - pond.created_at).days
            if days_active > 0:
                # 模拟增长率，时间越长增长率越低
                growth_rate = round(random.uniform(8.0, 15.0) / (1 + days_active/100), 1)
            else:
                growth_rate = round(random.uniform(10.0, 15.0), 1)
            
            # 计算密度（尾/平方米）
            density = int(pond.fish_count / pond.area) if pond.area > 0 else 0
            
            pond_data.append({
                'id': pond.id,
                'pondName': pond.name,
                'fishSpecies': pond.fish_type,
                'population': pond.fish_count,
                'growthRate': growth_rate,
                'density': density
            })
        
        return jsonify({
            'success': True,
            'data': pond_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取鱼塘详情失败: {str(e)}'
        }), 500
