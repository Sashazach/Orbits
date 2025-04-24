from models import Planet, System
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import math

# constants
G = 6.67430e-11
sun_mass = 1.989e30
planet_mass = 1e22 # smaller mass, less effect on sun if we modelled it

#make these high so that the orbit is more elliptx`ical
e = 0.7  # high eccentricity
rp = 1.471e11 # perihelion distance (closest) (also earth's same distances)
a = rp / (1 - e) # semi-major axis

# this calculates the speed at which the comet travels when it is closest to the sun
vp_mag = np.sqrt(G * sun_mass * (1 + e) / rp)

sun = Planet(name="Sun", mass=sun_mass, position=[-2e10, 0], velocity=[0, 0], color='yellow')
# place planet at perihelion on the positive x-axis relative to sun offset
planet_initial_pos = [sun.position[0] + rp, 0]
planet = Planet(name="Comet (e=0.7)", mass=planet_mass, position=planet_initial_pos, velocity=[0, vp_mag], color='cyan')
solar_system = System(host=sun, planets=[planet])

dt = 3600 # time step (1 hour)
fig, ax = plt.subplots(figsize=(10, 10))

fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.grid(True, color='gray', alpha=0.3)
ax.tick_params(colors='white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.title.set_color('white')

#calculate the fixed second focus position
sun_pos_initial = np.array(sun.position)  #convert sun position to array
planet_pos_initial = np.array(planet.position)  #convert planet position to array
vec_sun_planet_initial = planet_pos_initial - sun_pos_initial  #vector from sun to planet
rp_check = np.linalg.norm(vec_sun_planet_initial)  #measure perihelion distance (the distance where it is closest to the host)
a = rp_check / (1 - e)  # calculate semi-major axis
c = a * e  # distance from center to focus
focus_direction = vec_sun_planet_initial / rp_check  # unit vector to perihelion
focus_b_pos = sun_pos_initial - focus_direction * (2 * c)  # locate second focus

planet_trail = []

planet_point, = ax.plot([], [], 'o', color=planet.color, markersize=8, label=planet.name)
sun_point, = ax.plot([], [], 'o', color=sun.color, markersize=12, label='Sun (Focus A)')
trail_line, = ax.plot([], [], '-', color=planet.color, alpha=0.3)
focal_line_1, = ax.plot([], [], '-', color='red', alpha=0.5)  # line between foci
focal_line_2, = ax.plot([], [], '-', color='green', alpha=0.5) # line focus a to planet
focal_line_3, = ax.plot([], [], '-', color='blue', alpha=0.5)  # line focus b to planet
focal_lines_together, = ax.plot([], [], '-', color='purple', alpha=0.5)
focus_b_point, = ax.plot([], [], 'o', color='white', markersize=4, label='Focus B')

# Text elements for displaying distances
dist_text_a = ax.text(0.02, 0.95, '', transform=ax.transAxes, verticalalignment='top', fontsize=9, color='green')
dist_text_b = ax.text(0.02, 0.90, '', transform=ax.transAxes, verticalalignment='top', fontsize=9, color='blue')
dist_text_c = ax.text(0.02, 0.85, '', transform=ax.transAxes, verticalalignment='top', fontsize=9, color='purple')

def init():
    #initialize a bunch of values that we can use for the rest of the simulation (lines, trails, text)
    sun_point.set_data([sun_pos_initial[0]], [sun_pos_initial[1]])
    focus_b_point.set_data([focus_b_pos[0]], [focus_b_pos[1]])
    focal_line_1.set_data([sun_pos_initial[0], focus_b_pos[0]], [sun_pos_initial[1], focus_b_pos[1]])
    planet_point.set_data([], [])
    trail_line.set_data([], [])
    focal_line_2.set_data([], [])
    focal_line_3.set_data([], [])

    dist_text_c.set_text('')
    dist_text_a.set_text('')
    dist_text_b.set_text('')
    focal_lines_together.set_data([], [])
    return planet_point, sun_point, trail_line, focal_line_1, focal_line_2, focal_line_3, focus_b_point, dist_text_a, dist_text_b, dist_text_c, focal_lines_together
def update(frame):
    # increase steps per frame for faster movement, especially near aphelion
    steps_per_frame = 120 
    for _ in range(steps_per_frame):
        solar_system.step_forward(dt)
    
    planet_pos = np.array(planet.position)
    sun_pos = np.array(sun.position) 
    
    planet_trail.append(planet_pos)
    # note: we could increase trail length, but this is good since we want fast performance for verification
    if len(planet_trail) > 1000:
        planet_trail.pop(0)
    
    planet_point.set_data([planet_pos[0]], [planet_pos[1]])
    
    trail_x = [pos[0] for pos in planet_trail]
    trail_y = [pos[1] for pos in planet_trail]
    trail_line.set_data(trail_x, trail_y)
    
    focal_line_2.set_data([sun_pos[0], planet_pos[0]], [sun_pos[1], planet_pos[1]])
    focal_line_3.set_data([focus_b_pos[0], planet_pos[0]], [focus_b_pos[1], planet_pos[1]])
    # calculate and update distances text
    dist_a_planet = np.linalg.norm(planet_pos - sun_pos)
    dist_b_planet = np.linalg.norm(planet_pos - focus_b_pos)
    dist_text_a.set_text(f'Focus A to Planet: {dist_a_planet:.3e} m')
    dist_text_b.set_text(f'Focus B to Planet: {dist_b_planet:.3e} m')
    dist_text_c.set_text(f'Sum (Foci-Planet): {dist_a_planet + dist_b_planet:.3e} m')

    # set axis limits only once
    if frame == 0:
        # estimate distance of aphelion
        ra = a * (1 + e)
        max_dist = ra * 1.1 
        center = (sun_pos_initial + focus_b_pos) / 2 # center plot around ellipse's center
        ax.set_xlim(center[0] - max_dist * 1.1, center[0] + max_dist * 1.1)
        ax.set_ylim(center[1] - max_dist * 1.1, center[1] + max_dist * 1.1)
        print("Setting the axis limits... (DEBUG)")

    
    # only return artists that change
    return planet_point, trail_line, focal_line_2, focal_line_3, dist_text_a, dist_text_b, dist_text_c, focal_lines_together

ax.set_aspect('equal')

focal_line_2.set_label('Line Focus A-Planet')
focal_line_3.set_label('Line Focus B-Planet')
focal_lines_together.set_label('Lines added together')
legend = ax.legend(loc='upper right')
plt.setp(legend.get_texts(), color='white')
anim = animation.FuncAnimation(fig, update, init_func=init, frames=2000, interval=1, blit=True)
plt.show() 
