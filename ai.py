import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class aidriver():
    def __init__(self):
        options = Options()
        options.add_argument("--start-maximized")
        #options.add_argument("--headless")
        
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        

        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
            },
        )
        self.driver.get("https://gemini.google.com/")
        print("wait")
        editor_selector = "div[contenteditable='true']"
        editor = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, editor_selector))
        )
        print("init")
        self.driver.execute_script("arguments[0].focus();", editor)
        
    def _wait_for_new_message(self, old_count, timeout=15):
    
        start_time = time.time()
        while True:
            containers = self.driver.find_elements(By.CSS_SELECTOR, 'div.markdown-main-panel')
            if len(containers) > old_count:
                return
                
            if time.time() - start_time > timeout:
                raise TimeoutError("655")
                
            time.sleep(0.3)


    def send_msg(self,message, timeout=15):
        editor = self.driver.find_element(By.CSS_SELECTOR, 'div[contenteditable="true"]')
        editor.send_keys(message)
        time.sleep(0.2)
        editor.send_keys(Keys.ENTER)
        
        old_count = len(self.driver.find_elements(By.CSS_SELECTOR, 'div.markdown-main-panel'))
        
        self._wait_for_new_message(old_count, timeout)
    

    def _get_last_message_text(self):
        try:
            containers = self.driver.find_elements(By.CSS_SELECTOR, 'div.markdown-main-panel')
            if containers:
                return containers[-1].text
        except Exception:
            pass
        return ""
    def _is_generating(self):
        try:
            stop_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'gem-icon-button.send-button.stop')
            return len(stop_buttons) > 0
        except Exception:
            return False
    def get_stream_answer(self):
        last_printed_len = 0
        last_change_time = time.time()

        _ovr = False
        while True:
            current_text = self._get_last_message_text()
            
            if len(current_text) > last_printed_len:
                yield current_text[last_printed_len:]
                last_printed_len = len(current_text)
                last_change_time = time.time() 

            if not self._is_generating():
                _ovr = True
                time.sleep(0.5)
                if (_ovr):
                    break
            
    

            time.sleep(0.3)

