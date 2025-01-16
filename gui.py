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

def get_popup_pos(popup_width, popup_height):
    root_x = app.winfo_x()  # 메인 창의 X 좌표
    root_y = app.winfo_y()  # 메인 창의 Y 좌표
    root_width = app.winfo_width()  # 메인 창의 너비
    root_height = app.winfo_height()  # 메인 창의 높이

    # 팝업 창 위치 계산 (메인 창 중심)
    popup_x = root_x + (root_width // 2) - (popup_width // 2)
    popup_y = root_y + (root_height // 2) - (popup_height // 2)
    return popup_x, popup_y

# 팝업창 생성 함수
def open_popup():
    # 팝업 창 생성
    popup_width, popup_height = 250, 150
    popup_x, popup_y = get_popup_pos(popup_width, popup_height)
    
    popup = ctk.CTkToplevel(app)
    popup.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")
        
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
                
            popup_width, popup_height = 100, 50
            popup_x, popup_y = get_popup_pos(popup_width, popup_height)
            
            new_popup = ctk.CTkToplevel(app)
            new_popup.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")
            new_popup.title("")
            new_popup.grab_set()
            label = ctk.CTkLabel(new_popup, text="저장완료")
            label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        
    button0 = ctk.CTkButton(popup, text="저장하기", command=save_NID)
    button0.pack(padx=10, pady=10)

def open_my_pay_log():
    webbrowser.open("https://game.naver.com/profile#cash")
    
def compute_difference(num):
    # 입력된 숫자의 자리수 계산
    num_digits = max(5, len(str(num)))
    # 자리수보다 하나 큰 10의 거듭제곱 계산
    power_of_ten = 10 ** num_digits
    # 10의 거듭제곱에서 입력 숫자를 뺀 값 반환
    return power_of_ten - num

def display():
    total = 0
    row = 1
    header = [["총합"],["채팅", "유료 보이스", "영상", "미션", "미션 상금쌓기"], ["후원뱃지 기준", "유료 보이스", "다음 뱃지까지 남은 치즈"]][button5_state]
    for i, donation_type in enumerate(header):
        label = ctk.CTkLabel(scrollable_frame, text=donation_type, width=100, height=20)
        label.grid(row=0, column=i+1, padx=5, pady=5)  # 그리드 레이아웃으로 배치
        labels.append(label)
        
    if button5_state == 0:
        app.geometry("450x400")
        for channel_id, donation_data in sorted(total_pay_amount.items(), key= lambda item:sum(item[1].values()), reverse=True):
            streamer_total = sum(donation_data.values())
            total += streamer_total
            url = "https://api.chzzk.naver.com/service/v1/channels/" + channel_id
            streamer_name = requests.get(url, headers=headers).json()["content"]["channelName"]
            label = ctk.CTkLabel(scrollable_frame, text=streamer_name, width=100, height=20)
            label.grid(row=row, column=0, padx=5, pady=5)  # 그리드 레이아웃으로 배치
            labels.append(label)
            label = ctk.CTkLabel(scrollable_frame, text=streamer_total, width=100, height=20)
            label.grid(row=row, column=1, padx=5, pady=5)  # 그리드 레이아웃으로 배치
            labels.append(label)
            row += 1
            
    elif button5_state == 1:
        app.geometry("900x400")
        for channel_id, donation_data in sorted(total_pay_amount.items(), key= lambda item:sum(item[1].values()), reverse=True):
            streamer_total = sum(donation_data.values())
            total += streamer_total
            url = "https://api.chzzk.naver.com/service/v1/channels/" + channel_id
            streamer_name = requests.get(url, headers=headers).json()["content"]["channelName"]
            label = ctk.CTkLabel(scrollable_frame, text=streamer_name, width=100, height=20)
            label.grid(row=row, column=0, padx=5, pady=5)  # 그리드 레이아웃으로 배치
            labels.append(label)
            column = 1
            for donation_type in donation_data:
                label = ctk.CTkLabel(scrollable_frame, text=donation_data[donation_type], width=100, height=20)
                label.grid(row=row, column=column, padx=5, pady=5)  # 그리드 레이아웃으로 배치
                labels.append(label)
                column += 1
            row += 1
    else:
        app.geometry("700x400")
        for channel_id, donation_data in sorted(total_pay_amount.items(), key= lambda item:sum(item[1].values()), reverse=True):
            streamer_total = sum(donation_data.values())
            total += streamer_total
            url = "https://api.chzzk.naver.com/service/v1/channels/" + channel_id
            streamer_name = requests.get(url, headers=headers).json()["content"]["channelName"]
            label = ctk.CTkLabel(scrollable_frame, text=streamer_name, width=100, height=20)
            label.grid(row=row, column=0, padx=5, pady=5)  # 그리드 레이아웃으로 배치
            labels.append(label)
            badge_base = streamer_total-donation_data["TTS"]
            label = ctk.CTkLabel(scrollable_frame, text=badge_base, width=100, height=20)
            label.grid(row=row, column=1, padx=5, pady=5)  # 그리드 레이아웃으로 배치
            labels.append(label)
            label = ctk.CTkLabel(scrollable_frame, text=donation_data["TTS"], width=100, height=20)
            label.grid(row=row, column=2, padx=5, pady=5)  # 그리드 레이아웃으로 배치
            labels.append(label)
            label = ctk.CTkLabel(scrollable_frame, text=compute_difference(badge_base), text_color="red", width=100, height=20)
            label.grid(row=row, column=3, padx=5, pady=5)  # 그리드 레이아웃으로 배치
            labels.append(label)
            row += 1
    label = ctk.CTkLabel(scrollable_frame, text="총합: %d"%total, width=100, height=20)
    label.grid(row=row+2, column=0, padx=5, pady=5)  # 그리드 레이아웃으로 배치
    labels.append(label)

def calculate():
    button2.configure(state="disabled")
    button4.configure(state="disabled")
    button5.configure(state="disabled")
    NID_AUT, NID_SES = get_NID()
    cookies = {"NID_AUT":NID_AUT, "NID_SES":NID_SES}
    
    try:
        content = get_content(0, 2023, cookies)
    except:
        popup_width, popup_height = 200, 50
        popup_x, popup_y = get_popup_pos(popup_width, popup_height)
        
        new_popup = ctk.CTkToplevel(app)
        new_popup.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")
        new_popup.title("오류!")
        new_popup.grab_set()
        label = ctk.CTkLabel(new_popup, text="NID가 없거나 잘못되었습니다.")
        label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        button2.configure(state="normal")
        button4.configure(state="normal")
        button5.configure(state="normal")
        return
    
    for i in labels:
        i.destroy()  # 라벨 파괴
    labels.clear()  # 리스트 비우기
    
    global total_pay_amount
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
                donation_type = data["donationType"]
                
                if not channel_id in total_pay_amount:
                    total_pay_amount[channel_id] = {"CHAT": 0, "TTS": 0, "VIDEO": 0, "MISSION": 0, "MISSION_PARTICIPATION": 0}
                total_pay_amount[channel_id][donation_type] += pay_amount
                
            label.destroy()
    display()
    button2.configure(state="normal")
    button4.configure(state="normal")
    button5.configure(state="normal")
    
def start_calculate():
    thread = threading.Thread(target=calculate)  # 작업을 백그라운드 스레드에서 실행
    thread.start()

def change_mode():
    global button5_state
    button5_state = (button5_state+1)%3
    if button5_state == 0:
        button5.configure(text="간단히 보기", fg_color="#1fa372", hover_color="#14714f")
    elif button5_state == 1:
        button5.configure(text="자세히 보기", fg_color="#a31f5f", hover_color="#711441")
    else:
        button5.configure(text="후원뱃지 기준", fg_color="#4f1fa3", hover_color="#361471")
    for i in labels:
        i.destroy()  # 라벨 파괴
    labels.clear()  # 리스트 비우기
    if not total_pay_amount == {}:
        display()
        
# CustomTkinter 초기화
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# 메인 창 생성
app = ctk.CTk()
app.geometry("450x400")
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

button5 = ctk.CTkButton(menu_bar, text="간단히 보기", command=change_mode, fg_color="#1fa372", hover_color="#14714f")
button5.pack(pady=10, padx=10, fill="x")
button5_state = 0

labels = []
total_pay_amount = {}

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
