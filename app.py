# Rename dari tiktok_api_local.py untuk deployment
# File ini siap deploy ke Heroku/Railway/Render GRATIS!

from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import json
import logging
import os
import sys

# Import our working scraper
# Import scraper optimized for Railway
from tokcount_scraper_railway import TokCountScraperRailway as TokCountFixedDigits

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class TikTokAPIFree:
    def __init__(self):
        self.scraper = None
        self.last_used = 0
        self.max_idle_time = 300  # 5 minutes
    
    def get_scraper(self):
        """Get or create scraper instance"""
        current_time = time.time()
        
        # Create new scraper if needed
        if self.scraper is None:
            logger.info("🔧 Creating new scraper instance...")
            # Always headless for cloud deployment
            self.scraper = TokCountFixedDigits(headless=True)
            
        self.last_used = current_time
        return self.scraper
    
    def cleanup_scraper(self):
        """Cleanup scraper if idle too long"""
        if self.scraper and (time.time() - self.last_used) > self.max_idle_time:
            logger.info("🧹 Cleaning up idle scraper...")
            try:
                self.scraper.close_driver()
            except:
                pass
            self.scraper = None
    
    def scrape_user(self, username):
        """Scrape user data"""
        try:
            scraper = self.get_scraper()
            result = scraper.scrape_user_data(username)
            
            if result:
                return {
                    'username': result.get('username', username),
                    'followers': result.get('followers', '0'),
                    'likes': result.get('likes', '0'),
                    'following': result.get('following', '0'),
                    'videos': result.get('videos', '0'),
                    'success': True,
                    'message': 'Data scraped successfully',
                    'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'platform': 'Free Cloud Deployment'
                }
            else:
                return {
                    'username': username,
                    'followers': '0',
                    'likes': '0',
                    'following': '0',
                    'videos': '0',
                    'success': False,
                    'message': 'Failed to scrape data',
                    'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'platform': 'Free Cloud Deployment'
                }
                
        except Exception as e:
            logger.error(f"Error scraping {username}: {e}")
            return {
                'username': username,
                'followers': '0',
                'likes': '0',
                'following': '0',
                'videos': '0',
                'success': False,
                'message': f'Scraping error: {str(e)}',
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'platform': 'Free Cloud Deployment'
            }

# Global API instance
api = TikTokAPIFree()

@app.route('/', methods=['GET'])
def home():
    """API documentation"""
    return jsonify({
        'name': '🆓 TikTok Stats API (FREE DEPLOYMENT)',
        'version': '1.0',
        'description': 'API gratis untuk mengambil statistik TikTok user',
        'deployment': 'Free cloud platform (Heroku/Railway/Render)',
        'features': [
            '🆓 Completely FREE to use',
            '🚀 No VPS needed',
            '🔧 Auto Chrome + ChromeDriver setup',
            '📊 Real-time TikTok stats',
            '🌍 Global deployment'
        ],
        'endpoints': {
            'GET /': 'API documentation',
            'GET /health': 'Health check',
            'GET /api/user/<username>': 'Get TikTok user stats',
            'POST /api/user': 'Get TikTok user stats (JSON body)',
            'POST /api/batch': 'Get multiple users stats (max 3)'
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
                'message': 'Data scraped successfully',
                'platform': 'Free Cloud Deployment'
            }
        },
        'deployment_platforms': [
            '🚀 Railway.app (RECOMMENDED)',
            '🟣 Heroku',
            '🟢 Render.com',
            '🔵 Fly.io'
        ],
        'cost': '$0 💰'
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': '🆓 Free TikTok API is running!',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'version': '1.0 (Free Cloud)',
        'scraper_active': api.scraper is not None,
        'platform': os.environ.get('PLATFORM', 'Unknown'),
        'cost': '$0'
    })

@app.route('/api/user/<username>', methods=['GET'])
def get_user_stats(username):
    """Get TikTok user statistics"""
    try:
        if not username or len(username.strip()) == 0:
            return jsonify({
                'success': False,
                'message': 'Username is required'
            }), 400
        
        username = username.strip()
        
        # Basic validation
        if len(username) > 50:
            return jsonify({
                'success': False,
                'message': 'Username too long'
            }), 400
        
        logger.info(f"🎯 FREE API request for user: {username}")
        
        # Cleanup idle scraper
        api.cleanup_scraper()
        
        # Scrape data
        result = api.scrape_user(username)
        
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
    """Get TikTok user statistics via POST"""
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
        
        logger.info(f"🎯 FREE POST API request for user: {username}")
        
        # Cleanup idle scraper
        api.cleanup_scraper()
        
        # Scrape data
        result = api.scrape_user(username)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"POST API error: {e}")
        return jsonify({
            'success': False,
            'message': f'Internal server error: {str(e)}'
        }), 500

@app.route('/api/batch', methods=['POST'])
def get_batch_stats():
    """Get multiple users' statistics"""
    try:
        data = request.get_json()
        
        if not data or 'usernames' not in data:
            return jsonify({
                'success': False,
                'message': 'usernames array is required in JSON body'
            }), 400
        
        usernames = data['usernames']
        
        if not isinstance(usernames, list) or len(usernames) == 0:
            return jsonify({
                'success': False,
                'message': 'usernames must be a non-empty array'
            }), 400
        
        # Limit for free tier
        if len(usernames) > 2:
            return jsonify({
                'success': False,
                'message': 'Maximum 2 usernames per batch request (free tier limit)'
            }), 400
        
        logger.info(f"🎯 FREE Batch API request for users: {usernames}")
        
        # Cleanup idle scraper
        api.cleanup_scraper()
        
        results = []
        for username in usernames:
            if isinstance(username, str) and username.strip():
                username = username.strip()
                result = api.scrape_user(username)
                results.append(result)
                
                # Small delay between requests
                time.sleep(3)
        
        return jsonify({
            'success': True,
            'count': len(results),
            'data': results,
            'platform': 'Free Cloud Deployment'
        })
        
    except Exception as e:
        logger.error(f"Batch API error: {e}")
        return jsonify({
            'success': False,
            'message': f'Internal server error: {str(e)}'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Endpoint not found',
        'tip': 'Check /api/user/<username> or POST /api/user'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # Get port from environment (for cloud deployment)
    port = int(os.environ.get('PORT', 5000))
    
    print("🆓 Starting FREE TikTok Stats API...")
    print("💰 Cost: $0 (Completely FREE!)")
    print("🚀 Platform: Free Cloud Deployment")
    print("📡 API Endpoints:")
    print("   GET  /                     - API documentation")
    print("   GET  /health               - Health check")
    print("   GET  /api/user/<username>  - Get user stats")
    print("   POST /api/user             - Get user stats (JSON)")
    print("   POST /api/batch            - Get multiple users (max 2)")
    print("")
    print(f"⚡ Starting server on port {port}")
    print("🔧 Using Selenium scraper for accurate data extraction")
    
    try:
        app.run(host='0.0.0.0', port=port, debug=False)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        if api.scraper:
            api.scraper.close_driver()
    except Exception as e:
        print(f"❌ Server error: {e}")
        if api.scraper:
            api.scraper.close_driver()