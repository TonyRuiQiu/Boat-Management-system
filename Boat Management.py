import tkinter as tk
from tkinter.simpledialog import askstring
from socket import *
import time
from tkinter import ttk

state = 0  # 是否登录 0--未登录
boat_chosed = -1  # 目前被选择的船
boat_Buttons = [] # 存放所有的boat label
boat_data = [[0,0,0,"unknown","unknown"] for x in range(0,10)]  # [船的状态，起始时间，结束时间，顾客名，顾客ID]; 船的状态  0--可用  1--占用
detail_data = []  # 存放每条租赁记录
renting_Num = 0  # 租赁次数
total_renting_time = 0  # 总租赁时间
max_renting_time_AM = 0  # 上午最长租赁时间
max_renting_time_PM = 0  # 下午最长租赁时间
boat_communication = [0 for x in range(0,10)]  # 记录各船的通讯状况


# 被调用的相关函数
# 登录等出
def logfunc(x):
    global state
    # 登录
    if textvar1.get() == "Log In":
        # 询问密码
        ID = askstring("Log In", "Password: ")
        print(ID)
        if ID != "20201001":
            tk.messagebox.showerror(title="Info", message="The password is not correct!")
            return
        # 更改头像
        portrait_Label.configure(image = portrait_2)
        # 更改按钮文字
        textvar1.set("Log Out")
        # 更改用户名
        textvar2.set(" MANAGER ")
        # 更改状态
        state = 1
        # 告知登录成功
        tk.messagebox.showinfo(title="Info", message="Log in successfully!")
    # 登出
    elif textvar1.get() == "Log Out":
        # 更改头像
        portrait_Label.configure(image = portrait_1)
        # 更改按钮文字
        textvar1.set("Log In")
        # 更改用户名
        textvar2.set("UNKNOWN")
        # 更改状态
        state = 0

def detailInfoFunc():
    print("====In detail info====")
    # 创建子窗口
    if state == 1:
        newWin1 = tk.Toplevel()
        newWin1.geometry("850x400")
        newWin1.title("Detail Information")
        # 创建表格
        table = ttk.Treeview(newWin1)
        table["columns"] = ("Start Time", "End Time", "Customer Name", "Customer ID")
        table.column("Start Time", width=200)  # #设置列
        table.column("End Time", width=200)
        table.column("Customer Name", width=100)
        table.column("Customer ID", width=100)
        table.heading("Start Time", text="Start Time")  # #设置显示的表头名
        table.heading("End Time", text="End Time")
        table.heading("Customer Name", text="Customer Name")
        table.heading("Customer ID", text="Customer ID")
        # 插入数据
        for record_num in range(len(detail_data)):
            table.insert("", record_num, text="record"+str(record_num+1), values=(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(detail_data[record_num][0])), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(detail_data[record_num][1])), detail_data[record_num][2], detail_data[record_num][3]))

        table.place(relx=0, rely=0, relwidth=0.97, relheight=1)

        VScroll1 = tk.Scrollbar(newWin1, orient='vertical', command=table.yview)
        VScroll1.place(relx=0.97, rely=0, relwidth=0.023, relheight=1)
        # 给treeview添加配置
        table.configure(yscrollcommand=VScroll1.set)

        newWin1.mainloop()
    else:
        tk.messagebox.showinfo(title="Info", message="Please log in first!")

def setBoatNum(x):
    if state == 1:  # 已登录
        global boat_chosed
        boat_chosed = x
        textvar3.set("The boat you choose is # " + str(x))
    else:
        tk.messagebox.showinfo(title="Info", message="Please log in first!")

def start():
    print("=====In start=====")
    if state == 1:  # 如果登录了
        if boat_data[boat_chosed-1][0] == 0:  # 如果船没被占用
            # 更改船图标
            boat_Buttons[boat_chosed-1].configure(image = occupied)
            # 更改船相关信息
            boat_data[boat_chosed-1][0] = 1  # 船被占用-1
            boat_data[boat_chosed-1][1] = time.time()  # 获取起始时间
            boat_data[boat_chosed-1][3] = name_input.get()  # 获取用户姓名
            boat_data[boat_chosed-1][4] = ID_input.get()  # 获取用户ID
            print(boat_data)
        else:  # 如果船被占用
            tk.messagebox.showinfo(title="Info", message="Sorry, this boat is already occupied!")
    else:
        tk.messagebox.showinfo(title="Info", message="Please log in first!")


