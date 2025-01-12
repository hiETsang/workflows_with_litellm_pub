import os
import requests
from pathlib import Path

def download_logo(domain: str, output_dir: Path) -> Path:
    """下载网站 logo"""
    logo_url = f"https://img.logo.dev/{domain}?token=pk_flBx7FQ8T7i0rIbWfbJgDw&retina=true"
    logo_path = output_dir / "logo.png"
    
    response = requests.get(logo_url)
    if response.status_code == 200:
        with open(logo_path, "wb") as f:
            f.write(response.content)
    return logo_path

def download_screenshot(url: str, output_dir: Path) -> Path:
    """下载网站截图"""
    api_key = os.getenv("APIFLASH_KEY", "7716ac4eb9d64fa5911ce98d1bb8fd71")
    screenshot_url = f"https://api.apiflash.com/v1/urltoimage"
    params = {
        "access_key": api_key,
        "url": url,
        "width": 1200,
        "height": 1000,
        "wait_until": "page_loaded",
        "no_cookie_banners": True,
        "scroll_page": True,
        "no_ads": True
    }
    
    screenshot_path = output_dir / "screenshot.png"
    response = requests.get(screenshot_url, params=params)
    if response.status_code == 200:
        with open(screenshot_path, "wb") as f:
            f.write(response.content)
    return screenshot_path

def main(url: str, output_dir: str):
    """主函数"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    domain = url.split("//")[-1].split("/")[0]
    logo_path = download_logo(domain, output_path)
    screenshot_path = download_screenshot(url, output_path)
    
    return {
        "logo": str(logo_path),
        "screenshot": str(screenshot_path)
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python download_assets.py <url> <output_dir>")
        sys.exit(1)
    
    url = sys.argv[1]
    output_dir = sys.argv[2]
    result = main(url, output_dir)
    print(result) 