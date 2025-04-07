import tkinter as tk
import time
from math import *
import random
import ellipse as ec
import funnel_gradation_funs as fg

#時間設定
cycle=1 #周期（分）
click=0.1 #更新間隔（秒）
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
###楕円 長径、短径
aa=a
bb=aa*0.3
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
###砂の色
# グラデーションの色
color1 = (255, 0, 0)  # 鮮やかな赤
color2=(100,0,0)###暗い赤
###color3= '#%02x%02x%02x' % tuple(int((color1[i]+color2[i])/2) for i in range(3))
###color3='#%02x%02x%02x' % (200, 0, 0)###中間的な赤
###color3='#%02x%02x%02x' % tuple(int((color1[i]+color2[i])/2) for i in range(3)) ###中間的な赤
color3=(170,0,0)
Colors=(color1,color2,color3)

##########################################関数###############
def init(master,Colors):
        #外形表示
        draw_clock()
        ###
        update_sand(master,Colors)

def draw_clock():
        clock_shape=[M,A,B,C,F,G,O,K]
        ###,X,
        clock_shape.extend(ec.get_arc_of_eclipse(X[0],X[1],aa,bb,180,360,1))
        clock_shape.extend([L,Q,J,F,C,D,E,N])
        canvas.create_polygon(clock_shape, outline="lightgreen",fill="#ADD8E6",width=4,tags="clock")
        canvas.create_polygon(clock_shape, outline="lightgreen",fill="grey",width=4,tags="clock")
        ###print("end of draw_clock")
def update_sand(master,Colors):
        global time_elapsed
        ##canvas.delete("all")
        #外形表示
        ##draw_clock()
        if time_full >= time_elapsed:
            # 砂時計の砂の形を計算
            #上の砂
            ##描画
            draw_upper_sand(canvas,Colors)
            # 落ちる砂、下の砂
            if time_full > time_elapsed:
              #下の砂
              canvas.delete("lowersand")
              draw_lower_sand(canvas,Colors)
              #落ちる砂
              canvas.delete("dropsand")
              draw_dropping_sand(canvas,Colors)
            time_elapsed += click
            ##print("time_full time_elapsed *p2=",time_full,time_elapsed,time_elapsed*p2)
            master.after(int(1000*click), lambda: update_sand(master,Colors))  # click秒後に再度実行
        else:
            ###落ちる砂を消去
            canvas.delete("dropsand","uppersand")
            # 時間切れ
            """
            ###
            time_full = 60*cycle/click  # 最終時間（秒）
            time_elapsed=0 #経過時間
            update_sand()  # 再度計測開始
            """