def end():
    print("=====In end=====")
    if state == 1:  # 如果登录了
        if boat_data[boat_chosed-1][0] == 1:  # 如果船被占用
            # 更改船图标
            boat_Buttons[boat_chosed-1].configure(image = available)
            # 获取结束时间
            boat_data[boat_chosed-1][2] = time.time()
            print(boat_data)
            # 计算相关数据
            global renting_Num
            global total_renting_time
            global max_renting_time_AM
            global max_renting_time_PM

            renting_Num = renting_Num + 1
            temp_time = boat_data[boat_chosed-1][2] - boat_data[boat_chosed-1][1]
            total_renting_time = total_renting_time + temp_time
            if time.localtime(boat_data[boat_chosed-1][2]).tm_hour < 12:  # 上午
                if max_renting_time_AM < temp_time:
                    max_renting_time_AM =  temp_time
            else:
                if max_renting_time_PM < temp_time:
                    max_renting_time_PM = temp_time
            # 更新展示数据
            textvar_info1.set("Renting Number: " + str(renting_Num)+'  ')
            textvar_info2.set("Average Renting Time: " + str(round(total_renting_time/renting_Num/60, 2))+'  ')
            textvar_info3.set("Longest Renting Time: " + str(round((max(max_renting_time_AM, max_renting_time_PM))/60, 2))+'  ')
            textvar_info4.set("Longest Renting Time(AM): " + str(round(max_renting_time_AM/60, 2))+'  ')
            textvar_info5.set("Longest Renting Time(PM): " + str(round(max_renting_time_PM/60, 2))+'  ')

            # 存储记录
            detail_data.append(boat_data[boat_chosed-1][1:])
            print("detail data:\n", detail_data)

            # 改变船的状态为可用
            boat_data[boat_chosed - 1][0] = 0
        else:  # 如果船没被占用
            tk.messagebox.showinfo(title="Info", message="Sorry, this boat is not occupied. Therefore, it can't be ended!")
    else:
        tk.messagebox.showinfo(title="Info", message="Please log in first!")



# 主体窗口
# 根窗口
root = tk.Tk()
root.geometry("900x600")
root.title("Boat Management System")

# 通讯
def loopAction():
    print("==========In communication==========")
    for communication_num in range(10):
        if boat_data[communication_num][0] == 1:
            try:
                serverName = '127.0.0.1'
                serverPort = 12000
                clientSocket = socket(AF_INET, SOCK_STREAM)
                # 与服务器建立连接
                clientSocket.connect((serverName, serverPort))
                # 组装要传输的信息
                trans_info = str(communication_num+1) + '*' + str(1)  # 船号码 + * + 1; 代码1表示询问是否通讯良好
                clientSocket.send(trans_info.encode())
                # 得到服务器的结果
                recive_info = clientSocket.recv(1024).decode()
                print('服务器返回结果：', recive_info)
                if recive_info.split('*')[1] != '1-ok':
                    tk.messagebox.showinfo(title="Info", message="Communication error!")
                clientSocket.close()
                boat_communication[communication_num] = 0
                print("\n")
            except Exception:
                print("[failed] boat num: ", communication_num+1)
                boat_communication[communication_num] = boat_communication[communication_num] + 1
                if boat_communication[communication_num] >= 3:
                    # 消除船对应的数据
                    boat_data[communication_num] = [0,0,0,"unknown","unknown"]
                    # 图标恢复
                    boat_Buttons[communication_num].configure(image = available)
                    tk.messagebox.showinfo(title="Info", message="Boat #"+str(communication_num+1)+" is lost!")


    print("========End of communication========")
    root.after(5000, loopAction)

loopAction()

# 左侧边栏背景
canvas1 = tk.Canvas(root, bg='#a2d2fa', height=600, width=200)
canvas1.place(x=0, y=0)

# 用户头像
portrait_1 = tk.PhotoImage(file = "elements/user.png")
portrait_2 = tk.PhotoImage(file="elements/administrator.png")
portrait_Label = tk.Label(root, image = portrait_1)
portrait_Label.place(x=52, y=50)

# 用户名
textvar2 = tk.StringVar()
textvar2.set("UNKNOWN")
name_Label = tk.Label(root, textvariable = textvar2,font=('黑体',18), bg='#a2d2fa')
name_Label.place(x=50, y=170)

# 登录登出按钮
textvar1 = tk.StringVar()
textvar1.set("Log In")
log_button = tk.Button(root, textvariable=textvar1, command=lambda:logfunc(1))
log_button.place(x=30, y=500, width=140, height=30)

# 细节信息按钮
info_button = tk.Button(root, text="Detail Info", command=lambda:detailInfoFunc())
info_button.place(x=30, y=450, width=140, height=30)

# 操作面板背景
canvas2 = tk.Canvas(root, bg='#2699FB', height=300, width=600)
canvas2.place(x=250, y=20)

# 顾客信息输入
cus_name_label = tk.Label(root, text="Customer Name: ",font=('黑体',14), fg = "white", bg='#2699FB')
cus_name_label.place(x=300, y=70)
name_input = tk.Entry(root,font=('黑体',18))
name_input.place(x=300, y=100, width=180, height=40)

