import tkinter as tk
from tkinter import ttk
import threading
import winsound
import time

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x350")
        self.root.title("niggggg")

        self.timer_running = False
        self.timer_time_left = 0
        self.timer_after_id = None

        self.stopwatch_running = False
        self.stopwatch_time_left = 0
        self.stopwatch_after_id = None

        self.global_message = tk.Label(root, text="", font=("Arial", 16, "bold"), fg="red")
        self.global_message.pack(pady=10)

        style = ttk.Style()
        style.configure('TNotebook.Tab', width=200, anchor='center', padding=[0, 5])

        self.tab_control = ttk.Notebook(root, style='TNotebook')
        self.timer_tab = ttk.Frame(self.tab_control)
        self.stopwatch_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.timer_tab, text="Таймер")
        self.tab_control.add(self.stopwatch_tab, text="Секундомер")
        self.tab_control.pack(expand=1, fill="both")

        self.create_timer_tab()
        self.create_stopwatch_tab()

    def create_timer_tab(self):
        self.timer_label = tk.Label(self.timer_tab, text="00:00:00", font=("Arial", 48))
        self.timer_label.pack(pady=20)

        self.timer_entry = tk.Entry(self.timer_tab, font=("Arial", 16))
        self.timer_entry.pack(pady=10)

        tk.Button(self.timer_tab, text="Старт", font=("Arial", 12), command=self.start_timer).pack(pady=5)
        tk.Button(self.timer_tab, text="Сброс", font=("Arial", 12), command=self.stop_timer).pack(pady=5)

    def create_stopwatch_tab(self):
        self.stopwatch_label = tk.Label(self.stopwatch_tab, text="00:00:00", font=("Arial", 48))
        self.stopwatch_label.pack(pady=20)

        tk.Button(self.stopwatch_tab, text="Старт", font=("Arial", 12), command=self.start_stopwatch).pack(pady=5)
        tk.Button(self.stopwatch_tab, text="Пауза", font=("Arial", 12), command=self.pause_stopwatch).pack(pady=5)
        tk.Button(self.stopwatch_tab, text="Сброс", font=("Arial", 12), command=self.stop_stopwatch).pack(pady=5)

    def update_timer(self):
        if self.timer_running and self.timer_time_left >= 0:
            hours, remainder = divmod(self.timer_time_left, 3600)
            mins, secs = divmod(remainder, 60)
            self.timer_label.config(text=f"{hours:02}:{mins:02}:{secs:02}")
            self.timer_time_left -= 1
            self.timer_after_id = self.root.after(1000, self.update_timer)
        elif self.timer_time_left < 0:
            self.timer_running = False
            self.timer_after_id = None
            threading.Thread(target=self.play_alarm).start()

    def start_timer(self):
        self.stop_timer()
        entry_text = self.timer_entry.get()
        try:
            self.timer_time_left = int(entry_text)
        except:
            self.global_message.config(text="Введите число секунд!")
            return
        self.timer_entry.delete(0, tk.END)
        self.global_message.config(text="")
        self.timer_running = True
        self.update_timer()

    def stop_timer(self):
        if self.timer_after_id:
            self.root.after_cancel(self.timer_after_id)
            self.timer_after_id = None
        self.timer_running = False
        self.timer_time_left = 0
        self.timer_label.config(text="00:00:00")

    def update_stopwatch(self):
        if self.stopwatch_running:
            self.stopwatch_time_left += 1
            hours, remainder = divmod(self.stopwatch_time_left, 3600)
            mins, secs = divmod(remainder, 60)
            self.stopwatch_label.config(text=f"{hours:02}:{mins:02}:{secs:02}")
            self.stopwatch_after_id = self.root.after(1000, self.update_stopwatch)

    def start_stopwatch(self):
        if not self.stopwatch_running:
            self.stopwatch_running = True
            self.update_stopwatch()

    def pause_stopwatch(self):
        if self.stopwatch_after_id:
            self.root.after_cancel(self.stopwatch_after_id)
            self.stopwatch_after_id = None
        self.stopwatch_running = False

    def stop_stopwatch(self):
        self.pause_stopwatch()
        self.stopwatch_time_left = 0
        self.stopwatch_label.config(text="00:00:00")

    def play_alarm(self):
        def blink_message():
            for _ in range(5):  # 5 раз мигать и пищать
                self.global_message.config(text="Время вышло!")
                winsound.Beep(1000, 1000)  # частота 1000 Гц, длительность 1 сек
                time.sleep(0.3)
                self.global_message.config(text="")
                time.sleep(0.2)
            self.global_message.config(text="")  # убрать текст после завершения

        threading.Thread(target=blink_message).start()

root = tk.Tk()
TimerApp(root)
root.mainloop()