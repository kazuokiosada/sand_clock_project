import tkinter as tk

class SandClock:
    def __init__(self, master):
        self.master = master
        self.cycle = 1 #周期（分）
        self.time_left = 60*self.cycle # 初期時間（秒）
        self.canvas = tk.Canvas(master, width=200, height=300)
        self.canvas.pack()
        self.click = 1 # 追加：self.click を整数で初期化
        self.update_sand()

    def update_sand(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(50, 50, 150, 250, outline="black")
        height = 200 * (self.time_left / (60 * self.cycle))
        self.canvas.create_rectangle(50, 250 - height, 150, 250, fill="yellow")
        self.time_left -= 1
        if self.time_left >= 0:
            self.master.after(int(1000*self.click), self.update_sand) # 1秒後に再度実行
        else:
            self.time_left = 60 * self.cycle # 再度計測開始
            self.master.after(int(1000*self.click), self.update_sand)

root = tk.Tk()
sand_clock = SandClock(root)
root.mainloop()