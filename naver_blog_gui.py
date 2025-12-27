import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import time
import threading
import random


class NaverBlogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("네이버 블로그 포스팅 프로그램")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        self.driver = None
        self.is_logged_in = False
        
        self.create_widgets()
    
    def human_typing(self, element, text):
        """사람처럼 타이핑하는 함수"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))  # 랜덤 타이핑 지연
    
    def move_to_element_naturally(self, element):
        """자연스럽게 요소로 마우스 이동"""
        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            time.sleep(random.uniform(0.3, 0.7))
        except:
            pass
    
    def random_scroll(self):
        """랜덤 스크롤 - 사람처럼 행동"""
        try:
            scroll_amount = random.randint(100, 300)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(0.5, 1.0))
            self.driver.execute_script(f"window.scrollBy(0, -{scroll_amount});")
            time.sleep(random.uniform(0.3, 0.6))
        except:
            pass
    
    def create_widgets(self):
        # 스타일 설정
        style = ttk.Style()
        style.configure('Title.TLabel', font=('맑은 고딕', 14, 'bold'))
        style.configure('Section.TLabel', font=('맑은 고딕', 10, 'bold'))
        
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 제목
        title_label = ttk.Label(main_frame, text="네이버 블로그 자동 포스팅", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 로그인 섹션
        login_frame = ttk.LabelFrame(main_frame, text=" 로그인 정보 ", padding="10")
        login_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # 아이디 입력
        ttk.Label(login_frame, text="아이디:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.id_entry = ttk.Entry(login_frame, width=40)
        self.id_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # 비밀번호 입력
        ttk.Label(login_frame, text="비밀번호:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.pw_entry = ttk.Entry(login_frame, width=40, show="*")
        self.pw_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # 로그인 버튼
        self.login_btn = ttk.Button(login_frame, text="로그인", command=self.login)
        self.login_btn.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        # 로그인 상태 표시
        self.login_status = ttk.Label(login_frame, text="로그인 필요", foreground="red")
        self.login_status.grid(row=3, column=0, columnspan=2, pady=(5, 0))
        
        # 포스팅 섹션
        post_frame = ttk.LabelFrame(main_frame, text=" 블로그 포스팅 ", padding="10")
        post_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        
        # 제목 입력
        ttk.Label(post_frame, text="제목:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.title_entry = ttk.Entry(post_frame, width=50)
        self.title_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 내용 입력
        ttk.Label(post_frame, text="내용:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.content_text = scrolledtext.ScrolledText(post_frame, width=50, height=15, wrap=tk.WORD)
        self.content_text.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 카테고리 선택
        category_frame = ttk.Frame(post_frame)
        category_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(category_frame, text="카테고리:").pack(side=tk.LEFT, padx=(0, 10))
        self.category_entry = ttk.Entry(category_frame, width=30)
        self.category_entry.pack(side=tk.LEFT)
        self.category_entry.insert(0, "일상")
        
        # 공개 설정
        self.public_var = tk.BooleanVar(value=True)
        public_check = ttk.Checkbutton(post_frame, text="전체공개", variable=self.public_var)
        public_check.grid(row=5, column=0, sticky=tk.W, pady=(0, 10))
        
        # 포스팅 버튼
        self.post_btn = ttk.Button(post_frame, text="포스팅하기", command=self.post_blog, state='disabled')
        self.post_btn.grid(row=6, column=0, pady=(10, 0))
        
        # 상태 표시
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Label(status_frame, text="상태:", style='Section.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        self.status_label = ttk.Label(status_frame, text="대기 중", foreground="gray")
        self.status_label.pack(side=tk.LEFT)
    
    def login(self):
        """네이버 로그인 처리"""
        user_id = self.id_entry.get()
        user_pw = self.pw_entry.get()
        
        if not user_id or not user_pw:
            messagebox.showerror("오류", "아이디와 비밀번호를 입력해주세요.")
            return
        
        # 별도 스레드에서 로그인 처리
        threading.Thread(target=self._login_process, args=(user_id, user_pw), daemon=True).start()
    
    def _login_process(self, user_id, user_pw):
        """로그인 프로세스 (백그라운드)"""
        try:
            self.update_status("브라우저 시작 중...")
            self.login_btn.config(state='disabled')
            
            # Undetected ChromeDriver 시작 (최대 강화 모드)
            options = uc.ChromeOptions()
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--start-maximized')
            options.add_argument('--disable-notifications')
            options.add_argument('--disable-popup-blocking')
            options.add_argument('--disable-extensions')
            
            # User-Agent 설정 (실제 사용자)
            options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
            
            # Stealth 모드로 실행
            self.driver = uc.Chrome(options=options, use_subprocess=True, version_main=None)
            
            # JavaScript로 webdriver 속성 제거
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    window.navigator.chrome = {
                        runtime: {}
                    };
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5]
                    });
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['ko-KR', 'ko', 'en-US', 'en']
                    });
                '''
            })
            
            # 먼저 네이버 메인 페이지 방문 (실제 사용자처럼)
            self.update_status("네이버 접속 중...")
            self.driver.get("https://www.naver.com")
            time.sleep(random.uniform(3, 5))  # 충분한 로딩 시간
            
            # 스크롤로 자연스러운 행동 시뮬레이션
            self.random_scroll()
            time.sleep(random.uniform(1, 2))
            
            # 네이버 로그인 페이지 접속
            self.update_status("로그인 페이지 접속 중...")
            self.driver.get("https://nid.naver.com/nidlogin.login")
            
            # ID 입력창 대기
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "id"))
            )
            time.sleep(random.uniform(2, 3))
            
            # ID 입력 (자연스럽게 마우스 이동 후 타이핑)
            self.update_status("아이디 입력 중...")
            id_box = self.driver.find_element(By.ID, "id")
            self.move_to_element_naturally(id_box)
            id_box.click()
            time.sleep(random.uniform(0.5, 1.2))
            self.human_typing(id_box, user_id)
            time.sleep(random.uniform(0.8, 1.5))
            
            # PW 입력 (자연스럽게 마우스 이동 후 타이핑)
            self.update_status("비밀번호 입력 중...")
            pw_box = self.driver.find_element(By.ID, "pw")
            self.move_to_element_naturally(pw_box)
            pw_box.click()
            time.sleep(random.uniform(0.5, 1.2))
            self.human_typing(pw_box, user_pw)
            time.sleep(random.uniform(1.0, 2.0))
            
            # 로그인 버튼 클릭
            self.update_status("로그인 버튼 클릭...")
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "log.login"))
            )
            self.driver.find_element(By.ID, "log.login").click()
            
            # 캡챠 또는 로그인 완료 대기
            self.update_status("로그인 처리 중... (캡챠가 나타나면 수동으로 해결해주세요)")
            time.sleep(3)
            
            # 로그인 성공 확인 (현재 URL 체크)
            current_url = self.driver.current_url
            if "nid.naver.com" not in current_url or "nidlogin" not in current_url:
                self.is_logged_in = True
                self.update_status("로그인 성공!", "green")
                self.login_status.config(text="로그인 완료", foreground="green")
                self.post_btn.config(state='normal')
            else:
                self.update_status("로그인 확인 필요 - 캡챠를 풀어주세요", "orange")
                messagebox.showinfo("알림", "캡챠가 나타났다면 수동으로 해결 후 확인 버튼을 눌러주세요.")
                
                # 로그인 완료 대기
                time.sleep(5)
                if "nid.naver.com" not in self.driver.current_url or "nidlogin" not in self.driver.current_url:
                    self.is_logged_in = True
                    self.update_status("로그인 성공!", "green")
                    self.login_status.config(text="로그인 완료", foreground="green")
                    self.post_btn.config(state='normal')
            
        except Exception as e:
            self.update_status(f"로그인 오류: {str(e)}", "red")
            messagebox.showerror("로그인 오류", f"로그인 중 오류가 발생했습니다:\n{str(e)}")
            self.login_btn.config(state='normal')
    
    def post_blog(self):
        """블로그 포스팅"""
        if not self.is_logged_in or not self.driver:
            messagebox.showerror("오류", "먼저 로그인해주세요.")
            return
        
        title = self.title_entry.get()
        content = self.content_text.get("1.0", tk.END).strip()
        
        if not title or not content:
            messagebox.showerror("오류", "제목과 내용을 입력해주세요.")
            return
        
        # 별도 스레드에서 포스팅 처리
        threading.Thread(target=self._post_process, args=(title, content), daemon=True).start()
    
    def _post_process(self, title, content):
        """포스팅 프로세스 (백그라운드)"""
        try:
            self.update_status("블로그 글쓰기 페이지로 이동 중...")
            self.post_btn.config(state='disabled')
            
            # 네이버 블로그 글쓰기 페이지로 이동
            self.driver.get("https://blog.naver.com/")
            time.sleep(2)
            
            # 글쓰기 버튼 찾기 및 클릭
            self.update_status("글쓰기 페이지 로딩 중...")
            
            # 새 글쓰기 페이지로 직접 이동
            self.driver.get("https://blog.naver.com/PostWriteForm.naver")
            time.sleep(3)
            
            # iframe으로 전환 (블로그 에디터는 iframe 내부에 있음)
            self.update_status("에디터 로딩 중...")
            WebDriverWait(self.driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.ID, "mainFrame"))
            )
            
            # 제목 입력
            self.update_status("제목 입력 중...")
            title_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "se-input"))
            )
            title_box.click()
            time.sleep(0.5)
            pyperclip.copy(title)
            title_box.send_keys(Keys.CONTROL, 'v')
            time.sleep(0.5)
            
            # 본문 입력 (스마트에디터)
            self.update_status("본문 입력 중...")
            
            # 본문 영역 클릭
            content_area = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "se-component-content"))
            )
            content_area.click()
            time.sleep(0.5)
            
            # 내용 붙여넣기
            pyperclip.copy(content)
            content_area.send_keys(Keys.CONTROL, 'v')
            time.sleep(1)
            
            self.update_status("포스팅 준비 완료! 수동으로 발행 버튼을 눌러주세요.", "blue")
            messagebox.showinfo("알림", "글 작성이 완료되었습니다.\n수동으로 카테고리 설정 및 발행 버튼을 눌러주세요.")
            
            self.post_btn.config(state='normal')
            
        except Exception as e:
            self.update_status(f"포스팅 오류: {str(e)}", "red")
            messagebox.showerror("포스팅 오류", f"포스팅 중 오류가 발생했습니다:\n{str(e)}")
            self.post_btn.config(state='normal')
            
            # 메인 프레임으로 돌아가기
            try:
                self.driver.switch_to.default_content()
            except:
                pass
    
    def update_status(self, message, color="black"):
        """상태 메시지 업데이트"""
        self.status_label.config(text=message, foreground=color)
    
    def on_closing(self):
        """프로그램 종료 시"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"브라우저 종료 중 오류 (무시됨): {e}")
                pass
        try:
            self.root.destroy()
        except:
            pass


def main():
    root = tk.Tk()
    app = NaverBlogApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
