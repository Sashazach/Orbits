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
        tan_th=math.tan(th)
        
        # Calculate velocity needed to pass through (distance, GOAL_HEIGHT)
        v_squared = (G*distance**2)/(2*cos_th**2*(distance*tan_th-GOAL_HEIGHT))
        
        # Check if solution is valid (no negative under square root)
        if v_squared > 0:
            v = math.sqrt(v_squared)
            psi = psi_from_v(v)
            if 0 < psi < best_psi:
                best_psi = psi
                best_angle = deg
                
    if best_angle is None:
        raise ValueError("no solution")
    return best_angle, best_psi

print(find_angle_psi(30))
