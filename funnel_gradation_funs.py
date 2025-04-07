import tkinter as tk
import ellipse as ec
from math import *
w=200
h=400
###上の楕円
cx=100
cy=50
a=50
b=20
###砂下の頂点
###q=50
q=a*tan(radians(37))
###下の楕円
cx2=100
cy2=80
###q2=100
q2=(a+18)*tan(radians(55))
###下のガラスの上の円
cy3=280
cy4=310
"""
###定型の楕円について、弧を作る
def get_xy_ulrl_arc_of_eclipse(a,b,q,upOrLow):
    (xtl,ytl),(xtr,ytr)=ec.get_tangent_points(a,b,q)
    θl=ec.get_θ_from_xy(xtl,ytl)
    θr=ec.get_θ_from_xy(xtr,ytr)
    ###
    if upOrLow=="U" and θl<θr:
        θl+=360
        ###print("修正　θl=",θl,"θr=",θr)
    elif upOrLow=="L" and θl>θr:
        θr+=360
        ###print("修正　θl=",θl,"θr=",θr)
    ###楕円点列   
    if upOrLow == "U":
        xylistr=ec.get_arc_of_eclipse(a,b,θr,90,1)
        xylistr.append((0,-b))
        xylistl=ec.get_arc_of_eclipse(a,b,90,θl,1)
        xylistl.insert(0,(0,-b))
        print("θr,90,90,θl=",θr,90,90,θl)        
        print("upOrLow,θ1,θ2=",upOrLow,θl,θr)
        print("len(xylistr),len(xylistl)=",len(xylistr),len(xylistl))
    else:
        t90=270
        if θl<0:
            t90=-90 
        xylistr=ec.get_arc_of_eclipse(a,b,t90,θr,1)
        xylistr.insert(0,(0,b))
        xylistl=ec.get_arc_of_eclipse(a,b,θl,t90,1)
        xylistl.append((0,b))
    ###
    return xylistr,xylistl
###予め作っておくもの
xyur1,xyul1=get_xy_ulrl_arc_of_eclipse(a,b,q,"U")###右から左へ
xylr1,xyll1=get_xy_ulrl_arc_of_eclipse(a,b,-q,"L")###左から右へ
xylr2,xyll2=get_xy_ulrl_arc_of_eclipse(a+18,b+12,q2,"L")###左から右へ
####一気に穴
def create_gradient_hole(canvas,cx,cy,a,b,q,color1,color2,csteps):
    ###接点
    (xtl,ytl),(xtr,ytr)=ec.get_tangent_points(a,b,q)
    θl=ec.get_θ_from_xy(xtl,ytl)
    θr=ec.get_θ_from_xy(xtr,ytr)
    if(θl<θr):
        θl+=360
    ###
    xyr=[]
    xyl=[]
    ###右側
    steps=max(2,min(csteps,int(90-θr)))###グラデーション諧調数
    xystep=max(1,(90-θr+1)/steps)###ひとつのグラデーションあたりの座標の個数
    ###print("右側　steps=",steps," xystep=",xystep)
    for i in range(steps):
        upoints=[]
        lpoints=[]
        for θ in range(i*xystep+θr,(i+1)*xystep+θr):
            (x1,y1)=ec.get_xy_from_theta(a,b,θ)
            (x2,y2)=ec.get_another_cross_point(a,b,x1,y1,q)
            upoints.append((x1,y1))
            lpoints.insert((x2,y2))
        ###
        points=upoints+lpoints
        color=get_gradient_color(color1,color2,steps,i)
        ###
        canvas.create_polygon(points, fill=color, outline=color)
    ###左側
    steps=max(2,min(csteps,int(θl-90)))###グラデーション諧調数
    xystep=max(1,(θl-90+1)/steps)###ひとつのグラデーションあたりの座標の個数
    for i in range(steps):
        upoints=[]
        lpoints=[]
        for θ in range(i*xystep+90,(i+1)*xystep+90):
            (x1,y1)=ec.get_xy_from_theta(a,b,θ)
            (x2,y2)=ec.get_another_cross_point(a,b,x1,y1,q)
            upoints.append((x1,y1))
            lpoints.insert((x2,y2))
        ###
        points=upoints+lpoints
        color=get_gradient_color(color1,color2,steps,i)
        ###
        canvas.create_polygon(points, fill=color, outline=color)
"""

###漏斗
def create_gradient_funnel(canvas,cx,cy, a,b,upOrLow,q,color1, color2, csteps,tags):
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
        """
        print("-90,θr,θl,-90=",-90,θr,θl,-90)
        print("upOrLow,θ1,θ2=",upOrLow,θl,θr)
        print("len(xylistr),len(xylistl)=",len(xylistr),len(xylistl))
        """
    ##xylistl.insert(0,xylistr[-1])
    ##xylistr.append(xylistl[0])
    ###漏斗の描写
    ###右側
    steps=min(csteps,len(xylistr))
    xystep=max(1,int(len(xylistr)/steps))
    ###print("右側　steps=",steps," xystep=",xystep)
    for i in range(steps):
        points=[(cx,cy+q)]
        k=(i+1)*xystep
        if(i==steps-1):
            k=len(xylistl)
        for j in range(i*xystep,k):
            points.append(xylistr[j])
        ###
        color=get_gradient_color(color1,color2,steps,i)###明→暗
        if upOrLow == "U":
            color=get_gradient_color(color2,color1,steps,i)###暗→明
        ###
        canvas.create_polygon(points, fill=color, outline=color,tags=tags)
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
        color=get_gradient_color(color2,color1,steps,i)###暗→明
        if upOrLow == "U":
            color=get_gradient_color(color1,color2,steps,i)###明→暗
        ###
        canvas.create_polygon(points, fill=color, outline=color, tags=tags)
def create_gradient_cylinder(canvas,cx,cy,cx2,cy2,a,b,color1, color2, csteps,tags):
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
        color=get_gradient_color(color1,color2,steps,i)
        ###
        canvas.create_polygon(points, fill=color, outline=color,tags=tags)
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
        color=get_gradient_color(color2,color1,steps,i)
        ###
        canvas.create_polygon(points, fill=color, outline=color,tags=tags)

def create_lower_disc(canvas,cx,cy,a,b,aa,bb,color,tags):
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
    canvas.create_polygon(xylist,fill=color,tags=tags)

def get_gradient_color(color1,color2,steps,i):
    ###print("i steps color1 color2",i,steps,color1,color2)
    ratio= i / (steps - 1)
    r = int(color1[0] + (color2[0] - color1[0]) * ratio)
    g = int(color1[1] + (color2[1] - color1[1]) * ratio)
    b = int(color1[2] + (color2[2] - color1[2]) * ratio)
    color = '#%02x%02x%02x' % (r, g, b)
    return color
