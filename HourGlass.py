import sys
import os
from PyQt5.QtCore import Qt, QTimer,QPointF,QPoint
from PyQt5.QtGui import QLinearGradient,QPainter,  QPen,QPainterPath,QPolygonF,QBrush, QColor, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QMenu,QInputDialog
from math import *
import random
import colorsys
import ellipse as ec
import funnel_gradation_funs as fg


#時間設定
cycle=1.0 #周期（分）
click=0.1 #更新間隔（秒）
cn=1/click ###1秒間のクリック数
time_full = 60*cycle  # 最終時間（秒）
tcn=time_full*cn ###全クリック数
time_elapsed=0.0 #経過時間

#キャンバス寸法 <-- overview.png
H=200#キャンバス幅
V=495#キャンバス高
#砂時計寸法
φ=radians(37)#安息角
Ψ=radians(55)#漏斗角
a=H/7+3#2a=横幅
b=a
c=a*tan(Ψ)
d=a*(tan(Ψ) - tan(φ))/2
e=2*a*tan(φ)
f=0
g=d+e
h=a*tan(φ)
k=b+d
X0=H/2 - a +2
Y0=V/2 - c - b - g+5
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
###枠組み
###上円盤
#       US1()  USw        .
#        |                |
#    USh |                |
#        '---------------US2()
uw=30
uh=20
USw=2*a+uw*2
USa=a+uw
USb=USa*0.3
USh=2*uh
US1=(M[0]-uw,M[1]-uh)
US2=(US1[0]+USw,US1[1]+USh)
LS1=(K[0]-uw,K[1]+uh)
LS2=(LS1[0]+USw,LS1[1]+USh)
###支柱
pca=7
pcb=pca*0.3
pclux=US1[0]+uw/2
pcluy=US2[1]
pcllx=LS1[0]+uw/2
pclly=LS1[1]

pcrux=US2[0]-uw/2
pcruy=US2[1]
pcrlx=LS1[0]+USw-uw/2
pcrly=LS1[1]

pcmfactor=0.9
pcmux=(US1[0]+US2[0])/2+uw*pcmfactor ##-2
pcmuy=US2[1]
pcmlx=pcmux
pcmly=LS1[1]

###楕円 長径、短径
aa=a
bb=aa*0.3
###瓶
def create_bottle():
        clock_shape=[M,A,B,C,F,G,O,K]
        ###,X,
        clock_shape.extend(ec.get_arc_of_eclipse(X[0],X[1],aa,bb,180,360,1))
        clock_shape.extend([L,Q,J,F,C,D,E,N,M])
        points=[QPointF(x,y) for (x,y) in clock_shape]
        return points
bottle = QPolygonF(create_bottle())

#総面積など
"""
S3=2*a*b+a**2*tan(Ψ)
S1=a**2*tan(φ)
S2=2*a*b+a**2*tan(φ)
"""
#総体積など
V3=pi*a**2*(b+a*tan(Ψ)/3)
V2=pi*a**2*(b+a*tan(φ)/3)
V1=pi*a**3*tan(φ)/3
#落ちる砂の量
p3=V3/tcn ###1回ごとに落ちる量
#チェックポイント
t3=V3/p3*click
t1=V1/V3*t3
t2=V2/V3*t3
t4=t3


def adjust_saturation_hsv(rgba, saturation_factor):
    """RGBA値の彩度を調整する
    Args:
        rgba: (r, g, b, a) のタプル (0-255)
        saturation_factor: 彩度調整の係数 (1.0: 変化なし, >1.0: 鮮やか, <1.0: くすみ)
    Returns:
        調整されたRGBA値のタプル (0-255)
    """
    if len(rgba) == 3:  # RGB値のみの場合
        r, g, b = [x / 255.0 for x in rgba]
        a = 1.0  # アルファ値を1.0に設定
    elif len(rgba) == 4:  # RGBA値の場合
        r, g, b, a = [x / 255.0 for x in rgba]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    s = min(1.0, max(0.0, s * saturation_factor))  # 彩度を調整
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return tuple(int(x * 255) for x in (r, g, b, a))
# グラデーションの色
color1 = (250, 150, 250)  # 鮮やかな薄紫
color2=(150,80,150)###暗い薄紫
color3=(170,90,170)
color3=adjust_saturation_hsv(color1,0.7)[:3]
Colors=(color1,color2,color3)
###シュラウドの種類
type_shroud=0 
###マウスの位置
mouse_position=(300,300)
mouse_movement=(0,0)
mouse_move_ever=False


