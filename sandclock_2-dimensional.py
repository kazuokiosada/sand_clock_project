import tkinter as tk
import time
from math import *
import random

#時間設定
cycle=1.0 #周期（分）
click=0.3 #更新間隔（秒）
cn=1/click ###1秒間のクリック数
time_full = 60*cycle  # 最終時間（秒）
tcn=time_full*cn ###全クリック数
time_elapsed=0.0 #経過時間
is_reversed = False  # 時計が反転しているかどうか
#print("after update_sand")
#キャンバス寸法
H=200#キャンバス幅
V=500#キャンバス高
#砂時計寸法
φ=radians(37)#安息角
Ψ=radians(50)#漏斗角
a=H/5#2a=横幅
b=a
c=a*tan(Ψ)
d=a*(tan(Ψ) - tan(φ))/2
e=3*a*tan(φ)
f=3
g=d+e
h=a*tan(φ)
k=b+d
X0=H/2 - a
Y0=V/2 - c - b - g
LY=(0,0)
###下の砂の頂点
#座標
M=(X0,Y0)
A=(X0,Y0+g)
B=(X0,Y0+g+b)
C=(X0+a,Y0+g+b+c)
F=(X0+a,Y0+g+b+c+f)
G=(X0,Y0+g+b+2*c+f)
O=(X0,Y0+g+b+2*c+f+e)
K=(X0,Y0+g+b+2*c+f+e+k)
X=(X0+a,Y0+g+b+2*c+f+e+k)
L=(X0+2*a,Y0+g+b+2*c+f+e+k)
Q=(X0+2*a,Y0+g+b+2*c+f+e)
J=(X0+2*a,Y0+g+b+2*c+f)
D=(X0+2*a,Y0+g+b)
E=(X0+2*a,Y0+g)
N=(X0+2*a,Y0)
Z=(X0+a,Y0+g)
#総面積など
S3=2*a*b+a**2*tan(Ψ)
S1=a**2*tan(φ)
S2=2*a*b+a**2*tan(φ)
#落ちる砂の量
p2=S3/tcn ###1回ごとに落ちる量
print("p2=S3/tcn:",p2,S3,tcn)
#チェックポイント
t3=S3/p2*click ###=tcn*click=time_full*cn*click=60*cycle*cn*click=60*cycle
t1=S1/S3*t3
t2=S2/S3*t3
t4=t3
##print("t1=a**2*tan(φ)/p2*click",t1,a,a**2*tan(φ),p2,a**2*tan(φ)/p2)
print("t1 t2 t3=",t1,t2,t3)

def init(master):
        #外形表示
        draw_clock()
        ###
        update_sand(master)

def draw_clock():
        clock_shape=[M,A,B,C,F,G,O,K,X,L,Q,J,F,C,D,E,N]
        canvas.create_polygon(clock_shape, outline="green",tags="clock",fill="white",width=2)
        ###print("end of draw_clock")
def update_sand(master):
        global time_elapsed
        ##canvas.delete("all")
        #外形表示
        ##draw_clock()
        if time_full >= time_elapsed:
            # 砂時計の砂の形を計算
            #上の砂
            upper_sand_shape=create_upper_sand_shape()
            # クリア、描画
            canvas.delete("uppersand")
            canvas.create_polygon(upper_sand_shape, fill="violet", tags="uppersand")
            # 落ちる砂、下の砂
            if time_full > time_elapsed:
              #下の砂
              lower_sand_shape=create_lower_sand_shape()
              canvas.delete("lowersand")
              canvas.create_polygon(lower_sand_shape, fill="red", tags="lowersand")
              #落ちる砂
              dropping_sand_shape=create_dropping_sand_shape()
              canvas.delete("dropsand")
              canvas.create_line(dropping_sand_shape, fill="violet", width=1,tags="dropsand")
            time_elapsed += click
            ##print("time_full time_elapsed *p2=",time_full,time_elapsed,time_elapsed*p2)
            master.after(int(1000*click), lambda: update_sand(master))  # click秒後に再度実行
        else:
            ###落ちる砂を消去
            canvas.delete("dropsand","upperrsand")
            ###canvas.delete("dropsand","upperrsand")
            ###time.sleep(5)
            # 時間切れ
            """
            ###
            time_full = 60*cycle/click  # 最終時間（秒）
            time_elapsed=0 #経過時間
            update_sand()  # 再度計測開始
            """

def create_upper_sand_shape():
            if(time_elapsed==0):
                return [A,B,C,D,E]
            elif(time_elapsed<t1):
                ##print("time_elapsed<t1:",time_elapsed,t1)
                ###time_elapsed*cn:砂が落ちた回数
                ###p2*time_elapsed*cn：砂が落ちた量
                x=sqrt(p2*time_elapsed*cn/tan(φ))
                y=sqrt(p2*time_elapsed*cn*tan(φ))
                ##print("a,x,y,x*y,S1,time_elapsed,p2,p2*time_elapsed*cn=",a,x,y,x*y,S1,time_elapsed,p2,time_elapsed*p2*cn)
                return [(Z[0]-x,Z[1]),(Z[0]+random.uniform(-1.0, 1.0),Z[1]+y),(Z[0]+x,Z[1]),E,D,C,B,A]
            elif(time_elapsed<t2):
                ##print("time_elapsed<t2:",time_elapsed,t2)
                y=(p2*time_elapsed*cn+a**2*tan(φ))/(2*a)
                return [(X0,Z[1]+y-a*tan(φ)),(Z[0]+random.uniform(-1.0, 1.0),Z[1]+y),(N[0],Z[1]+y-a*tan(φ)),D,C,B]
            elif(time_elapsed<t3):
                ##print("time_elapsed<t3:",time_elapsed,t3)
                y=b+c-sqrt((2*a*b+a**2*tan(Ψ)-p2*time_elapsed*cn)*(tan(Ψ)-tan(φ)))
                u=(b+c-y)/(tan(Ψ)-tan(φ))
                v=u*tan(φ)
                return [(Z[0]-u,Z[1]+y-v),(Z[0],Z[1]+y),(Z[0]+u,Z[1]+y-v),C]
            else:
                return [C,C,C]
def create_dropping_sand_shape():
        return [C,(LY[0]+random.uniform(-1.0, 1.0),LY[1])]

def create_lower_sand_shape():
        global LY
        if time_elapsed<t1:
            x=sqrt(p2*time_elapsed*cn/tan(φ))
            y=sqrt(p2*time_elapsed*cn*tan(φ))
            LY=(X[0],X[1]-y)
            return [(X[0]-x,X[1]),(X[0],X[1]-y),(X[0]+x,X[1])]
        else:
            y=(p2*time_elapsed*cn+a**2*tan(φ))/(2*a)
            LY=(X[0],X[1]-y)
            return [(L[0],L[1]-y+a*tan(φ)),(X[0]+random.uniform(-1.0, 1.0),X[1]-y),(K[0],K[1]-y+a*tan(φ)),K,L]
###設定
root = tk.Tk()
root.wm_attributes('-transparentcolor', "white")  # 白色を透過色に設定
root.config(bg='white')  # ウィンドウの背景色を白色に設定
###表示すべきもの
root.title("1分砂時計")
#
canvas = tk.Canvas(root, width=H, height=V, bg="white")
canvas.pack()
###sand_clock = SandClock(root)
init(root)
###ｳｨﾝﾄﾞｳを表示
root.mainloop()