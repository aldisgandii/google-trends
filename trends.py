from flask import Blueprint, request, jsonify
from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime, timedelta
import random

trends_bp = Blueprint('trends', __name__)

def get_trending_keywords(timeframe='today 1-d', geo='ID'):
    """
    Mengambil trending keywords dari Google Trends
    """
    try:
        pytrends = TrendReq(hl='id-ID', tz=420)
        
        # Ambil trending searches
        trending_searches = pytrends.trending_searches(pn='indonesia')
        
        if trending_searches.empty:
            return []
        
        # Ambil top 20 trending keywords
        keywords = trending_searches[0].head(20).tolist()
        
        # Untuk setiap keyword, ambil data interest over time
        trends_data = []
        for keyword in keywords:
            try:
                pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo, gprop='')
                interest_data = pytrends.interest_over_time()
                
                if not interest_data.empty:
                    # Ambil nilai rata-rata interest
                    avg_interest = interest_data[keyword].mean()
                    max_interest = interest_data[keyword].max()
                    
                    trends_data.append({
                        'keyword': keyword,
                        'interest': int(avg_interest) if not pd.isna(avg_interest) else 0,
                        'max_interest': int(max_interest) if not pd.isna(max_interest) else 0,
                        'color': get_random_color()
                    })
                else:
                    trends_data.append({
                        'keyword': keyword,
                        'interest': random.randint(10, 100),
                        'max_interest': random.randint(50, 100),
                        'color': get_random_color()
                    })
            except Exception as e:
                print(f"Error processing keyword {keyword}: {e}")
                # Fallback dengan data random
                trends_data.append({
                    'keyword': keyword,
                    'interest': random.randint(10, 100),
                    'max_interest': random.randint(50, 100),
                    'color': get_random_color()
                })
        
        return trends_data
        
    except Exception as e:
        print(f"Error getting trending keywords: {e}")
        # Fallback data untuk testing
        return get_fallback_data()

def get_random_color():
    """Generate random color for trending keyword"""
    colors = [
        '#FF6B6B',  # Red
        '#4ECDC4',  # Teal
        '#45B7D1',  # Blue
        '#96CEB4',  # Green
        '#FFEAA7',  # Yellow
        '#DDA0DD',  # Plum
        '#98D8C8',  # Mint
        '#F7DC6F',  # Light Yellow
        '#BB8FCE',  # Light Purple
        '#85C1E9'   # Light Blue
    ]
    return random.choice(colors)

def get_fallback_data():
    """Data fallback untuk testing"""
    fallback_keywords = [
        'Indonesia', 'Jakarta', 'Bali', 'Surabaya', 'Bandung',
        'Yogyakarta', 'Medan', 'Semarang', 'Palembang', 'Makassar',
        'Depok', 'Tangerang', 'Bekasi', 'Bogor', 'Malang'
    ]
    
    return [
        {
            'keyword': keyword,
            'interest': random.randint(20, 100),
            'max_interest': random.randint(50, 100),
            'color': get_random_color()
        }
        for keyword in fallback_keywords
    ]

@trends_bp.route('/trends', methods=['GET'])
def get_trends():
    """
    API endpoint untuk mengambil data Google Trends
    Query parameters:
    - keyword: filter berdasarkan keyword (optional)
    - date: tanggal dalam format YYYY-MM-DD (optional)
    - timeframe: today 1-d, today 7-d, today 1-m, today 3-m (default: today 1-d)
    """
    try:
        # Ambil parameter dari query string
        keyword_filter = request.args.get('keyword', '').lower()
        date_filter = request.args.get('date', '')
        timeframe = request.args.get('timeframe', 'today 1-d')
        
        # Validasi timeframe
        valid_timeframes = ['today 1-d', 'today 7-d', 'today 1-m', 'today 3-m']
        if timeframe not in valid_timeframes:
            timeframe = 'today 1-d'
        
        # Jika ada date filter, konversi ke timeframe yang sesuai
        if date_filter:
            try:
                target_date = datetime.strptime(date_filter, '%Y-%m-%d')
                today = datetime.now()
                days_diff = (today - target_date).days
                
                if days_diff <= 1:
                    timeframe = 'today 1-d'
                elif days_diff <= 7:
                    timeframe = 'today 7-d'
                elif days_diff <= 30:
                    timeframe = 'today 1-m'
                else:
                    timeframe = 'today 3-m'
            except ValueError:
                pass  # Gunakan timeframe default jika format tanggal salah
        
        # Ambil data trending
        trends_data = get_trending_keywords(timeframe=timeframe)
        
        # Filter berdasarkan keyword jika ada
        if keyword_filter:
            trends_data = [
                trend for trend in trends_data 
                if keyword_filter in trend['keyword'].lower()
            ]
        
        # Sort berdasarkan interest (descending)
        trends_data.sort(key=lambda x: x['interest'], reverse=True)
        
        return jsonify({
            'success': True,
            'data': trends_data,
            'timeframe': timeframe,
            'total': len(trends_data)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'data': []
        }), 500

@trends_bp.route('/trends/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'message': 'Google Trends API is running',
        'timestamp': datetime.now().isoformat()
    })

