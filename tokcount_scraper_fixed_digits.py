from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import re

class TokCountFixedDigits:
    def __init__(self, headless=False):
        self.options = Options()
        if headless:
            self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--window-size=1920,1080')
        self.options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        self.driver = None
    
    def start_driver(self):
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=self.options)
            return True
        except Exception as e:
            print(f"❌ Error starting driver: {e}")
            return False
    
    def get_element_position(self, element):
        """Get element position for ordering"""
        try:
            location = element.location
            return (location['y'], location['x'])  # Sort by Y first, then X
        except:
            return (0, 0)
    
    def extract_stat_by_keyword(self, keyword):
        """Extract stat for a specific keyword using DOM structure"""
        try:
            print(f"\n🔍 Looking for {keyword}...")
            
            # Find the keyword element
            keyword_elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{keyword}')]")
            
            if not keyword_elements:
                print(f"❌ '{keyword}' not found")
                return None
            
            print(f"✅ Found {len(keyword_elements)} '{keyword}' elements")
            
            for keyword_elem in keyword_elements:
                try:
                    # Get the container that holds both the number and the keyword
                    # Try different parent levels
                    containers = [
                        keyword_elem.find_element(By.XPATH, "./.."),  # Direct parent
                        keyword_elem.find_element(By.XPATH, "./../.."),  # Grandparent
                        keyword_elem.find_element(By.XPATH, "./../../.."),  # Great-grandparent
                    ]
                    
                    for container in containers:
                        try:
                            # Get all elements in this container
                            all_elements = container.find_elements(By.XPATH, ".//*")
                            
                            # Filter elements that contain single digits or commas
                            digit_elements = []
                            
                            for elem in all_elements:
                                try:
                                    text = elem.text.strip()
                                    # Only single digits, commas, or very short numbers
                                    if text and re.match(r'^[\d,]{1,2}$', text):
                                        position = self.get_element_position(elem)
                                        digit_elements.append({
                                            'text': text,
                                            'position': position,
                                            'element': elem
                                        })
                                except:
                                    continue
                            
                            if not digit_elements:
                                continue
                            
                            # Sort by position (top to bottom, left to right)
                            digit_elements.sort(key=lambda x: x['position'])
                            
                            # Remove duplicates based on position proximity
                            unique_digits = []
                            for digit in digit_elements:
                                # Check if this position is too close to existing ones
                                is_duplicate = False
                                for existing in unique_digits:
                                    y_diff = abs(digit['position'][0] - existing['position'][0])
                                    x_diff = abs(digit['position'][1] - existing['position'][1])
                                    
                                    # If positions are very close (within 5 pixels), consider duplicate
                                    if y_diff < 5 and x_diff < 5:
                                        is_duplicate = True
                                        break
                                
                                if not is_duplicate:
                                    unique_digits.append(digit)
                            
                            if unique_digits:
                                # Build the number from unique digits
                                number_parts = [d['text'] for d in unique_digits]
                                number_str = ''.join(number_parts)
                                
                                # Clean up the number
                                number_str = re.sub(r',+', ',', number_str)  # Multiple commas to single
                                number_str = number_str.strip(',')  # Remove leading/trailing commas
                                
                                # Validate it's a reasonable number
                                try:
                                    test_num = int(number_str.replace(',', ''))
                                    if test_num > 0:
                                        print(f"✅ {keyword}: {number_parts} -> {number_str}")
                                        return number_str
                                except:
                                    continue
                        
                        except Exception as e:
                            continue
                
                except Exception as e:
                    continue
            
            print(f"❌ Could not extract number for {keyword}")
            return None
            
        except Exception as e:
            print(f"❌ Error extracting {keyword}: {e}")
            return None
    
    def extract_stats_by_visual_layout(self):
        """Extract stats by analyzing visual layout"""
        try:
            print("\n📐 Analyzing visual layout...")
            
            # Get all elements with single digits or short text
            all_elements = self.driver.find_elements(By.XPATH, "//*[text()]")
            
            # Categorize elements
            digit_elements = []
            keyword_elements = []
            
            for elem in all_elements:
                try:
                    text = elem.text.strip()
                    if not text:
                        continue
                    
                    position = self.get_element_position(elem)
                    
                    # Single digits or commas
                    if re.match(r'^[\d,]{1,2}$', text):
                        digit_elements.append({
                            'text': text,
                            'position': position,
                            'element': elem
                        })
                    
                    # Keywords
                    elif text in ['Followers', 'Likes', 'Following', 'Videos']:
                        keyword_elements.append({
                            'text': text,
                            'position': position,
                            'element': elem
                        })
                
                except:
                    continue
            
            print(f"📊 Found {len(digit_elements)} digit elements, {len(keyword_elements)} keywords")
            
            # Group digits by proximity to keywords
            stats = {}
            
            for keyword_elem in keyword_elements:
                keyword = keyword_elem['text']
                keyword_pos = keyword_elem['position']
                
                # Find digits that are close to this keyword (above or to the left)
                nearby_digits = []
                
                for digit_elem in digit_elements:
                    digit_pos = digit_elem['position']
                    
                    # Calculate distance
                    y_distance = keyword_pos[0] - digit_pos[0]  # Positive if digit is above
                    x_distance = abs(keyword_pos[1] - digit_pos[1])  # Horizontal distance
                    
                    # Digits should be close vertically and horizontally
                    if 0 <= y_distance <= 100 and x_distance <= 200:  # Within reasonable range
                        nearby_digits.append({
                            'text': digit_elem['text'],
                            'position': digit_pos,
                            'distance': y_distance + x_distance  # Combined distance
                        })
                
                if nearby_digits:
                    # Sort by position (left to right, top to bottom)
                    nearby_digits.sort(key=lambda x: (x['position'][0], x['position'][1]))
                    
                    # Remove duplicates based on position
                    unique_digits = []
                    for digit in nearby_digits:
                        is_duplicate = False
                        for existing in unique_digits:
                            y_diff = abs(digit['position'][0] - existing['position'][0])
                            x_diff = abs(digit['position'][1] - existing['position'][1])
                            
                            if y_diff < 10 and x_diff < 10:  # Very close positions
                                is_duplicate = True
                                break
                        
                        if not is_duplicate:
                            unique_digits.append(digit)
                    
                    # Build number
                    if unique_digits:
                        number_parts = [d['text'] for d in unique_digits]
                        number_str = ''.join(number_parts)
                        number_str = re.sub(r',+', ',', number_str).strip(',')
                        
                        try:
                            test_num = int(number_str.replace(',', ''))
                            if test_num >= 0:  # Allow 0 for following
                                stats[keyword.lower()] = number_str
                                print(f"✅ {keyword}: {number_parts} -> {number_str}")
                        except:
                            continue
            
            return stats
            
        except Exception as e:
            print(f"❌ Error in visual layout analysis: {e}")
            return {}
    
    def scrape_user_data(self, username):
        """Main scraping function"""
        if not self.driver:
            if not self.start_driver():
                return None
        
        url = f"https://tokcount.com/?user={username}"
        
        try:
            print(f"🌐 Loading: {url}")
            self.driver.get(url)
            
            # Wait for page load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Wait for animations to complete
            print("⏳ Waiting for digit animations...")
            time.sleep(12)  # Longer wait for animations
            
            # Try visual layout method first
            stats = self.extract_stats_by_visual_layout()
            
            # Fill in missing stats with keyword method
            keywords = ['Followers', 'Likes', 'Following', 'Videos']
            for keyword in keywords:
                key = keyword.lower()
                if key not in stats or stats[key] == 'Not found':
                    result = self.extract_stat_by_keyword(keyword)
                    if result:
                        stats[key] = result
            
            # Ensure all keys exist
            final_stats = {
                'username': username,
                'followers': stats.get('followers', 'Not found'),
                'likes': stats.get('likes', 'Not found'),
                'following': stats.get('following', 'Not found'),
                'videos': stats.get('videos', 'Not found')
            }
            
            # Take screenshot
            try:
                self.driver.save_screenshot(f"{username}_fixed_digits_screenshot.png")
                print(f"📸 Screenshot: {username}_fixed_digits_screenshot.png")
            except:
                pass
            
            return final_stats
            
        except Exception as e:
            print(f"❌ Error scraping: {e}")
            return None
    
    def close_driver(self):
        if self.driver:
            self.driver.quit()