def draw_upper_sand(canvas,Colors):
    color1=Colors[0]###鮮やか
    color2=Colors[1]###暗い
    color3=Colors[2]###中間色
    csteps=20
    hcolor3='#%02x%02x%02x' % color3
    ###tuple(int((color1[i]+color2[i])/2) for i in range(3)) ###中間的な赤

    tags="uppersand"    
    # クリア
    canvas.delete("uppersand")
    if(time_elapsed==0):
        ###return [A,B,C,D,E]        
        create_eclipse(canvas,Z,aa,bb,hcolor3,tags)
        ##draw_cylinder(canvas,Center,UpperOuterMaA,UpperOuterMiA,LowerOuterMaA,LowerOuterMiA,color1,color2)
        ###create_gradient_cylinder(canvas,cx,cy,cx2,cy2,a,b,color1, color2, csteps)
        fg.create_gradient_cylinder(canvas,Z[0],Z[1],Z[0],B[1],aa,bb,color1, color2, csteps,tags)
        ##draw_funnel(canvas,Center,LowerOuterMaA,LowerOuterMiA,color1,color2)
        ###create_gradient_funnel(canvas,cx,cy, a,b,upOrLow,q,color1, color2, csteps):
        fg.create_gradient_funnel(canvas,Z[0],B[1], aa,bb-1,"L",c-1,color1, color2, csteps,tags)
    elif(time_elapsed<=t1):
        x=sqrt(p2*time_elapsed*cn/tan(φ))
        y=sqrt(p2*time_elapsed*cn*tan(φ))
        ###return [(Z[0]-x,Z[1]),(Z[0]+random.uniform(-1.0, 1.0),Z[1]+y),(Z[0]+x,Z[1]),E,D,C,B,A]
        create_eclipse(canvas,Z,aa,bb,hcolor3,tags)###上部円盤
        ###draw_hole(canvas,Center,MajorAxis,MinorAxix,Q,color1,color2)
        ###create_gradient_funnel(canvas,cx,cy, a,b,upOrLow,q,color1, color2, csteps)
        fg.create_gradient_funnel(canvas,Z[0],Z[1], x,x*bb/aa,"U",y,color1, color2, csteps,tags)
        ###draw_lower_disc(canvas,Center,OuterMaA,OuterMiA,MajorAxis,MinorAxix,Q,color3)
        ###create_lower_disc(canvas,cx,cy,a,b,aa,bb,color)
        fg.create_lower_disc(canvas,Z[0],Z[1],x,x*bb/aa,aa,bb,hcolor3,tags)
        ##draw_cylinder(canvas,Center,UpperOuterMaA,UpperOuterMiA,LowerOuterMaA,LowerOuterMiA,color1,color2)
        ##create_gradient_cylinder(canvas,cx,cy,cx2,cy2,a,b,color1, color2, csteps)
        fg.create_gradient_cylinder(canvas,Z[0],Z[1],Z[0],B[1],aa,bb,color1, color2, csteps,tags)
        ##draw_funnel(canvas,Center,LowerOuterMaA,LowerOuterMiA,color1,color2)
        ###create_gradient_funnel(canvas,cx,cy, a,b,upOrLow,q,color1, color2, csteps):
        fg.create_gradient_funnel(canvas,Z[0],B[1], aa,bb,"L",c,color1, color2, csteps,tags)
        ###draw_funnel(canvas,Center,LowerOuterMaA,LowerOuterMiA,color1,color2)
    elif(time_elapsed <= t2):
        y=(p2*time_elapsed*cn+a**2*tan(φ))/(2*a)
        ###return [(X0,Z[1]+y-a*tan(φ)),(Z[0]+random.uniform(-1.0, 1.0),Z[1]+y),(N[0],Z[1]+y-a*tan(φ)),D,C,B]
        ##draw_hole(canvas,Center,MajorAxis,MinorAxix,Q,color1,color2)
        fg.create_gradient_funnel(canvas,Z[0],Z[1]+y-a*tan(φ), aa,bb,"U",a*tan(φ),color1, color2, csteps,tags)
        ##draw_cylinder(canvas,Center,UpperOuterMaA,UpperOuterMiA,LowerOuterMaA,LowerOuterMiA,color1,color2)
        ##create_gradient_cylinder(canvas,cx,cy,cx2,cy2,a,b,color1, color2, csteps)
        fg.create_gradient_cylinder(canvas,Z[0],Z[1]+y-a*tan(φ),Z[0],B[1],aa,bb,color1, color2, csteps,tags)
        ##draw_funnel(canvas,Center,LowerOuterMaA,LowerOuterMiA,color1,color2)
        ###create_gradient_funnel(canvas,cx,cy, a,b,upOrLow,q,color1, color2, csteps):
        fg.create_gradient_funnel(canvas,Z[0],B[1], aa,bb,"L",c,color1, color2, csteps,tags)
        ###draw_funnel(canvas,Center,LowerOuterMaA,LowerOuterMiA,color1,color2)
    elif(time_elapsed<t3):
        ###print("time_elapsed<=t3 ",time_elapsed,t3)
        y=b+c-sqrt((2*a*b+a**2*tan(Ψ)-p2*time_elapsed*cn)*(tan(Ψ)-tan(φ)))
        u=(b+c-y)/(tan(Ψ)-tan(φ))
        v=u*tan(φ)
        ###print("b+c,y,u,v=",b+c,y,u,v)
        ###return [(Z[0]-u,Z[1]+y-v),(Z[0],Z[1]+y),(Z[0]+u,Z[1]+y-v),C]
        ##draw_hole(canvas,Center,MajorAxis,MinorAxix,Q,color1,color2)
        fg.create_gradient_funnel(canvas,Z[0],Z[1]+y-v, u,u*bb/aa,"U",v,color1, color2, csteps,tags)
        ##draw_funnel(canvas,Center,LowerOuterMaA,LowerOuterMiA,color1,color2)
        fg.create_gradient_funnel(canvas,Z[0],Z[1]+y-v, u,u*bb/aa,"L",b+c-y+v,color1, color2, csteps,tags)
    else:
        ###print("b+c,y,u,v=",b+c,y,u,v)
        ###return [C,C,C]
        return
def create_eclipse(canvas,Center,major_axis, minor_axis, color,tags):
     (center_x, center_y)=Center
     create_ellipse(canvas, center_x, center_y, major_axis, minor_axis,color,tags)

def create_ellipse(canvas, center_x, center_y, major_axis, minor_axis,color,tags):
    """中心座標、長径、短径を指定して楕円を描画する"""
    x1 = center_x - major_axis #/ 2
    y1 = center_y - minor_axis #/ 2
    x2 = center_x + major_axis #/ 2
    y2 = center_y + minor_axis #/ 2
    return canvas.create_oval(x1, y1, x2, y2,fill=color, outline=color, width=2,tags=tags)

def draw_dropping_sand(canvas,Colors):
    color1=Colors[0]###鮮やか
    color2=Colors[1]###暗い
    color3=Colors[2]###中間色
    hcolor3='#%02x%02x%02x' % tuple(int((color1[i]+color2[i])/2) for i in range(3)) ###中間的な赤

    
    csteps=20
    tags="dropsand" 
    ###return [C,(LY[0]+random.uniform(-1.0, 1.0),LY[1])]
    return canvas.create_line(C[0],C[1],LY[0]+random.uniform(-1.0, 1.0),LY[1],fill=hcolor3, width=2,tags="dropsand")
def create_dropping_sand_shape():
        return [C,(LY[0]+random.uniform(-1.0, 1.0),LY[1])]

def draw_lower_sand(canvas,Colors):
        global LY
        color1=Colors[0]###鮮やか
        color2=Colors[1]###暗い
        color3=Colors[2]###中間色
        csteps=20
        tags="lowersand"    
        if time_elapsed<t1:
            x=sqrt(p2*time_elapsed*cn/tan(φ))
            y=sqrt(p2*time_elapsed*cn*tan(φ))
            LY=(X[0],X[1]-y)
            ###return [(X[0]-x,X[1]),(X[0],X[1]-y),(X[0]+x,X[1])]
            fg.create_gradient_funnel(canvas,X[0],X[1], x,x*bb/aa,"L",-y,color1, color2, csteps,tags)
        else:
            y=(p2*time_elapsed*cn+a**2*tan(φ))/(2*a)
            LY=(X[0],X[1]-y)
            ##return [(L[0],L[1]-y+a*tan(φ)),(X[0]+random.uniform(-1.0, 1.0),X[1]-y),(K[0],K[1]-y+a*tan(φ)),K,L]
            fg.create_gradient_funnel(canvas,LY[0],LY[1]+a*tan(φ), aa,bb,"L",-a*tan(φ),color1, color2, csteps,tags)
            fg.create_gradient_cylinder(canvas,LY[0],LY[1]+a*tan(φ),Z[0],L[1],aa,bb,color1, color2, csteps,tags)
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
init(root,Colors)
###ｳｨﾝﾄﾞｳを表示し、イベントを待つ
root.mainloop()