cus_ID_label = tk.Label(root, text="Customer ID: ",font=('黑体',14), fg = "white", bg='#2699FB')
cus_ID_label.place(x=300, y=150)
ID_input = tk.Entry(root,font=('黑体',18))
ID_input.place(x=300, y=180, width=180, height=40)

# 船列表
subtitle1_label = tk.Label(root, text="Boat List: ",font=('黑体',18), fg = "white", bg='#2699FB')
subtitle1_label.place(x=550, y=50)

available = tk.PhotoImage(file = "elements/available.png")
occupied = tk.PhotoImage(file="elements/occupied.png")

boat_Button_1 = tk.Button(root, image = available, command=lambda:setBoatNum(1))
boat_Button_1.place(x=550, y=90)
boat_Buttons.append(boat_Button_1)

boat_Button_2 = tk.Button(root, image = available, command=lambda:setBoatNum(2))
boat_Button_2.place(x=600, y=90)
boat_Buttons.append(boat_Button_2)

boat_Button_3 = tk.Button(root, image = available, command=lambda:setBoatNum(3))
boat_Button_3.place(x=650, y=90)
boat_Buttons.append(boat_Button_3)

boat_Button_4 = tk.Button(root, image = available, command=lambda:setBoatNum(4))
boat_Button_4.place(x=700, y=90)
boat_Buttons.append(boat_Button_4)

boat_Button_5 = tk.Button(root, image = available, command=lambda:setBoatNum(5))
boat_Button_5.place(x=750, y=90)
boat_Buttons.append(boat_Button_5)

boat_Button_6 = tk.Button(root, image = available, command=lambda:setBoatNum(6))
boat_Button_6.place(x=550, y=160)
boat_Buttons.append(boat_Button_6)

boat_Button_7 = tk.Button(root, image = available, command=lambda:setBoatNum(7))
boat_Button_7.place(x=600, y=160)
boat_Buttons.append(boat_Button_7)

boat_Button_8 = tk.Button(root, image = available, command=lambda:setBoatNum(8))
boat_Button_8.place(x=650, y=160)
boat_Buttons.append(boat_Button_8)

boat_Button_9 = tk.Button(root, image = available, command=lambda:setBoatNum(9))
boat_Button_9.place(x=700, y=160)
boat_Buttons.append(boat_Button_9)

boat_Button_10 = tk.Button(root, image = available, command=lambda:setBoatNum(10))
boat_Button_10.place(x=750, y=160)
boat_Buttons.append(boat_Button_10)

textvar3 = tk.StringVar()
textvar3.set("The boat you choose is #")
BoatNum_label = tk.Label(root, textvariable = textvar3,font=('黑体',16), fg = "white", bg='#2699FB')
BoatNum_label.place(x=550, y=220)

# Start & End
start_Button = tk.Button(root, text="START", command=start)
start_Button.place(x=350, y=265, width=170, height=35)

end_Button = tk.Button(root, text="END", command=end)
end_Button.place(x=580, y=265, width=170, height=35)

# Information
# 信息面板背景
canvas2 = tk.Canvas(root, bg='#2699FB', height=230, width=600)
canvas2.place(x=250, y=340)

subtitle2_label = tk.Label(root, text="Information",font=('黑体',22), fg = "white", bg='#2699FB')
subtitle2_label.place(x=490, y=365)

textvar_info1 = tk.StringVar()
textvar_info1.set("Renting Number: 0")
info_label_1 = tk.Label(root, textvariable = textvar_info1,font=('黑体',18), fg = "white", bg='#2699FB')
info_label_1.place(x=280, y=410)

textvar_info2 = tk.StringVar()
textvar_info2.set("Average Renting Time: 0")
info_label_2 = tk.Label(root, textvariable = textvar_info2,font=('黑体',18), fg = "white", bg='#2699FB')
info_label_2.place(x=280, y=460)

textvar_info3 = tk.StringVar()
textvar_info3.set("Longest Renting Time: 0")
info_label_3 = tk.Label(root, textvariable = textvar_info3,font=('黑体',18), fg = "white", bg='#2699FB')
info_label_3.place(x=280, y=510)

textvar_info4 = tk.StringVar()
textvar_info4.set("Longest Renting Time(AM): 0")
info_label_4 = tk.Label(root, textvariable = textvar_info4,font=('黑体',18), fg = "white", bg='#2699FB')
info_label_4.place(x=560, y=410)

textvar_info5 = tk.StringVar()
textvar_info5.set("Longest Renting Time(PM): 0")
info_label_5 = tk.Label(root, textvariable = textvar_info5,font=('黑体',18), fg = "white", bg='#2699FB')
info_label_5.place(x=560, y=460)



root.mainloop()