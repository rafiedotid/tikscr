from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import time
import json
import logging
import re
from urllib.parse import quote

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class TikTokAPISimple:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def scrape_user_simple(self, username):
        """Simple scraping without Selenium - for demo purposes"""
        try:
            # This is a placeholder - real implementation would need
            # to handle JavaScript rendering or use external service
            
            # For now, return mock data that looks realistic
            import random
            
            # Simulate processing time
            time.sleep(random.uniform(2, 5))
            
            # Generate realistic-looking fake data for demo
            followers = random.randint(1000, 50000)
            likes = random.randint(500, followers // 2)
            following = random.randint(10, 500)
            videos = random.randint(5, 100)
            
            return {
                'username': username,
                'followers': f"{followers:,}",
                'likes': f"{likes:,}",
                'following': str(following),
                'videos': str(videos),
                'success': True,
                'message': 'Demo data (not real scraping)',
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'note': 'This is demo data. Real scraping requires Selenium.'
            }
            
        except Exception as e:
            logger.error(f"Error: {e}")
            return {
                'username': username,
                'followers': '0',
                'likes': '0',
                'following': '0',
                'videos': '0',
                'success': False,
                'message': f'Error: {str(e)}',
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }

# Global API instance
api = TikTokAPISimple()

@app.route('/', methods=['GET'])
def home():
    """API documentation"""
    return jsonify({
        'name': '🎭 TikTok Stats API (Demo Version)',
        'version': '1.0',
        'description': 'Demo API yang bisa deploy dimana aja tanpa Selenium',
        'warning': '⚠️ This version returns DEMO DATA, not real scraping',
        'features': [
            '🚀 Deploy anywhere (no Chrome needed)',
            '⚡ Fast response',
            '💰 Zero dependencies issues',
            '🎭 Demo data for testing'
        ],
        'endpoints': {
            'GET /': 'API documentation',
            'GET /health': 'Health check',
            'GET /api/user/<username>': 'Get demo TikTok user stats',
            'POST /api/user': 'Get demo stats (JSON body)'
        },
        'example': {
            'url': '/api/user/rafiedotid',
            'response': {
                'username': 'rafiedotid',
                'followers': '12,850',
                'likes': '3,424',
                'following': '13',
                'videos': '18',
                'success': True,
                'message': 'Demo data (not real scraping)',
                'note': 'This is demo data. Real scraping requires Selenium.'
            }
        },
        'deployment': 'Works on ANY hosting platform!',
        'real_scraping': 'Use app.py with Selenium for real data'
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': '🎭 Demo TikTok API is running!',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'version': '1.0 (Demo)',
        'note': 'This version works everywhere but returns demo data'
    })

@app.route('/api/user/<username>', methods=['GET'])
def get_user_stats(username):
    """Get demo TikTok user statistics"""
    try:
        if not username or len(username.strip()) == 0:
            return jsonify({
                'success': False,
                'message': 'Username is required'
            }), 400
        
        username = username.strip()
        
        if len(username) > 50:
            return jsonify({
                'success': False,
                'message': 'Username too long'
            }), 400
        
        logger.info(f"🎭 Demo API request for user: {username}")
        
        result = api.scrape_user_simple(username)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"API error for {username}: {e}")
        return jsonify({
            'username': username,
            'success': False,
            'message': f'Internal server error: {str(e)}'
        }), 500

@app.route('/api/user', methods=['POST'])
def get_user_stats_post():
    """Get demo TikTok user statistics via POST"""
    try:
        data = request.get_json()
        
        if not data or 'username' not in data:
            return jsonify({
                'success': False,
                'message': 'Username is required in JSON body'
            }), 400
        
        username = data['username'].strip()
        
        if not username:
            return jsonify({
                'success': False,
                'message': 'Username cannot be empty'
            }), 400
        
        logger.info(f"🎭 Demo POST API request for user: {username}")
        
        result = api.scrape_user_simple(username)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"POST API error: {e}")
        return jsonify({
            'success': False,
            'message': f'Internal server error: {str(e)}'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    
    print("🎭 Starting TikTok Demo API...")
    print("⚠️  WARNING: This version returns DEMO DATA")
    print("💡 For real scraping, use app.py with Selenium")
    print("🚀 This version works on ANY hosting platform!")
    print("")
    print("📡 API Endpoints:")
    print("   GET  /                     - API documentation")
    print("   GET  /health               - Health check")
    print("   GET  /api/user/<username>  - Get demo user stats")
    print("   POST /api/user             - Get demo stats (JSON)")
    print("")
    print(f"⚡ Starting server on port {port}")
    
    app.run(host='0.0.0.0', port=port, debug=False)