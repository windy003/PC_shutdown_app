import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import time

class ShutdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("定时关机程序:2025.5.26-03")
        
        # 设置窗口最大化而不是全屏
        # self.root.attributes('-fullscreen', True)  # 注释掉全屏设置
        self.root.state('zoomed')  # 使用zoomed状态代替，这样会保留标题栏和任务栏
        
        # 允许调整窗口大小
        # self.root.geometry("400x200")
        self.root.resizable(True, True)
        
        # 设置背景颜色为红色
        self.root.configure(bg="red")
        
        self.is_timer_running = False
        self.remaining_time = 0
        self.timer_thread = None
        
        # 创建界面元素
        tk.Label(root, text="请输入关机倒计时(分钟):", font=("微软雅黑", 18), bg="red", fg="white").pack(pady=20)
        
        # 输入框和标签
        self.input_frame = tk.Frame(root, bg="red")
        self.input_frame.pack(pady=10)
        
        self.minutes_entry = tk.Entry(self.input_frame, width=10, font=("微软雅黑", 18))
        self.minutes_entry.pack(side=tk.LEFT, padx=5)
        self.minutes_entry.insert(0, "30")  # 设置默认值为30分钟
        
        # 设置输入框的快捷键
        # self.minutes_entry.focus_set()  # 注释掉这行，不再默认聚焦在输入框
        root.bind("<Alt-m>", lambda e: self.minutes_entry.focus_set())
        
        # 按钮框架
        self.button_frame = tk.Frame(root, bg="red")
        self.button_frame.pack(pady=20)
        
        # 开始按钮
        self.start_button = tk.Button(self.button_frame, text="开始(S)", command=self.start_timer, 
                                     font=("微软雅黑", 14), width=10, height=2)
        self.start_button.pack(side=tk.LEFT, padx=20)
        root.bind("<Alt-s>", lambda e: self.start_timer())
        root.bind("<Return>", lambda e: self.start_timer())  # 添加回车键绑定
        root.bind("<space>", lambda e: self.start_timer())   # 添加空格键绑定
        
        # 取消按钮
        self.cancel_button = tk.Button(self.button_frame, text="取消(C)", command=self.cancel_timer, 
                                      state=tk.DISABLED, font=("微软雅黑", 14), width=10, height=2)
        self.cancel_button.pack(side=tk.LEFT, padx=20)
        root.bind("<Alt-c>", lambda e: self.cancel_timer())
        
        # 退出按钮
        self.exit_button = tk.Button(self.button_frame, text="退出(Q)", command=self.quit_app,
                                    font=("微软雅黑", 14), width=10, height=2)
        self.exit_button.pack(side=tk.LEFT, padx=20)
        root.bind("<Alt-q>", lambda e: self.quit_app())
        root.bind("<Escape>", lambda e: self.quit_app())  # 添加ESC键退出
        
        # 倒计时标签
        self.time_label = tk.Label(root, text="倒计时: 未开始", font=("微软雅黑", 30), bg="red", fg="white")
        self.time_label.pack(pady=30)

        # 设置窗口关闭时的操作
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        
        # 程序启动时聚焦在开始按钮上
        self.start_button.focus_set()
    
    def start_timer(self):
        # 如果计时器已经在运行，则不做任何操作
        if self.is_timer_running:
            return
        
        try:
            minutes = int(self.minutes_entry.get())
            if minutes <= 0:
                messagebox.showerror("错误", "请输入大于0的分钟数")
                return
        except ValueError:
            messagebox.showerror("错误", "请输入有效的分钟数")
            return
        
        self.remaining_time = minutes * 60
        self.is_timer_running = True
        
        # 设置Windows关机命令
        subprocess.run(f"shutdown /s /t {self.remaining_time}", shell=True)
        
        # 更新界面状态
        self.start_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        self.minutes_entry.config(state=tk.DISABLED)
        
        # 启动倒计时线程
        self.timer_thread = threading.Thread(target=self.update_timer)
        self.timer_thread.daemon = True
        self.timer_thread.start()
    
    def update_timer(self):
        while self.remaining_time > 0 and self.is_timer_running:
            # 计算时分秒
            minutes, seconds = divmod(self.remaining_time, 60)
            hours, minutes = divmod(minutes, 60)
            
            # 更新标签
            time_str = f"倒计时: {hours:02d}:{minutes:02d}:{seconds:02d}"
            self.time_label.config(text=time_str)
            
            time.sleep(1)
            self.remaining_time -= 1
        
        # 如果计时器已经完成但不是被取消的
        if self.remaining_time <= 0 and self.is_timer_running:
            self.time_label.config(text="计算机即将关闭...")
    
    def cancel_timer(self):
        if not self.is_timer_running:
            return
        
        # 取消Windows关机命令
        subprocess.run("shutdown /a", shell=True)
        
        self.is_timer_running = False
        self.time_label.config(text="倒计时: 已取消")
        
        # 恢复界面状态
        self.start_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
        self.minutes_entry.config(state=tk.NORMAL)
    
    def quit_app(self):
        # 如果计时器正在运行，先取消它
        if self.is_timer_running:
            self.cancel_timer()
        
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ShutdownTimer(root)
    root.mainloop()
