import tkinter as tk
import time
from math import *
import random

class SandClock:
    def __init__(self, master):
        """
        self.master = master
        self.cycle = 1 #周期（分）
        self.time_left = 60*self.cycle # 初期時間（秒）
        self.canvas = tk.Canvas(master, width=200, height=300)        
        self.canvas.pack()
        """
        self.master = master
        master.title("1分砂時計")
        #時間設定
        self.cycle=0.5 #周期（分）
        self.click=1.0 #更新間隔（秒）
        #キャンバス寸法
        self.H=200#キャンバス幅
        self.V=500#キャンバス高
        self.canvas = tk.Canvas(master, width=self.H, height=self.V, bg="white")
        self.canvas.pack()
        #外形
        self.shape_clock()
        #外形表示
        self.draw_clock()
        ###
        self.time_full = 60*self.cycle/self.click  # 最終時間（秒）
        self.time_elapsed=0 #経過時間
        self.is_reversed = False  # 時計が反転しているかどうか
        #print("before update_sand")
        #self.update_sand()
        #print("after update_sand")
        """
        self.time_full = 60*self.cycle  # 最終時間（秒）
        self.time_elapsed=0 #経過時間
        self.is_reversed = False  # 時計が反転しているかどうか
        self.click = 1 # 追加：self.click を整数で初期化
        """
        self.update_sand()
    def shape_clock(self):
        #砂時計寸法
        self.φ=radians(37)#安息角
        self.Ψ=radians(50)#漏斗角
        self.a=self.H/5#2a=横幅
        self.b=self.a
        self.c=self.a*tan(self.Ψ)
        self.d=self.a*(tan(self.Ψ) - tan(self.φ))/2
        self.e=3*self.a*tan(self.φ)
        self.f=3
        self.g=self.d+self.e
        self.h=self.a*tan(self.φ)
        self.k=self.b+self.d
        self.X0=self.H/2 - self.a
        self.Y0=self.V/2 - self.c - self.b - self.g
        self.LY=0###下の砂の頂点
        #座標
        self.M=(self.X0,self.Y0)
        self.A=(self.X0,self.Y0+self.g)
        self.B=(self.X0,self.Y0+self.g+self.b)
        self.C=(self.X0+self.a,self.Y0+self.g+self.b+self.c)
        self.F=(self.X0+self.a,self.Y0+self.g+self.b+self.c+self.f)
        self.G=(self.X0,self.Y0+self.g+self.b+2*self.c+self.f)
        self.O=(self.X0,self.Y0+self.g+self.b+2*self.c+self.f+self.e)
        self.K=(self.X0,self.Y0+self.g+self.b+2*self.c+self.f+self.e+self.k)
        self.X=(self.X0+self.a,self.Y0+self.g+self.b+2*self.c+self.f+self.e+self.k)
        self.L=(self.X0+2*self.a,self.Y0+self.g+self.b+2*self.c+self.f+self.e+self.k)
        self.Q=(self.X0+2*self.a,self.Y0+self.g+self.b+2*self.c+self.f+self.e)
        self.J=(self.X0+2*self.a,self.Y0+self.g+self.b+2*self.c+self.f)
        self.D=(self.X0+2*self.a,self.Y0+self.g+self.b)
        self.E=(self.X0+2*self.a,self.Y0+self.g)
        self.N=(self.X0+2*self.a,self.Y0)
        self.Z=(self.X0+self.a,self.Y0+self.g)
        #総面積
        self.S3=2*self.a*self.b+self.a**2*tan(self.Ψ)
        #落ちる砂の量
        self.p2=self.S3/(self.cycle*60/self.click)
        #チェックポイント
        self.t1=self.a**2*tan(self.φ)/self.p2
        self.t2=(2*self.a*self.b+self.a**2*tan(self.φ))/self.p2
        self.t3=self.S3/self.p2
        self.t4=self.t3
        ###print("end of shape_clock")

    def draw_clock(self):
        clock_shape=[self.M,self.A,self.B,self.C,self.F,self.G,self.O,self.K,self.X,self.L,self.Q,self.J,self.F,self.C,self.D,self.E,self.N]
        self.canvas.create_polygon(clock_shape, outline="green",tags="clock",fill="white",width=2)
        ###print("end of draw_clock")
    def update_sand(self):
        ##self.canvas.delete("all")
        #外形表示
        ##self.draw_clock()
        """
        self.canvas.create_rectangle(50, 50, 150, 250, outline="black")
        height = 200 * (self.time_left / (60 * self.cycle))
        self.canvas.create_rectangle(50, 250 - height, 150, 250, fill="yellow")
        self.time_left -= 1
        if self.time_left >= 0:
            self.master.after(int(1000*self.click), self.update_sand) # 1秒後に再度実行
        else:
            self.time_left = 60 * self.cycle # 再度計測開始
            self.master.after(int(1000*self.click), self.update_sand)
            """
        if self.time_full >= self.time_elapsed:
            # 砂時計の砂の形を計算
            #上の砂
            upper_sand_shape=self.create_upper_sand_shape()
            # クリア、描画
            self.canvas.delete("uppersand")
            self.canvas.create_polygon(upper_sand_shape, fill="violet", tags="uppersand")
            # 落ちる砂、下の砂
            if self.time_full > self.time_elapsed:
              #下の砂
              lower_sand_shape=self.create_lower_sand_shape()
              self.canvas.delete("lowersand")
              self.canvas.create_polygon(lower_sand_shape, fill="red", tags="lowersand")
              #落ちる砂
              dropping_sand_shape=self.create_dropping_sand_shape()
              self.canvas.delete("dropsand")
              self.canvas.create_line(dropping_sand_shape, fill="blue", tags="dropsand")
            self.time_elapsed += self.click
            self.master.after(int(1000*self.click), self.update_sand)  # self.click秒後に再度実行
        else:
            ###落ちる砂を消去
            self.canvas.delete("dropsand","upperrsand")
            ###self.canvas.delete("dropsand","upperrsand")
            ###time.sleep(5)
            # 時間切れ
            """
            ###
            self.time_full = 60*self.cycle/self.click  # 最終時間（秒）
            self.time_elapsed=0 #経過時間
            self.update_sand()  # 再度計測開始
            """

    def create_upper_sand_shape(self):
            if(self.time_elapsed==0):
                return [self.A,self.B,self.C,self.D,self.E]
            elif(self.time_elapsed<self.t1):
                x=sqrt(self.p2*self.time_elapsed/tan(self.φ))
                y=sqrt(self.p2*self.time_elapsed*tan(self.φ))
                return [(self.Z[0]-x,self.Z[1]),(self.Z[0]+random.uniform(-1.0, 1.0),self.Z[1]+y),(self.Z[0]+x,self.Z[1]),self.E,self.D,self.C,self.B,self.A]
            elif(self.time_elapsed<self.t2):
                y=(self.p2*self.time_elapsed+self.a**2*tan(self.φ))/(2*self.a)
                return [(self.X0,self.Z[1]+y-self.a*tan(self.φ)),(self.Z[0]+random.uniform(-1.0, 1.0),self.Z[1]+y),(self.N[0],self.Z[1]+y-self.a*tan(self.φ)),self.D,self.C,self.B]
            elif(self.time_elapsed<self.t3):
                y=self.b+self.c-sqrt((2*self.a*self.b+self.a**2*tan(self.Ψ)-self.p2*self.time_elapsed)*(tan(self.Ψ)-tan(self.φ)))
                u=(self.b+self.c-y)/(tan(self.Ψ)-tan(self.φ))
                v=u*tan(self.φ)
                return [(self.Z[0]-u,self.Z[1]+y-v),(self.Z[0],self.Z[1]+y),(self.Z[0]+u,self.Z[1]+y-v),self.C]
            else:
                return [self.C,self.C,self.C]
    def create_dropping_sand_shape(self):
        return [self.C,(self.LY[0]+random.uniform(-1.0, 1.0),self.LY[1])]

    def create_lower_sand_shape(self):
        if self.time_elapsed<self.t1:
            x=sqrt(self.p2*self.time_elapsed/tan(self.φ))
            y=sqrt(self.p2*self.time_elapsed*tan(self.φ))
            self.LY=(self.X[0],self.X[1]-y)
            return [(self.X[0]-x,self.X[1]),(self.X[0],self.X[1]-y),(self.X[0]+x,self.X[1])]
        else:
            y=(self.p2*self.time_elapsed+self.a**2*tan(self.φ))/(2*self.a)
            self.LY=(self.X[0],self.X[1]-y)
            return [(self.L[0],self.L[1]-y+self.a*tan(self.φ)),(self.X[0]+random.uniform(-1.0, 1.0),self.X[1]-y),(self.K[0],self.K[1]-y+self.a*tan(self.φ)),self.K,self.L]

root = tk.Tk()
root.wm_attributes('-transparentcolor', "white")  # 白色を透過色に設定
root.config(bg='white')  # ウィンドウの背景色を白色に設定
sand_clock = SandClock(root)
root.mainloop()