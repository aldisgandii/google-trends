from flask import Blueprint, request, jsonify
from datetime import datetime
import random

trends_bp = Blueprint('trends', __name__)

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

def get_mock_trends_data():
    """Generate mock trending data for demo"""
    keywords = [
        'Indonesia', 'Jakarta', 'Bali', 'Surabaya', 'Bandung',
        'Yogyakarta', 'Medan', 'Semarang', 'Palembang', 'Makassar',
        'Depok', 'Tangerang', 'Bekasi', 'Bogor', 'Malang',
        'Denpasar', 'Batam', 'Pekanbaru', 'Banjarmasin', 'Manado'
    ]
    
    return [
        {
            'keyword': keyword,
            'interest': random.randint(20, 100),
            'max_interest': random.randint(50, 100),
            'color': get_random_color()
        }
        for keyword in keywords
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
        
        # Generate mock data
        trends_data = get_mock_trends_data()
        
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
        'message': 'Google Trends API is running (Mock Data)',
        'timestamp': datetime.now().isoformat()
    })

