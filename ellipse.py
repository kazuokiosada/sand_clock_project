from math import *
import numpy as np

def get_arc_of_eclipse(cx,cy,a,b,θ1,θ2,step):
    """中心（0,0）の楕円上の弧を座標点列として求める
    a：横,b：縦,θ1：最初の角,θ2:最終の角,step：
    if(step>0 and θ1>θ2 or step<0 and θ1<θ2):
        print("step>0 and θ1>θ2 or step<0 and θ1<θ2: ",step,θ1,θ2)
    """
    xylist=[]
    for theta in np.arange(θ1,θ2+step,step):
        xylist.append((get_xy(a,b,theta)[0]+cx,get_xy(a,b,theta)[1]+cy))
    return xylist
###角度tでの座標
def get_xy(a,b,theta):
    t=radians(theta)
    r=a*b/sqrt(b*b*cos(t)**2+a*a*sin(t)**2)
    x=r*cos(t)
    y=r*sin(t)
    return x,-y

def get_another_cross_point(a,b,x1,y1,q):
    """a:横,b：縦,x1,y1:楕円上の点,q：(0,-q)：漏斗の頂点"""
    A=b**2+2*b/a*q*sqrt(a**2-x1**2)+q**2
    B=(b/a*sqrt(a**2-x1**2)+q)*q*x1
    C=(q**2-b**2)*x1**2
    x2=B/A+sqrt(B**2-A*C)/A if x1<0 else B/A-sqrt(B**2-A*C)/A
    y2=-b/a*sqrt(a**2-x2**2)
    return x2,y2

def get_tangent_points(a,b,q):
    """a:横,b：縦,q：(0,-q)：穴の頂点"""
    yt=-b**2/q
    xt=a*sqrt(1-(yt/b)**2)
    return (-xt,yt),(xt,yt)

def get_xy_from_theta(a,b,θ):
    """a,b,θ:度"""
    t=radians(θ)
    r=a*b/sqrt((b*cos(t))**2+(a*sin(t))**2)
    x=r*cos(t)
    y=r*sin(t)
    return x,y

def get_θ_from_xy(x,y):
    return degrees(atan2(y,x))## -180°< < 180°

def get_theta_from_xy(x,y):
    return atan2(y,x)