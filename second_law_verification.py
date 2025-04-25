import numpy as np
import math
from models import Planet, System 
import matplotlib.pyplot as plt

# constants
G = 6.67430e-11
M_sun = 1.989e30
M_body = 1e22

ecc = 0.7
r_peri = 1.471e11
a = r_peri / (1 - ecc)  #semimajor axi

#per velocity
v_peri = np.sqrt(G * M_sun * (1 + ecc) / r_peri)

sun = Planet(name="Sun", mass=M_sun, position=[0, 0], velocity=[0, 0], color='yellow')
init_pos = [r_peri, 0]
comet = Planet(name="Comet", mass=M_body, position=init_pos.copy(), velocity=[0, v_peri], color='cyan')
system = System(host=sun, planets=[comet])

# sim params
dt = 3600  # 60 * 60 secs
steps_per_sweep = 100
dt_sweep = dt * steps_per_sweep
years = 3
total_time = 3.154e7 * years
n_steps = int(total_time / dt)

# sim loop
print("Running simulation...")
positions = [np.array(comet.position)]
for step in range(n_steps):
    system.step_forward(dt)
    positions.append(np.array(comet.position))
    if (step + 1) % (n_steps // 10) == 0:
        print(f"{(step + 1) / n_steps * 100:.0f}% complete")

print("Simulation done.")
print(f"Steps: {len(positions)}")
print(f"Steps per sweep: {steps_per_sweep}")

# area calc
areas = []

for i in range(0, len(positions) - steps_per_sweep, steps_per_sweep):
    """
        we break the positions into larger pieces to make the area calculation less subject
        to random noise (even though it still is a little bit)
    """
    
    p1 = positions[i]
    p2 = positions[i + steps_per_sweep]
    # shoelace formula (triangular area, had to google it)
    A = 0.5 * abs(p1[0] * p2[1] - p2[0] * p1[1])
    areas.append(A)
if len(areas) > 1:
    avg = np.mean(areas)
    std = np.std(areas)
    cv = (std / avg) * 100 if avg != 0 else float('inf')

    print('\n')
    print("Kepler's 2nd Law")
    print(f"Interval: {dt_sweep / 86400:.2f} days")
    print(f"Intervals: {len(areas)}")
    print(f"Avg area: {avg:.4e} m^2")
    print(f"Standard dev: {std:.4e}")
    print(f"Variation: {cv:.2f}%")
    if cv < 1.0:
        print("Result: Kepler verified (constant areal sweep which is what the second law says).")
    else:
        print("Result: Variation too high!")
else:
    print("Something got messed up.")

if len(areas) > 1:
    equal_values = np.ones(len(areas))
    colors = plt.cm.viridis(np.linspace(0, 1, len(areas)))

    plt.figure(figsize=(8, 8))
    wedges, texts = plt.pie(equal_values, colors=colors, startangle=90, counterclock=False)
    plt.title(f"Kepler's Second Law Verification\nEqual Areas Swept in Equal Time Intervals ({dt_sweep/86400:.2f} days each)", pad=20)

    center_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(center_circle)

    plt.text(0, 0, f"{len(areas)}\nIntervals", ha='center', va='center', fontsize=12)

    plt.text(0.5, -0.1, 
             f"Average Area: {avg:.3e} m^2\nVariation: {cv:.2f}% - {'Verified' if cv < 1.0 else 'High Variation!'}", 
             ha='center', va='center', transform=fig.transFigure)

    plt.axis('equal')  
    plt.tight_layout()
    plt.show()
