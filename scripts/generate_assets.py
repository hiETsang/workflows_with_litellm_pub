import os
import requests
from urllib.parse import urlparse
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AssetGenerator:
    def __init__(self, apiflash_key: str):
        self.apiflash_key = apiflash_key

    @staticmethod
    def _extract_tool_name(url: str) -> str:
        """从 URL 中提取工具名称，与 app.py 保持一致"""
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            name = domain.replace('www.', '').split('.')[0]
            return name
        except Exception as e:
            logger.error(f"Error extracting tool name from URL: {e}")
            return "unknown"

    @staticmethod
    def _clean_url(url: str) -> str:
        """清理 URL，移除协议和 www 前缀"""
        try:
            parsed = urlparse(url)
            clean_domain = parsed.netloc.replace('www.', '')
            return clean_domain
        except Exception as e:
            logger.error(f"Error cleaning URL: {e}")
            return url

    def get_logo(self, url: str) -> bytes:
        """使用 img logo API 获取网站 logo"""
        try:
            clean_url = self._clean_url(url)
            logo_url = f"https://img.logo.dev/{clean_url}?token=pk_flBx7FQ8T7i0rIbWfbJgDw&retina=true"
            logger.info(f"Fetching logo from: {logo_url}")
            
            response = requests.get(logo_url)
            logger.info(f"Logo fetch status: {response.status_code}")
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.error(f"Error fetching logo: {e}")
            raise

    def get_screenshot(self, url: str) -> bytes:
        """使用 Apiflash API 获取网站截图"""
        logger.info(f"Fetching screenshot for URL: {url}")
        params = {
            "access_key": self.apiflash_key,
            "url": url,
            "width": 1200,
            "height": 1000,
            "no_cookie_banners": True,
            "scroll_page": True,
            "no_ads": True,
            "wait_until": "page_loaded"
        }
        response = requests.get("https://api.apiflash.com/v1/urltoimage", params=params)
        logger.info(f"Screenshot fetch status: {response.status_code}")
        response.raise_for_status()
        return response.content

    def save_assets(self, url: str):
        """保存 logo 和 screenshot 到本地"""
        logger.info(f"Saving assets for URL: {url}")
        
        # 使用与 app.py 相同的工具名称提取逻辑
        tool_name = self._extract_tool_name(url)
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dir_path = os.path.join(current_dir, 'IndieTO', tool_name)
        os.makedirs(dir_path, exist_ok=True)
        logger.info(f"Directory created: {dir_path}")

        try:
            # 保存 logo
            logo = self.get_logo(url)
            logo_path = os.path.join(dir_path, 'logo.jpg')
            with open(logo_path, 'wb') as f:
                f.write(logo)
            logger.info(f"Logo saved to {logo_path}")
        except Exception as e:
            logger.error(f"Error saving logo: {e}")

        try:
            # 保存 screenshot
            screenshot = self.get_screenshot(url)
            screenshot_path = os.path.join(dir_path, 'screenshot.jpg')
            with open(screenshot_path, 'wb') as f:
                f.write(screenshot)
            logger.info(f"Screenshot saved to {screenshot_path}")
        except Exception as e:
            logger.error(f"Error saving screenshot: {e}")

        return f"Assets saved to {dir_path}"

# Example usage
if __name__ == "__main__":
    generator = AssetGenerator(apiflash_key="your_apiflash_key")
    result = generator.save_assets("https://www.uneed.best/")
    print(result) 