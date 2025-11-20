from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import re
import logging
import os

logger = logging.getLogger(__name__)

class TokCountScraperRailway:
    def __init__(self, headless=True):
        self.driver = None
        self.headless = headless
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome driver for Railway/cloud platforms"""
        try:
            options = Options()
            
            if self.headless:
                options.add_argument('--headless')
            
            # Essential arguments for cloud platforms
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins')
            options.add_argument('--disable-images')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--remote-debugging-port=9222')
            
            # Try different Chrome binary locations
            chrome_paths = [
                '/usr/bin/chromium',
                '/usr/bin/chromium-browser', 
                '/usr/bin/google-chrome',
                '/usr/bin/google-chrome-stable',
                '/app/.chrome-for-testing/chrome-linux64/chrome',
                os.environ.get('GOOGLE_CHROME_BIN'),
                None
            ]
            
            driver_created = False
            
            for chrome_path in chrome_paths:
                if chrome_path and not os.path.exists(chrome_path):
                    continue
                    
                try:
                    if chrome_path:
                        options.binary_location = chrome_path
                        logger.info(f"Trying Chrome at: {chrome_path}")
                    
                    # Try different ChromeDriver paths
                    chromedriver_paths = [
                        '/usr/bin/chromedriver',
                        os.environ.get('CHROMEDRIVER_PATH'),
                        None  # Let webdriver-manager handle it
                    ]
                    
                    for driver_path in chromedriver_paths:
                        try:
                            if driver_path and os.path.exists(driver_path):
                                service = Service(driver_path)
                                logger.info(f"Using ChromeDriver at: {driver_path}")
                            else:
                                # Try webdriver-manager as fallback
                                from webdriver_manager.chrome import ChromeDriverManager
                                service = Service(ChromeDriverManager().install())
                                logger.info("Using webdriver-manager")
                            
                            self.driver = webdriver.Chrome(service=service, options=options)
                            logger.info(f"✅ Chrome driver initialized successfully")
                            driver_created = True
                            break
                            
                        except Exception as e:
                            logger.warning(f"Failed with driver path {driver_path}: {e}")
                            continue
                    
                    if driver_created:
                        break
                        
                except Exception as e:
                    logger.warning(f"Failed with Chrome path {chrome_path}: {e}")
                    continue
            
            if not driver_created:
                raise Exception("Could not initialize Chrome driver")
                
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to setup driver: {e}")
            return False
    
    def get_element_position(self, element):
        """Get element position for ordering"""
        try:
            location = element.location
            return (location['y'], location['x'])
        except:
            return (0, 0)
    
    def extract_stats_by_visual_layout(self):
        """Extract stats using visual layout analysis"""
        try:
            all_elements = self.driver.find_elements(By.XPATH, "//*[text()]")
            
            digit_elements = []
            keyword_elements = []
            
            for elem in all_elements:
                try:
                    text = elem.text.strip()
                    if not text:
                        continue
                    
                    position = self.get_element_position(elem)
                    
                    if re.match(r'^[\d,]{1,2}$', text):
                        digit_elements.append({
                            'text': text,
                            'position': position,
                            'element': elem
                        })
                    elif text in ['Followers', 'Likes', 'Following', 'Videos']:
                        keyword_elements.append({
                            'text': text,
                            'position': position,
                            'element': elem
                        })
                
                except:
                    continue
            
            logger.info(f"Found {len(digit_elements)} digit elements, {len(keyword_elements)} keywords")
            
            stats = {}
            
            for keyword_elem in keyword_elements:
                keyword = keyword_elem['text']
                keyword_pos = keyword_elem['position']
                
                nearby_digits = []
                
                for digit_elem in digit_elements:
                    digit_pos = digit_elem['position']
                    y_distance = keyword_pos[0] - digit_pos[0]
                    x_distance = abs(keyword_pos[1] - digit_pos[1])
                    
                    if 0 <= y_distance <= 100 and x_distance <= 200:
                        nearby_digits.append({
                            'text': digit_elem['text'],
                            'position': digit_pos,
                            'distance': y_distance + x_distance
                        })
                
                if nearby_digits:
                    nearby_digits.sort(key=lambda x: (x['position'][0], x['position'][1]))
                    
                    unique_digits = []
                    for digit in nearby_digits:
                        is_duplicate = False
                        for existing in unique_digits:
                            y_diff = abs(digit['position'][0] - existing['position'][0])
                            x_diff = abs(digit['position'][1] - existing['position'][1])
                            
                            if y_diff < 10 and x_diff < 10:
                                is_duplicate = True
                                break
                        
                        if not is_duplicate:
                            unique_digits.append(digit)
                    
                    if unique_digits:
                        number_parts = [d['text'] for d in unique_digits]
                        number_str = ''.join(number_parts)
                        number_str = re.sub(r',+', ',', number_str).strip(',')
                        
                        try:
                            test_num = int(number_str.replace(',', ''))
                            if test_num >= 0:
                                stats[keyword.lower()] = number_str
                                logger.info(f"Extracted {keyword}: {number_str}")
                        except:
                            continue
            
            return stats
            
        except Exception as e:
            logger.error(f"Error in visual layout analysis: {e}")
            return {}
    
    def scrape_user_data(self, username):
        """Main scraping function"""
        if not self.driver:
            if not self.setup_driver():
                return None
        
        url = f"https://tokcount.com/?user={username}"
        
        try:
            logger.info(f"🌐 Loading: {url}")
            self.driver.get(url)
            
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            logger.info("⏳ Waiting for digit animations...")
            time.sleep(12)
            
            stats = self.extract_stats_by_visual_layout()
            
            final_stats = {
                'username': username,
                'followers': stats.get('followers', 'Not found'),
                'likes': stats.get('likes', 'Not found'),
                'following': stats.get('following', 'Not found'),
                'videos': stats.get('videos', 'Not found')
            }
            
            try:
                self.driver.save_screenshot(f"{username}_railway_screenshot.png")
                logger.info(f"📸 Screenshot: {username}_railway_screenshot.png")
            except:
                pass
            
            return final_stats
            
        except Exception as e:
            logger.error(f"Error scraping data: {e}")
            return None
    
    def close_driver(self):
        """Close the browser driver"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass