import customtkinter as ctk
import webbrowser
import time
import requests
import threading

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
def get_content(page, year, cookies):
    url = "https://api.chzzk.naver.com/commercial/v1/product/purchase/history?page=%d&size=10&searchYear=%d"%(page, year)
    try:
        return requests.get(url, cookies=cookies, headers=headers).json()["content"]
    except:
        time.sleep(5)
        return requests.get(url, cookies=cookies, headers=headers).json()["content"]

# 함수 정의
def open_github():
    github_url = "https://github.com/junobonnie/chzzk_pay_amount_calculator"  # 이동할 GitHub 페이지 URL
    webbrowser.open(github_url)  # 기본 브라우저로 URL 열기

def get_NID():
    with open("NID.txt", "r") as f:
        NID = f.read().split(" ")
    if not len(NID) == 2:
        NID = ["", ""]
    return NID

# 팝업창 생성 함수
def open_popup():
    # 팝업 창 생성
    popup = ctk.CTkToplevel(app)
    popup.geometry("250x150")
    popup.title("NID 수정")
    popup.grab_set()  # 모달 창으로 설정 (메인 창 비활성화)

    NID_AUT, NID_SES = get_NID()

    # 라벨과 입력창을 같은 행에 배치
    input_area = ctk.CTkFrame(popup, width=250, corner_radius=0)
    input_area.pack()
    
    label_prompt1 = ctk.CTkLabel(input_area, text="NID_AUT")
    label_prompt1.grid(row=0, column=0, padx=10, pady=10, sticky="w")  # 좌측 정렬
    
    entry1 = ctk.CTkEntry(input_area, width=150, placeholder_text=NID_AUT)
    entry1.grid(row=0, column=1, padx=10, pady=10)
    
    label_prompt2 = ctk.CTkLabel(input_area, text="NID_SES")
    label_prompt2.grid(row=1, column=0, padx=10, pady=10, sticky="w")  # 좌측 정렬
    
    entry2 = ctk.CTkEntry(input_area, width=150, placeholder_text=NID_SES)
    entry2.grid(row=1, column=1, padx=10, pady=10)
    
    def save_NID():
        NID_AUT = entry1.get()  # 입력 필드의 텍스트 가져오기
        NID_SES = entry2.get()
        
        if not (NID_AUT == "" and NID_SES == ""):
            with open("NID.txt", "w") as f:
                f.write(NID_AUT+" "+NID_SES)
            
            new_popup = ctk.CTkToplevel(app)
            new_popup.geometry("100x50")
            new_popup.title("")
            new_popup.grab_set()
            label = ctk.CTkLabel(new_popup, text="저장완료")
            label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        
    button0 = ctk.CTkButton(popup, text="저장하기", command=save_NID)
    button0.pack(padx=10, pady=10)

def open_my_pay_log():
    webbrowser.open("https://game.naver.com/profile#cash")

def calculate():
    NID_AUT, NID_SES = get_NID()
    cookies = {"NID_AUT":NID_AUT, "NID_SES":NID_SES}
    
    try:
        content = get_content(0, 2023, cookies)
    except:
        new_popup = ctk.CTkToplevel(app)
        new_popup.geometry("200x50")
        new_popup.title("오류!")
        new_popup.grab_set()
        label = ctk.CTkLabel(new_popup, text="NID가 없거나 잘못되었습니다.")
        label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        return
    
    for i in labels:
        i.destroy()  # 라벨 파괴
    labels.clear()  # 리스트 비우기
    
    total_pay_amount = {}
    for year in range(2023, time.localtime().tm_year+1):
        content = get_content(0, year, cookies)
        page_num = content["totalPages"]
        for i in reversed(range(page_num)):
            label = ctk.CTkLabel(scrollable_frame, text="%d년도 내역 검색 중"%(year)+(i%6)*".", width=100, height=20)
            label.grid(padx=5, pady=5) 
            progress_bar.set(1-i/page_num)
            for data in get_content(i, year, cookies)["data"]:
                channel_id = data["channelId"]
                pay_amount = data["payAmount"]
                
                if channel_id in total_pay_amount:
                    total_pay_amount[channel_id] += pay_amount
                else:
                    total_pay_amount[channel_id] = pay_amount
            label.destroy() 
    
    total = 0
    row = 0
    for channel_id, pay_amount in sorted(total_pay_amount.items(), key= lambda item:item[1], reverse=True):
        total += pay_amount
        url = "https://api.chzzk.naver.com/service/v1/channels/" + channel_id
        streamer_name = requests.get(url, headers=headers).json()["content"]["channelName"]
        # 라벨 추가 (2행 110열)
        label = ctk.CTkLabel(scrollable_frame, text=streamer_name, width=100, height=20)
        label.grid(row=row, column=0, padx=5, pady=5)  # 그리드 레이아웃으로 배치
        labels.append(label)
        label = ctk.CTkLabel(scrollable_frame, text=pay_amount, width=100, height=20)
        label.grid(row=row, column=1, padx=5, pady=5)  # 그리드 레이아웃으로 배치
        labels.append(label)
        row += 1
    label = ctk.CTkLabel(scrollable_frame, text="총합: %d"%total, width=100, height=20)
    label.grid(row=row+2, column=0, padx=5, pady=5)  # 그리드 레이아웃으로 배치
    labels.append(label)
    
def start_calculate():
    thread = threading.Thread(target=calculate)  # 작업을 백그라운드 스레드에서 실행
    thread.start()
    
# CustomTkinter 초기화
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# 메인 창 생성
app = ctk.CTk()
app.geometry("500x400")
app.title("치즈 사용내역 총합 계산기")
app.iconbitmap("icon.ico")


# 좌측 메뉴바 생성
menu_bar = ctk.CTkFrame(app, width=150, corner_radius=0)
menu_bar.pack(side="left", fill="y")

button1 = ctk.CTkButton(menu_bar, text="프로그램 정보", command=open_github)
button1.pack(pady=10, padx=10, fill="x")

button2 = ctk.CTkButton(menu_bar, text="NID 수정", command=open_popup)
button2.pack(pady=10, padx=10, fill="x")

button3 = ctk.CTkButton(menu_bar, text="치즈 사용내역 보기", command=open_my_pay_log)
button3.pack(pady=10, padx=10, fill="x")

button4 = ctk.CTkButton(menu_bar, text="치즈 사용내역 총합", command=start_calculate)
button4.pack(pady=10, padx=10, fill="x")

labels = []

# 프로그래스바 추가
progress_bar = ctk.CTkProgressBar(menu_bar, width=150)
progress_bar.pack(pady=10, side="bottom")

progress_bar.set(1.)

# 메인 컨텐츠 영역
main_content = ctk.CTkFrame(app, corner_radius=0)
main_content.pack(side="left", fill="both", expand=True)

# 스크롤 가능한 프레임 생성
scrollable_frame = ctk.CTkScrollableFrame(main_content, width=580, height=300)
scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)
    

# 실행
app.mainloop()
