import math

G=9.81
GOAL_HEIGHT=3.048
m=0.173863
b=9.79369

def v_from_psi(psi):
    return m*psi+b

def psi_from_v(v):
    return (v-b)/m

def find_angle_psi(distance):
    best_angle=None
    best_psi=float('inf')
    for deg in range(5,85):
        th=math.radians(deg)
        cos_th=math.cos(th)
        sin_th=math.sin(th)
        vt=distance*math.tan(th)-GOAL_HEIGHT#vertical term
        if vt<=0: continue
        v=math.sqrt((G*distance**2)/(2*cos_th*cos_th*vt))
        psi=psi_from_v(v)
        if 0<psi<best_psi:
            best_psi=psi
            best_angle=deg
    if best_angle is None:
        raise ValueError("no solution")
    return best_angle,best_psi
