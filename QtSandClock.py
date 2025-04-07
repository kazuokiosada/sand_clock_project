import sys
from PyQt5.QtCore import Qt, QTimer,QRectF,QPointF,QPoint
from PyQt5.QtGui import QTransform,QPainter,  QPen,QPainterPath,QPolygonF,QBrush, QColor, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QMenu,QInputDialog
from math import *
import random
import ellipse as ec
import funnel_gradation_funs as fg

#時間設定
cycle=0.5 #周期（分）
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
Ψ=radians(60)#漏斗角
a=H/7+3#2a=横幅
b=a
c=a*tan(Ψ)
d=a*(tan(Ψ) - tan(φ))/2
e=2*a*tan(φ)
f=0
g=d+4*e
h=a*tan(φ)
k=b+d
X0=H/2 - a +2
Y0=V/2 - c - b - g +5
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
S3=2*a*b+a**2*tan(Ψ)
S1=a**2*tan(φ)
S2=2*a*b+a**2*tan(φ)
#落ちる砂の量
p2=S3/tcn ###1回ごとに落ちる量
###print("p2=S3/tcn:",p2,S3,tcn)
#チェックポイント
t3=S3/p2*click ###=tcn*click=time_full*cn*click=60*cycle*cn*click=60*cycle
t1=S1/S3*t3
t2=S2/S3*t3
t4=t3
##print("t1=a**2*tan(φ)/p2*click",t1,a,a**2*tan(φ),p2,a**2*tan(φ)/p2)
###print("t1 t2 t3=",t1,t2,t3)
###砂の色
# グラデーションの色
color1 = (238, 130, 238)  # 鮮やかな薄紫
color2=(160,90,160)###暗い紫
###color3= '#%02x%02x%02x' % tuple(int((color1[i]+color2[i])/2) for i in range(3))
###color3='#%02x%02x%02x' % (200, 0, 0)###中間的な赤
###color3='#%02x%02x%02x' % tuple(int((color1[i]+color2[i])/2) for i in range(3)) ###中間的な赤
color3=(200,110,200)
"""
color1 = (255, 0, 0)  # 鮮やかな赤
color2=(100,0,0)###暗い赤
###color3= '#%02x%02x%02x' % tuple(int((color1[i]+color2[i])/2) for i in range(3))
###color3='#%02x%02x%02x' % (200, 0, 0)###中間的な赤
###color3='#%02x%02x%02x' % tuple(int((color1[i]+color2[i])/2) for i in range(3)) ###中間的な赤
color3=(170,0,0)
"""
Colors=(color1,color2,color3)

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

    def initUI(self):
        self.setGeometry(300, 300, H, V)
        self.setWindowTitle("砂時計")
        self.image = QImage("砂時計枠組み.png")  # 画像を読み込みます
        transform = QTransform().rotate(3)  # 3度回転する変換行列を作成
        self.rotated_image = self.image.transformed(transform, Qt.SmoothTransformation)  # 画像を回転

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
        ###砂の描画
        self.draw_sand(painter)
        ###瓶の描画
        self.draw_bottle(painter)
        ###枠組み
        painter.drawImage(0, 0, self.rotated_image)  # 画像を描画します

    def draw_bottle(self,painter):
        path = QPainterPath()
        path.addPolygon(bottle)
        # 塗りつぶし色を設定
        # 透明なブラシを設定
        brush = QBrush(Qt.transparent)
        painter.setBrush(brush)
        # 青いペンを設定
        pen = QPen(QColor(0, 0, 255))  # 青色
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawPath(path)

    def draw_sand(self,painter):
        global time_elapsed
        if time_full > time_elapsed:
            # 砂時計の砂の形を計算            
            # 落ちる砂、下の砂
            ###if time_full > time_elapsed:
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
        ###tuple(int((color1[i]+color2[i])/2) for i in range(3)) ###中間的な赤
        if(time_elapsed==0):
            ###return [A,B,C,D,E]        
            self.create_eclipse(painter,Z,aa,bb,hcolor3)
            ###create_gradient_cylinder(canvas,cx,cy,cx2,cy2,a,b,color1, color2, csteps)
            self.create_gradient_cylinder(painter,Z[0],Z[1],Z[0],B[1],aa,bb,color1, color2, csteps)
            ##draw_funnel(canvas,Center,LowerOuterMaA,LowerOuterMiA,color1,color2)
            ###create_gradient_funnel(canvas,cx,cy, a,b,upOrLow,q,color1, color2, csteps):
            self.create_gradient_funnel(painter,Z[0],B[1], aa,bb-1,"L",c-1,color1, color2, csteps)
        elif(time_elapsed<=t1):
            x=sqrt(p2*time_elapsed*cn/tan(φ))
            y=sqrt(p2*time_elapsed*cn*tan(φ))
            ###return [(Z[0]-x,Z[1]),(Z[0]+random.uniform(-1.0, 1.0),Z[1]+y),(Z[0]+x,Z[1]),E,D,C,B,A]
            self.create_eclipse(painter,Z,aa,bb,hcolor3)###上部円盤
            ###draw_hole(canvas,Center,MajorAxis,MinorAxix,Q,color1,color2)
            ###create_gradient_funnel(painter,Z,cx,cy, a,b,upOrLow,q,color1, color2, csteps)
            self.create_gradient_funnel(painter,Z[0],Z[1], x,x*bb/aa,"U",y,color1, color2, csteps)
            ###draw_lower_disc(canvas,Center,OuterMaA,OuterMiA,MajorAxis,MinorAxix,Q,color3)
            ###create_lower_disc(canvas,cx,cy,a,b,aa,bb,color)
            self.create_lower_disc(painter,Z[0],Z[1],x,x*bb/aa,aa,bb,hcolor3)
            ##draw_cylinder(canvas,Center,UpperOuterMaA,UpperOuterMiA,LowerOuterMaA,LowerOuterMiA,color1,color2)
            ##create_gradient_cylinder(canvas,cx,cy,cx2,cy2,a,b,color1, color2, csteps)
            self.create_gradient_cylinder(painter,Z[0],Z[1],Z[0],B[1],aa,bb,color1, color2, csteps)
            ##draw_funnel(canvas,Center,LowerOuterMaA,LowerOuterMiA,color1,color2)
            ###create_gradient_funnel(canvas,cx,cy, a,b,upOrLow,q,color1, color2, csteps):
            self.create_gradient_funnel(painter,Z[0],B[1], aa,bb,"L",c,color1, color2, csteps)
            ###draw_funnel(canvas,Center,LowerOuterMaA,LowerOuterMiA,color1,color2)
        elif(time_elapsed <= t2):
            y=(p2*time_elapsed*cn+a**2*tan(φ))/(2*a)
            ###return [(X0,Z[1]+y-a*tan(φ)),(Z[0]+random.uniform(-1.0, 1.0),Z[1]+y),(N[0],Z[1]+y-a*tan(φ)),D,C,B]
            ##draw_hole(canvas,Center,MajorAxis,MinorAxix,Q,color1,color2)
            self.create_gradient_funnel(painter,Z[0],Z[1]+y-a*tan(φ), aa,bb,"U",a*tan(φ),color1, color2, csteps)
            ##draw_cylinder(canvas,Center,UpperOuterMaA,UpperOuterMiA,LowerOuterMaA,LowerOuterMiA,color1,color2)
            ##create_gradient_cylinder(canvas,cx,cy,cx2,cy2,a,b,color1, color2, csteps)
            self.create_gradient_cylinder(painter,Z[0],Z[1]+y-a*tan(φ),Z[0],B[1],aa,bb,color1, color2, csteps)
            ##draw_funnel(canvas,Center,LowerOuterMaA,LowerOuterMiA,color1,color2)
            ###create_gradient_funnel(canvas,cx,cy, a,b,upOrLow,q,color1, color2, csteps):
            self.create_gradient_funnel(painter,Z[0],B[1], aa,bb,"L",c,color1, color2, csteps)
            ###draw_funnel(canvas,Center,LowerOuterMaA,LowerOuterMiA,color1,color2)
        elif(time_elapsed<t3):
            ###print("time_elapsed<=t3 ",time_elapsed,t3)
            y=b+c-sqrt((2*a*b+a**2*tan(Ψ)-p2*time_elapsed*cn)*(tan(Ψ)-tan(φ)))
            u=(b+c-y)/(tan(Ψ)-tan(φ))
            v=u*tan(φ)
            ###print("b+c,y,u,v=",b+c,y,u,v)
            ###return [(Z[0]-u,Z[1]+y-v),(Z[0],Z[1]+y),(Z[0]+u,Z[1]+y-v),C]
            ##draw_hole(canvas,Center,MajorAxis,MinorAxix,Q,color1,color2)
            self.create_gradient_funnel(painter,Z[0],Z[1]+y-v, u,u*bb/aa,"U",v,color1, color2, csteps)
            ##draw_funnel(canvas,Center,LowerOuterMaA,LowerOuterMiA,color1,color2)
            self.create_gradient_funnel(painter,Z[0],Z[1]+y-v, u,u*bb/aa,"L",b+c-y+v,color1, color2, csteps)
        else:
            ###print("b+c,y,u,v=",b+c,y,u,v)
            ###return [C,C,C]
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
        global LY
        color1=Colors[0]###鮮やか
        color2=Colors[1]###暗い
        color3=Colors[2]###中間色
        csteps=20
        if time_elapsed<t1:
            x=sqrt(p2*time_elapsed*cn/tan(φ))
            y=sqrt(p2*time_elapsed*cn*tan(φ))
            LY=(X[0],X[1]-y)
            ###return [(X[0]-x,X[1]),(X[0],X[1]-y),(X[0]+x,X[1])]
            self.create_gradient_funnel(painter,X[0],X[1], x,x*bb/aa,"L",-y,color1, color2, csteps)
        else:
            y=(p2*time_elapsed*cn+a**2*tan(φ))/(2*a)
            LY=(X[0],X[1]-y)
            ##return [(L[0],L[1]-y+a*tan(φ)),(X[0]+random.uniform(-1.0, 1.0),X[1]-y),(K[0],K[1]-y+a*tan(φ)),K,L]
            self.create_gradient_funnel(painter,LY[0],LY[1]+a*tan(φ), aa,bb,"L",-a*tan(φ),color1, color2, csteps)
            self.create_gradient_cylinder(painter,LY[0],LY[1]+a*tan(φ),Z[0],L[1],aa,bb,color1, color2, csteps)
    def draw_dropping_sand(self,painter,Colors):
        color1=Colors[0]###鮮やか
        color2=Colors[1]###暗い
        color3=Colors[2]###中間色
        hcolor3='#%02x%02x%02x' % tuple(int((color1[i]+color2[i])/2) for i in range(3)) ###中間的な赤
        csteps=20
        ###return [C,(LY[0]+random.uniform(-1.0, 1.0),LY[1])]
        ###return canvas.create_line(C[0],C[1],LY[0]+random.uniform(-1.0, 1.0),LY[1],fill=hcolor3, width=2,tags="dropsand")
        # ペンの設定
        pen = QPen(QColor(hcolor3))  # 赤色
        pen.setWidth(1)  # 線の太さ
        painter.setPen(pen)
        # 線を描画
        start_point = QPointF(C[0],C[1])
        end_point = QPointF(LY[0]+random.uniform(-1.0, 1.0),LY[1])
        painter.drawLine(start_point, end_point)
    ###漏斗
    def create_gradient_funnel(self,painter,cx,cy, a,b,upOrLow,q,color1, color2, csteps):
        """グラデーション漏斗を作成する関数"""
        if abs(q)<= 0:
            return
        ###接点
        (xtl,ytl),(xtr,ytr)=ec.get_tangent_points(a,b,q)
        θl=ec.get_θ_from_xy(xtl,ytl)
        θr=ec.get_θ_from_xy(xtr,ytr)
        ###print("create_gradient_funnel:upOrLow=",upOrLow,"θl=",θl,"θr=",θr)    
        if upOrLow=="U" and θl<θr:###　θl>θrとなるように補正する
            θl+=360
            ###print("修正　θl=",θl,"θr=",θr)
        elif upOrLow=="L" and θl>θr:###　θl<θrとなるように補正する
            θr+=360
            ###print("修正　θl=",θl,"θr=",θr)
        ###楕円点列   
        if upOrLow == "U":
            xylistr=ec.get_arc_of_eclipse(cx,cy,a,b,θr,90,1)###右半分　     90°<--θr
            xylistr.append((cx,cy-b))###θr,....,90°　暗→明
            xylistl=ec.get_arc_of_eclipse(cx,cy,a,b,90,θl,1)###左半分　θl<--90°
            xylistl.insert(0,(cx,cy-b))###90°,....,θl　明→暗
            """
            print("θr,90,90,θl=",θr,90,90,θl)        
            print("upOrLow,θ1,θ2=",upOrLow,θl,θr)
            print("len(xylistr),len(xylistl)=",len(xylistr),len(xylistl))
            """
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
        ###print("右側　steps=",steps," xystep=",xystep)
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

    def create_gradient_cylinder(self,painter,cx,cy,cx2,cy2,a,b,color1, color2, csteps):
        """二つの楕円を結ぶ円筒を描画する"""
        ###楕円点列
        xylistru=ec.get_arc_of_eclipse(cx,cy,a,b,270,360,1)
        xylistrl=ec.get_arc_of_eclipse(cx2,cy2,a,b,270,360,1)
        xylistlu=ec.get_arc_of_eclipse(cx,cy,a,b,180,270,1)
        xylistll=ec.get_arc_of_eclipse(cx2,cy2,a,b,180,270,1)
        ###右側
        steps=min(csteps,len(xylistru),len(xylistrl))
        xystep=max(1,min(int(len(xylistru)/steps),int(len(xylistrl)/steps)))
        ###print("右側　steps=",steps," xystep=",xystep)
        ###
        lpu=(xylistru[0][0],xylistru[0][1])
        lpl=(xylistrl[0][0],xylistrl[0][1])
        for i in range(steps):
            points=[lpu]
            lpoints=[lpl]
            k=(i+1)*xystep
            if(i==steps-1):
                k=len(xylistru)
            for j in range(i*xystep,k):
                lpu=xylistru[j]
                lpl=xylistrl[j]
                points.append(lpu)
                lpoints.insert(0,lpl)
            points.extend(lpoints)
            ###
            color=self.get_gradient_color(color1,color2,steps,i)
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
        steps=min(csteps,len(xylistlu),len(xylistll))
        xystep=max(1,int(len(xylistlu)/steps),int(len(xylistll)/steps))
        ###print("左側　steps=",steps," xystep=",xystep)
        ###
        lpu=(xylistlu[0][0],xylistlu[0][1])
        lpl=(xylistll[0][0],xylistll[0][1])
        for i in range(steps):
            points=[lpu]
            lpoints=[lpl]
            k=(i+1)*xystep
            if(i==steps-1):
                k=len(xylistlu)
            for j in range(i*xystep,k):
                lpu=xylistlu[j]
                lpl=xylistll[j]
                points.append(lpu)
                lpoints.insert(0,lpl)
            points.extend(lpoints)
            ###
            color=self.get_gradient_color(color2,color1,steps,i)
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
        ###print("i steps color1 color2",i,steps,color1,color2)
        ratio= i / (steps - 1)
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        color = '#%02x%02x%02x' % (r, g, b)
        return color        

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
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = False
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
        action2 = context_menu.addAction("時間変更")
        action3 = context_menu.addAction("砂の色")
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
        global cycle,cn,time_full,tcn,p2
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
        text, ok = qid.getText(self, "計測時間の変更(分)", "値を入力してください:")
        if ok:
            ###print("入力された値:", text)
            if text.isdigit():
                tval=int(text)
                cycle=tval
                cn=1/click ###1秒間のクリック数
                time_full = 60*cycle  # 最終時間（秒）
                tcn=time_full*cn ###全クリック数
                p2=S3/tcn
        ###print("アクション2が選択されました　tval=",tval)
        print("tval,cycle,,cn,time_full,tcn,p2=",tval,cycle,cn,time_full,tcn,p2)

    def action3_triggered(self):
        ###print("アクション3が選択されました")    
        return  

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sand_timer = SandTimer()
    sys.exit(app.exec_())

"""
```

**修正点:**

1.  **`elapsed_time`変数の追加:**
    * `self.elapsed_time`変数で経過時間を秒単位で管理します。
    * `__init__`メソッドで`0`に初期化します。
2.  **`update_sand`メソッドの修正:**
    * `self.elapsed_time += self.click`で経過時間を更新します。
    * `if self.elapsed_time >= 180:`で3分（180秒）経過したかどうかを判定します。
        * 3分経過した場合、`self.timer.stop()`でタイマーを停止し、ラベルのテキストを「終了！」に変更して、`return`でメソッドを終了します。
    * 3分経過していない場合、ラベルのテキストを更新します。

**コードの動作:**

1.  タイマーが開始され、`self.click`秒ごとに`update_sand`メソッドが呼び出されます。
2.  `update_sand`メソッドで経過時間が更新され、3分経過したかどうかが判定されます。
3.  3分経過した場合、タイマーが停止し、ラベルのテキストが「終了！」に変更されます。
4.  3分経過していない場合、ラベルのテキストが更新され、タイマー処理が続行されます。

この修正により、タイマー処理が3分後に自動的に終了するようになりました。
"""