class SandTimer(QWidget):
    def __init__(self):
        global time_elapsed
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background: transparent;")
        self.click = click  # タイマーの間隔（秒）
        self.initUI()
        ###
        self.mouse_pressed = False
        self.mouse_pos = QPoint()
        ###
        self.initTimer()
        ###

    def initUI(self):
        self.setGeometry(300, 300, H+20, V)
        self.setWindowTitle("砂時計")        
        ###データファイルの位置を確実にする
        if getattr(sys, 'frozen', False):
            # 実行ファイルからの実行時
            script_dir = sys._MEIPASS
        else:
            # スクリプトからの実行時
            script_dir = os.path.dirname(os.path.abspath(__file__))
        D = os.path.join(script_dir, "sunadokei.png")     
        self.image = QImage(D)  # 画像を読み込みます
        self.rotated_image=self.image
        self.show()

    def initTimer(self):
        global time_elapsed
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_sand)
        self.timer.start(int(1000 * self.click))#### click秒ごとに　===> update_sand()   
        time_elapsed = 0  # 経過時間（秒）

    def update_sand(self):#### <==== timer.timeout
            global time_elapsed
            if time_elapsed >= time_full:  # 3分経過
                self.timer.stop()
            else:
                # ここに砂時計の更新処理を記述   
                self.update()#### ====> paintEvent
                ###            
                time_elapsed += self.click

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # アンチエイリアスを有効にする
        if type_shroud == 0:
            self.draw_3rd_pole(painter)
        ###砂の描画
        self.draw_sand(painter)
        ###瓶の描画
        self.draw_bottle(painter)
        ###枠組み
        if type_shroud==1:
            ###painter.drawImage(0, 0, self.rotated_image)  # 画像を描画します 木製
            painter.drawImage(0, 70, self.rotated_image)  # 画像を描画します
        elif type_shroud==0:
            self.draw_shrouding(painter)

    def draw_bottle(self,qp):
        ##土台
        clock_base=[K]
        clock_base.extend(ec.get_arc_of_eclipse(X[0],X[1],aa,bb+1,180,360,1))
        clock_base.extend([L,(L[0],L[1]+40),(K[0],K[1]+40),K])
        points=[QPointF(x,y) for (x,y) in clock_base]
        path= QPainterPath()
        path.addPolygon(QPolygonF([QPointF(f[0],f[1]) for f in clock_base]))
        brush=QBrush(QColor(30, 0, 0))
        qp.setBrush(brush)
        pen=QPen(QColor(30, 0, 0))
        qp.setPen(pen)
        qp.drawPath(path)
        # グラデーションの作成（ガラスの質感）
        gradient = QLinearGradient(B[0], B[1], D[0], D[1])###B→D
        gradient.setColorAt(0, QColor(255, 255, 255, 100))  # 色：白、不透明度を設定　全透明
        gradient.setColorAt(0.5, QColor(255, 255, 255, 0))###透明
        gradient.setColorAt(1, QColor(255, 255, 255, 100))###不透明
        qp.setBrush(QBrush(gradient))
        path = QPainterPath()
        path.addPolygon(bottle)
        # 青いペンを設定
        pen = QPen(QColor(140, 140, 255))  # 青色
        pen.setWidth(2)  # ペンの太さを5ピクセルに設定
        qp.setPen(pen)
        ###描画
        qp.drawPath(path)

    def draw_shrouding(self,qp):
        ###上円盤
        path = QPainterPath()
        path.addEllipse(QPointF(M[0]+a, US1[1]), a+uw, uh)
        path.addEllipse(QPointF(M[0]+a, US2[1]), a+uw, uh)
        ##qp.drawEllipse(QRectF(US1[0], US1[1], USw, USh))
        ###下円盤
        ##path.addEllipse(QPointF(M[0]+a, LS1[1]), a+uw, uh)
        path.addEllipse(QPointF(M[0]+a, LS2[1]), a+uw, uh)
        # 青いペンを設定
        pen = QPen(QColor(113, 75, 52))  # 茶色
        pen.setWidth(2)  # ペンの太さを5ピクセルに設定
        qp.setPen(pen)
        ###
        qp.setBrush(QColor(113, 75, 52))
        ##qp.setBrush(QBrush(QColor(0,255,255)))
        qp.drawPath(path)
        ###支柱
        self.create_gradient_cylinder(qp,pclux,pcluy,pcllx,pclly,pca,pcb,(113, 75, 52),(60, 30, 20),10)
        self.create_gradient_cylinder(qp,pcrux,pcruy,pcrlx,pcrly,pca,pcb,(113, 75, 52),(60, 30, 20),10)
        self.create_gradient_cylinder(qp,Z[0],US1[1],Z[0],US2[1],USa,USb,(113, 75, 52),(60, 30, 20),10)
        self.create_gradient_cylinder(qp,Z[0],LS1[1],Z[0],LS2[1],USa,USb,(113, 75, 52),(60, 30, 20),10)
        return
    
    def draw_3rd_pole(self,painter):
        self.create_gradient_cylinder(painter,pcmux,pcmuy,pcmlx,pcmly,pca,pcb,(100, 70, 50),(50, 20, 10),10)
        
    def draw_sand(self,painter):
        global time_elapsed
        if time_full > time_elapsed:
            # 砂時計の砂の形を計算            
            #下の砂
            self.draw_lower_sand(painter,Colors)
            #落ちる砂
            self.draw_dropping_sand(painter,Colors)
            #上の砂
            self.draw_upper_sand(painter,Colors)
        else:
            ##下の砂
            self.draw_lower_sand(painter,Colors)
        

    def draw_upper_sand(self,painter,Colors):
        color1=Colors[0]###鮮やか
        color2=Colors[1]###暗い
        color3=Colors[2]###中間色
        csteps=20
        hcolor3='#%02x%02x%02x' % color3
        if(time_elapsed==0):
            self.create_eclipse(painter,Z,aa,bb,hcolor3)
            self.create_gradient_cylinder(painter,Z[0],Z[1],Z[0],B[1],aa,bb,color1, color2, csteps)
            self.create_gradient_funnel(painter,Z[0],B[1], aa,bb-1,"L",c-1,color1, color2, csteps)
        elif(time_elapsed<=t1):
            x=(time_elapsed*cn*3*p3/pi/tan(φ))**(1/3)
            y=((time_elapsed*cn*3*p3*tan(φ)**2)/pi)**(1/3)
            self.create_eclipse(painter,Z,aa,bb,hcolor3)###上部円盤
            self.create_gradient_funnel(painter,Z[0],Z[1], x,x*bb/aa*0.74,"U",y,color1, color2, csteps)
            self.create_lower_disc(painter,Z[0],Z[1],x,x*bb/aa,aa,bb,hcolor3)
            self.create_gradient_cylinder(painter,Z[0],Z[1],Z[0],B[1],aa,bb,color1, color2, csteps)
            self.create_gradient_funnel(painter,Z[0],B[1], aa,bb,"L",c,color1, color2, csteps)
        elif(time_elapsed <= t2):
            y=p3*time_elapsed*cn/(pi*a**2)+2*a*tan(φ)/3
            self.create_gradient_funnel(painter,Z[0],Z[1]+y-a*tan(φ), aa,bb,"U",a*tan(φ),color1, color2, csteps)
            self.create_gradient_cylinder(painter,Z[0],Z[1]+y-a*tan(φ),Z[0],B[1],aa,bb,color1, color2, csteps)
            self.create_gradient_funnel(painter,Z[0],B[1], aa,bb,"L",c,color1, color2, csteps)
        elif(time_elapsed<t3):
            y=b+c-((V3-p3*time_elapsed*cn)*(tan(Ψ)-tan(φ))**2/(pi/3))**(1/3)
            u=(b+c-y)/(tan(Ψ)-tan(φ))
            v=u*tan(φ)
            self.create_gradient_funnel(painter,Z[0],Z[1]+y-v, u,u*bb/aa,"U",v,color1, color2, csteps)
            self.create_gradient_funnel(painter,Z[0],Z[1]+y-v, u,u*bb/aa,"L",b+c-y+v,color1, color2, csteps)
        else:
            return
        
    def create_eclipse(self,painter,Center,major_axis, minor_axis, color):
        # 塗りつぶし色を設定
        colort=color
        if not isinstance(color, QColor):
            colort = QColor(color) #colorがタプルだった場合
        brush = QBrush(colort)  # 赤色
        painter.setBrush(brush)
        # 楕円を描画
        painter.drawEllipse(QPointF(Center[0],Center[1]),major_axis, minor_axis)

    def draw_lower_sand(self,painter,Colors):
        global LY,mouse_movement,mouse_position
        color1=Colors[0]###鮮やか
        color2=Colors[1]###暗い
        color3=Colors[2]###中間色
        csteps=20
        if time_elapsed<t1:
            x=(p3*time_elapsed*cn/(pi*tan(φ)/3))**(1/3)
            y=(p3*time_elapsed*cn*tan(φ)**2/(pi/3))**(1/3)
            LY=(X[0],X[1]-y)
            self.create_gradient_funnel(painter,X[0],X[1], x,x*bb/aa,"L",-y,color1, color2, csteps)
        elif time_elapsed<=t3:
            y=(p3*time_elapsed*cn+2*pi*a**3*tan(φ)/3)/(pi*a**2)
            LY=(X[0],X[1]-y)
            self.create_gradient_funnel(painter,LY[0],LY[1]+a*tan(φ), aa,bb,"L",-a*tan(φ),color1, color2, csteps)
            self.create_gradient_cylinder(painter,LY[0],LY[1]+a*tan(φ),Z[0],L[1],aa,bb,color1, color2, csteps)
        else:
            if mouse_move_ever:
                ###
                γ=random.uniform(-φ, φ)
                bd=b+a*(tan(Ψ)-tan(φ))/2
                t=bd+a*tan(γ)
                u=bd-a*tan(γ)
                self.create_gradient_line_ellipse(painter,bd,γ,X[0],X[1],a,b,color1,color2,1)
                ###
                mouse_movement=(0,0)
            else:
                y=(p3*time_elapsed*cn+2*pi*a**3*tan(φ)/3)/(pi*a**2)
                LY=(X[0],X[1]-y)
                ##return [(L[0],L[1]-y+a*tan(φ)),(X[0]+random.uniform(-1.0, 1.0),X[1]-y),(K[0],K[1]-y+a*tan(φ)),K,L]
                self.create_gradient_funnel(painter,LY[0],LY[1]+a*tan(φ), aa,bb,"L",-a*tan(φ),color1, color2, csteps)
                self.create_gradient_cylinder(painter,LY[0],LY[1]+a*tan(φ),Z[0],L[1],aa,bb,color1, color2, csteps)
                
    def get_Y_from_X_on_line(self,bd,cx,cy,γ,X):
        Y=-(bd+(-X+cx)*tan(γ))+cy
        return Y
    def create_gradient_line_ellipse(self,qp,bd,γ,cx,cy,a,b,color1,color2,csteps):
        xylist=ec.get_arc_of_eclipse(cx,cy,a,b,180,360,1)
        lxylist=[]
        for (x,y) in xylist:
            lxylist.insert(0,(x,self.get_Y_from_X_on_line(bd,cx,cy,γ,x)))
        points=xylist
        points.extend(lxylist)
        ###
        # グラデーションブラシを作成
        gradient = QLinearGradient(QPointF(K[0],K[1]), QPointF(L[0],L[1]))
        gradient.setColorAt(0, QColor(color2[0],color2[1],color2[2],255))  # 開始色: 赤
        gradient.setColorAt(0.5, QColor(color1[0],color1[1],color1[2],255))###色：color1、透明
        gradient.setColorAt(1, QColor(color2[0],color2[1],color2[2],255))  # 終了色: 青
        ###
        pathl=QPainterPath()
        # 折れ線を描画
        pointsl=[QPointF(f[0],f[1]) for f in points]
        pathl.addPolygon(QPolygonF(pointsl))
        brush = QBrush(gradient)
        qp.fillPath(pathl, brush)

    def draw_dropping_sand(self,painter,Colors):
        color1=Colors[0]###鮮やか
        color2=Colors[1]###暗い
        color3=Colors[2]###中間色
        hcolor3='#%02x%02x%02x' % tuple(int((color1[i]+color2[i])/2) for i in range(3)) ###中間的な赤
        csteps=20
        # ペンの設定
        pen = QPen(QColor(hcolor3))  # 赤色
        pen.setWidth(1)  # 線の太さ
        painter.setPen(pen)
        # 線を描画
        start_point = QPointF(C[0],C[1])
        end_point = QPointF(LY[0]+random.uniform(-1.0, 1.0),LY[1])
        painter.drawLine(start_point, end_point)

    ###漏斗
    def create_gradient_funnel(self,qp,cx,cy, a,b,upOrLow,q,color1, color2, csteps):
        """グラデーション漏斗を作成する関数"""
        if abs(q)<= 0:
            return
        ###接点
        (xtl,ytl),(xtr,ytr)=ec.get_tangent_points(a,b,q)
        θl=ec.get_θ_from_xy(xtl,ytl)
        θr=ec.get_θ_from_xy(xtr,ytr) 
        if upOrLow=="U" and θl<θr:###　θl>θrとなるように補正する
            θl+=360
        elif upOrLow=="L" and θl>θr:###　θl<θrとなるように補正する
            θr+=360
        ###楕円点列   
        xylist=[]
        ###　U：右→左
        ###右側 xylistr
        ### U:θr -> 90°＝右→中央＝暗→明＝（xtr,ytr）ー＞（cx,cy-b）
        ###左側 xylistl
        ### U:90°→θl=中央→左＝90°,....,θl＝（cx,cy-b）→（xtl,ytl）　明→暗
        ###　L：左→右
        ###左側 xylistl
        ### L:θl→t90＝左→中央＝暗→明= （xtl,ytl） -> （cx,cy+b）
        ###右側 xylistr
        ### L:t90　→θr＝中央→右＝明→暗= (cx,cy+b) -> (xtr,ytr)
        if upOrLow == "U":###　U：右→左
            xylistr=ec.get_arc_of_eclipse(cx,cy,a,b,θr,90,1)###右半分θr,....,90°　暗→明
            xylist.extend(xylistr)
            xylistl=ec.get_arc_of_eclipse(cx,cy,a,b,90,θl,1)###左半分　θl<--90°
            xylist.extend(xylistl)###90°,....,θl　明→暗
            xylist.append((cx,cy+q))
        else:###　L：左→右
            t90=270
            if θl<0:
                t90=-90             
            xylistl=ec.get_arc_of_eclipse(cx,cy,a,b,θl,t90,1)###左半分　θl-->t90°＝θl,....,t90　暗→明
            xylist.extend(xylistl)
            xylistr=ec.get_arc_of_eclipse(cx,cy,a,b,t90,θr,1)###右半分　    t90-->θr
            xylist.extend(xylistr)### t90,....,θr　明→暗
            xylist.append((cx,cy+q))
        ###漏斗の描写
        ### linear gradation
        # グラデーションの作成（ガラスの質感）
        gradient=QLinearGradient()
        if upOrLow == "U":### U:θr->90°→θl＝右→中央→左＝暗→明→暗＝（xtr,ytr）→（cx,cy-b）→（xtl,ytl）
            gradient = QLinearGradient(cx+a,cy, cx-a, cy)###楕円の両端＝右→中央→左
        else:###左→中央→右
            gradient = QLinearGradient(cx-a,cy, cx+a, cy)###楕円の両端＝左→中央→右
        gradient.setColorAt(0, QColor(color2[0],color2[1],color2[2],255))# 色：color2、不透明
        gradient.setColorAt(0.5, QColor(color1[0],color1[1],color1[2],255))###色：color1、透明
        gradient.setColorAt(1, QColor(color2[0],color2[1],color2[2],255))# 色：color2、不透明
        qp.setBrush(QBrush(gradient))
        path = QPainterPath()
        path.addPolygon(QPolygonF(QPointF(f[0],f[1]) for f in xylist))
        ###描画
        qp.drawPath(path)

    def create_gradient_funnel2(self,painter,cx,cy, a,b,upOrLow,q,color1, color2, csteps):
        """グラデーション漏斗を作成する関数"""
        if abs(q)<= 0:
            return
        ###接点
        (xtl,ytl),(xtr,ytr)=ec.get_tangent_points(a,b,q)
        θl=ec.get_θ_from_xy(xtl,ytl)
        θr=ec.get_θ_from_xy(xtr,ytr)  
        if upOrLow=="U" and θl<θr:###　θl>θrとなるように補正する
            θl+=360
        elif upOrLow=="L" and θl>θr:###　θl<θrとなるように補正する
            θr+=360
        ###楕円点列   
        if upOrLow == "U":
            xylistr=ec.get_arc_of_eclipse(cx,cy,a,b,θr,90,1)###右半分　     90°<--θr
            xylistr.append((cx,cy-b))###θr,....,90°　暗→明
            xylistl=ec.get_arc_of_eclipse(cx,cy,a,b,90,θl,1)###左半分　θl<--90°
            xylistl.insert(0,(cx,cy-b))###90°,....,θl　明→暗
        else:
            t90=270
            if θl<0:
                t90=-90 
            xylistr=ec.get_arc_of_eclipse(cx,cy,a,b,t90,θr,1)###右半分　    t90-->θr
            xylistr.insert(0,(cx,cy+b))### t90,....,θr　明→暗
            xylistl=ec.get_arc_of_eclipse(cx,cy,a,b,θl,t90,1)###左半分　θl-->t90°
            xylistl.append((cx,cy+b))###　θl,....,t90　暗→明
        ###漏斗の描写
        ###右側
        steps=min(csteps,len(xylistr))
        xystep=max(1,int(len(xylistr)/steps))
        for i in range(steps):
            points=[(cx,cy+q)]
            k=(i+1)*xystep
            if(i==steps-1):
                k=len(xylistr)
            for j in range(i*xystep,k):
                points.append(xylistr[j])
            ###
            color=self.get_gradient_color(color1,color2,steps,i)###明→暗
            if upOrLow == "U":
                color=self.get_gradient_color(color2,color1,steps,i)###暗→明
            ###
            # QPointのリストを作成
            qpoints = [QPointF(x, y) for x, y in points]
            # QPolygonFを作成
            polygon = QPolygonF(qpoints)
            path = QPainterPath()
            path.addPolygon(polygon)
            # 塗りつぶし色を設定
            colort=color
            if not isinstance(color, QColor):
                colort = QColor(color) #colorがタプルだった場合
            brush = QBrush(colort)
            painter.setBrush(brush)
            ###
            painter.drawPath(path)
        ###左側
        steps=min(csteps,len(xylistl))
        xystep=max(1,int(len(xylistl)/steps))
        for i in range(steps):
            points=[(cx,cy+q)]
            k=(i+1)*xystep
            if(i==steps-1):
                k=len(xylistl)
            for j in range(i*xystep,k):
                points.append(xylistl[j])
            ###
            color=self.get_gradient_color(color2,color1,steps,i)###暗→明
            if upOrLow == "U":
                color=self.get_gradient_color(color1,color2,steps,i)###明→暗
            ###
            # QPointのリストを作成
            qpoints = [QPointF(x, y) for x, y in points]
            # QPolygonFを作成
            polygon = QPolygonF(qpoints)
            path = QPainterPath()
            path.addPolygon(polygon)
            # 塗りつぶし色を設定
            colort=color
            if not isinstance(color, QColor):
                colort = QColor(color) #colorがタプルだった場合
            brush = QBrush(colort)
            painter.setBrush(brush)
            ###
            painter.drawPath(path)

    def create_gradient_cylinder(self,qp,cx,cy,cx2,cy2,a,b,color1, color2, csteps):
        """二つの楕円を結ぶ円筒を描画する"""
        ### L to L
        xylist=[]
        xylistu=[]
        xylistl=[]
        ###楕円点列
        xylistru=ec.get_arc_of_eclipse(cx,cy,a,b,270,360,1)
        xylistrl=ec.get_arc_of_eclipse(cx2,cy2,a,b,270,360,1)
        xylistlu=ec.get_arc_of_eclipse(cx,cy,a,b,180,270,1)
        xylistll=ec.get_arc_of_eclipse(cx2,cy2,a,b,180,270,1)
        xylistu.extend(xylistlu)###180->270
        xylistu.extend(xylistru)###270->360
        xylistl.extend(xylistrl[::-1])###360->270
        xylistl.extend(xylistll[::-1])###270->180
        xylist=xylistu+xylistl
        ### linear gradation
        # グラデーションの作成（ガラスの質感）
        ###左→中央→右
        gradient = QLinearGradient(cx-a,cy, cx+a, cy)###楕円の両端＝左→中央→右
        gradient.setColorAt(0, QColor(color2[0],color2[1],color2[2],255))# 色：color2、不透明
        gradient.setColorAt(0.5, QColor(color1[0],color1[1],color1[2],255))###色：color1、透明
        gradient.setColorAt(1, QColor(color2[0],color2[1],color2[2],255))# 色：color2、不透明
        qp.setBrush(QBrush(gradient))
        ###
        path = QPainterPath()
        path.addPolygon(QPolygonF(QPointF(f[0],f[1]) for f in xylist))
        ###描画
        qp.drawPath(path)
        ###上下の線をグラデーション        
        # 楕円のパスを作成
        pathu=QPainterPath()
        # 折れ線を描画
        pointsu=[QPointF(f[0],f[1]) for f in xylistu]
        pathu.addPolygon(QPolygonF(pointsu))
        # グラデーションブラシを作成
        gradient = QLinearGradient(pointsu[0], pointsu[-1])
        gradient.setColorAt(0, QColor(color2[0],color2[1],color2[2],255))  # 開始色: 赤
        gradient.setColorAt(0.5, QColor(color1[0],color1[1],color1[2],255))###色：color1、透明
        gradient.setColorAt(1, QColor(color2[0],color2[1],color2[2],255))  # 終了色: 青
        ###
        brush = QBrush(gradient)
        qp.fillPath(pathu, brush)
        ###下側
        pathl=QPainterPath()
        # 折れ線を描画
        pointsl=[QPointF(f[0],f[1]) for f in xylistl]
        pathl.addPolygon(QPolygonF(pointsl))
        brush = QBrush(gradient)
        qp.fillPath(pathl, brush)

    def create_lower_disc(self,painter,cx,cy,a,b,aa,bb,color):
        ###              １        ４      ３
        ###           -a    -aa   cx   aa    a
        ### cy         .------.         .----.
        ### cy+bb                  -
        ### cy+b         ２        -
        xylist=[]
        xylist.append((cx-aa,cy))
        xylist.append((cx-a,cy))###１
        xylist.extend(ec.get_arc_of_eclipse(cx,cy,a,b,180,360,1))###２
        xylist.append((cx+a,cy))
        xylist.append((cx+aa,cy))###３
        xylist.extend(ec.get_arc_of_eclipse(cx,cy,aa,bb,360,180,-1))###４
        # QPointのリストを作成
        qpoints = [QPointF(x, y) for x, y in xylist]
        # QPolygonFを作成
        polygon = QPolygonF(qpoints)
        path = QPainterPath()
        path.addPolygon(polygon)
        # 塗りつぶし色を設定
        colort=color
        if not isinstance(color, QColor):
                colort = QColor(color) #colorがタプルだった場合
        brush = QBrush(colort)
        painter.setBrush(brush)
        # 縁の色を設定
        pen = QPen(QColor(colort))  # 青色
        painter.setPen(pen)
        ###
        painter.drawPath(path)
        
    def get_gradient_color(self,color1,color2,steps,i):
        ratio= i / (steps - 1)
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        color = '#%02x%02x%02x' % (r, g, b)
        return color        
    def paint_point(self,qp,color,cx,cy,r):        
        # 大きさ10の白色の点を描画
        qp.setPen(color)  # ペンの色を白色に設定 as QColor(255, 0, 0)
        qp.setBrush(color)  # ブラシの色を白色に設定
        qp.drawEllipse(QPointF(cx, cy), r, r)  # 中心(100, 100)、半径5の円を描画
    def paint_pointP(self,qp,color,P,r):
        self.paint_point(qp,color,P[0],P[1],r)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = True
            self.mouse_pos = event.globalPos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.mouse_pressed:
            delta = event.globalPos() - self.mouse_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.mouse_pos = event.globalPos()
            event.accept()

    def mouseReleaseEvent(self, event):
        global mouse_position,mouse_movement,mouse_move_ever
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = False
            ###
            event.accept()   

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)
        context_menu.setStyleSheet("""
            QMenu {
                background-color: lightblue; /* 背景色 */
                border: 1px solid blue; /* 枠線 */
            }
            QMenu::item:selected {
                background-color: skyblue; /* 選択時の背景色 */
            }
        """)
        action1 = context_menu.addAction("開始")
        action2 = context_menu.addAction("時間(分)")
        action3 = context_menu.addAction("枠")
        exit_action = context_menu.addAction("終了")
        exit_action.triggered.connect(QApplication.quit) # 終了アクション
        
        action1.triggered.connect(self.action1_triggered)
        action2.triggered.connect(self.action2_triggered)
        action3.triggered.connect(self.action3_triggered)

        context_menu.exec_(self.mapToGlobal(event.pos()))

    def action1_triggered(self):
        self.initTimer()
        ###time_elapsed = 0  # 経過時間（秒）
        ###print("アクション1が選択されました")

    def action2_triggered(self):
        global cycle,SystemReSet
        ###print("cycle,,cn,time_full,tcn,p2=",cycle,cn,time_full,tcn,p2)
        qid=QInputDialog()
        # スタイルシートを設定
        qid.setStyleSheet("""
            QInputDialog {
                background-color: lightblue; /* ダイアログ全体の背景色 */
            }
            QLabel {
                color: black; /* ラベルの文字色 */
            }
            QLineEdit {
                background-color: yellow; /* 入力フィールドの背景色 */
                color: darkblue; /* 入力文字の色 */
            }
            QPushButton {
                background-color: skyblue; /* ボタンの背景色 */
            }
        """)
        text, ok = qid.getText(self, "Change time(mimutes)", "Enter:")
        if ok:
            ###print("入力された値:", text)
            try:
                tval=float(text)
                if tval<0.1:
                    return
                else:
                    SystemReSet(tval,0.1)
            except ValueError:
                return False
            
    def action3_triggered(self):
        global type_shroud,pcmfactor,pcmux,pcmlx
        type_shroud += 1
        type_shroud %=3
        ##重装備
        ###if type_shroud==0:
        pcmfactor = random.uniform(-0.95, 0.95)
        pcmux=(US1[0]+US2[0])/2+uw*pcmfactor
        pcmlx=pcmux
        return  
def SystemReSet(aaaa,bbbb):
    global cycle,click,cn,time_full,tcn,time_elapsed,V3,p3,t1,t2,t3,t4,mouse_move_ever
    #時間設定
    cycle=aaaa #周期（分）
    click=bbbb #更新間隔（秒）
    cn=1/click ###1秒間のクリック数
    time_full = 60*cycle  # 最終時間（秒）
    tcn=time_full*cn ###全クリック数
    time_elapsed=0.0 #経過時間
    p3=V3/tcn
    #チェックポイント
    t3=V3/p3*click
    t1=V1/V3*t3
    t2=V2/V3*t3
    t4=t3
    mouse_move_ever=False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sand_timer = SandTimer()
    sys.exit(app.exec_())
