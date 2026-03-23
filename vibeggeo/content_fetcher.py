from playwright.sync_api import sync_playwright
import base64

def fetch_content_from_url(url):
    """
    极简版抓取：移除不稳定的 stealth 库，改用纯手动伪装
    """
    with sync_playwright() as p:
        try:
            # 1. 启动浏览器
            browser = p.chromium.launch(headless=True)
            # 2. 伪装成一个普通的 Mac Chrome 浏览器
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={'width': 1280, 'height': 800}
            )
            page = context.new_page()
            
            # 3. 访问网页
            # 使用 domcontentloaded 速度更快，更不容易被拦截
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # 4. 停顿几秒，假装在看页面，顺便等图片加载
            page.wait_for_timeout(5000) 
            
            # 5. 截图（这是我们的保底方案）
            screenshot = page.screenshot(full_page=False)
            screenshot_base64 = base64.b64encode(screenshot).decode('utf-8')
            
            # 6. 提取文字
            text_content = page.inner_text("body")
            
            # 7. 如果被丝芙兰拦截了，文字会包含 Access Denied
            if "Access Denied" in text_content or "Permission" in text_content or len(text_content) < 200:
                print("Text blocked or too short, rely on Vision AI.")
                text_content = "" # 设为空，触发后端的视觉读图模式
                
            browser.close()
            return text_content, screenshot_base64
            
        except Exception as e:
            print(f"Scraping Error: {e}")
            try: browser.close()
            except: pass
            return "", None