def main():
    print("🔧 TokCount Fixed Digits Scraper")
    print("=" * 50)
    print("🎯 Fixes duplicate digit collection")
    print("📐 Uses visual layout analysis")
    print("🚫 Removes duplicate positions")
    print("=" * 50)
    
    scraper = TokCountFixedDigits(headless=False)
    
    username = "rafiedotid"
    print(f"🎯 Target: {username}")
    
    user_data = scraper.scrape_user_data(username)
    
    if user_data:
        print("\n" + "🎉 HASIL FINAL" + "\n" + "=" * 40)
        for key, value in user_data.items():
            icon = {"username": "👤", "followers": "👥", "likes": "❤️", 
                   "following": "➡️", "videos": "🎬"}.get(key, "📊")
            print(f"{icon} {key.title()}: {value}")
        
        # Validate results look reasonable
        print(f"\n🔍 VALIDATION:")
        for key, value in user_data.items():
            if key != 'username' and value != 'Not found':
                try:
                    num = int(value.replace(',', ''))
                    if key == 'followers' and num > 1000:
                        print(f"✅ {key}: {value} (looks good)")
                    elif key == 'likes' and num > 100:
                        print(f"✅ {key}: {value} (looks good)")
                    elif key in ['following', 'videos'] and 0 <= num <= 10000:
                        print(f"✅ {key}: {value} (looks good)")
                    else:
                        print(f"⚠️  {key}: {value} (check this)")
                except:
                    print(f"❌ {key}: {value} (invalid format)")
        
        # Save result
        filename = f"{username}_data_fixed.json"
        with open(filename, "w") as f:
            json.dump(user_data, f, indent=2)
        print(f"\n💾 Saved: {filename}")
        
    else:
        print("❌ Failed to extract data")
    
    input("\n⏸️  Press Enter to close...")
    scraper.close_driver()

if __name__ == "__main__":
    main()