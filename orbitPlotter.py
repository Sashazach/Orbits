from models import Planet, System
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
from plotter3d import Planet3d, System3d

def get_user_input3d():
    predefined_planets = {
        "Mercury": Planet3d("Mercury",[5.7e10],[0],[0],"silver",2.44e6),
        "Venus":   Planet3d("Venus",[1.075e11],[0],[0],"yellow",6.052e6),
        "Earth":   Planet3d("Earth",[1.471e11],[0],[0],"deepskyblue",6.371e6),
        "Mars":    Planet3d("Mars",[2.066e11],[0],[0],"orangered",3.389e6),
        "Jupiter": Planet3d("Jupiter",[7.4052e11],[0],[0],"orange",6.9911e7),
        "Saturn":  Planet3d("Saturn",[1.3526e12],[0],[0],"gold",5.8232e7),
        "Uranus":  Planet3d("Uranus",[2.7413e12],[0],[0],"cyan",2.5362e7),
        "Neptune": Planet3d("Neptune",[4.4445e12],[0],[0],"dodgerblue",2.4622e7),
        "Pluto":   Planet3d("Pluto",[4.4368e12],[0],[0],"sandybrown",1.1883e6)
    }
    return list(predefined_planets.values())


def get_user_input2d():
    predefined_planets = {
        "Mercury": {
            "name": "Mercury",  
            "mass": 3.3011e23,
            "color": "silver",  
            "position": [5.7e10, 0],
            "velocity": [0, 47362],    
        },
        "Venus": {
            "name": "Venus",
            "mass": 4.8675e24,
            "color": "yellow",
            "position": [1.075e11, 0],
            "velocity": [0, 35020],
        },
        "Earth": {
            "name": "Earth",
            "mass": 5.972e24,
            "color": "deepskyblue",
            "position": [1.471e11, 0],  
            "velocity": [0, 30300],    
        },
        "Mars": {
            "name": "Mars",
            "mass": 6.4171e23,
            "color": "orangered",  
            "position": [2.066e11, 0],  
            "velocity": [0, 26500],
        },
        "Jupiter": {
            "name": "Jupiter",
            "mass": 1.8982e27,
            "color": "orange",
            "position": [7.4052e11, 0],
            "velocity": [0, 13720],
        },
        "Saturn": {
            "name": "Saturn",
            "mass": 5.6834e26,
            "color": "gold",
            "position": [1.3526e12, 0],
            "velocity": [0, 10180],
        },
        "Uranus": {
            "name": "Uranus",
            "mass": 8.6810e25,
            "color": "cyan", 
            "position": [2.7413e12, 0],
            "velocity": [0, 7110],
        },
        "Neptune": {
            "name": "Neptune",
            "mass": 1.02413e26,
            "color": "dodgerblue",  
            "position": [4.4445e12, 0],
            "velocity": [0, 5500],
        },
        "Pluto": {
            "name": "Pluto",
            "mass": 1.303e22,
            "color": "sandybrown", 
            "position": [4.4368e12, 0], 
            "velocity": [0, 4670],
        }
    }
    
    # get trail selection from user
    while True:
        trail_input = input("Do you want to show orbit trails? (yes/no): ").lower()
        if trail_input in ['yes', 'no']:
            show_trails = (trail_input == 'yes')
            break
        print("Please enter 'yes' or 'no'")
    
    # display list of avaliable planets
    print("\nAvailable planets:")
    for planet_name in predefined_planets.keys():
        print(f"- {planet_name}")
    
    # let user select planets
    selected_planets = []
    
    while True:
        try:
            num_planets = int(input("\nHow many planets would you like to include? "))
            if num_planets < 1:
                print("Please select at least one planet please")
                continue
            if num_planets > len(predefined_planets):
                print(f"Maximum number of planets is {len(predefined_planets)}")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    for i in range(num_planets):
        while True:
            print(f"\nSelect planet {i+1}:")
            selection = input("Enter planet name: ").strip()
            
            # check if planit name exists (without case sensitivity)
            planet_found = False
            for planet_name in predefined_planets.keys():
                if selection.lower() == planet_name.lower():
                    selected_planets.append(predefined_planets[planet_name].copy())
                    print(f"Added {planet_name} to simulation.")
                    planet_found = True
                    break
            
            if planet_found:
                break
            else:
                print(f"Planet '{selection}' not found. Please enter a valid planet name.")
    
    return selected_planets, show_trails

def simulate_orbits(system, show_trails=True, days=365, steps_per_day=24, sub_steps=2000):

    dt = 86400 / steps_per_day  
    dt_calc = dt / sub_steps     
    steps_per_frame = 5          

    fig, ax = plt.subplots(figsize=(10, 10))
    
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.grid(True, color='gray', alpha=0.3)
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    
    positions_x = []
    positions_y = []
    
    for planet in system.planets:
        positions_x.append(planet.position[0])
        positions_y.append(planet.position[1])
    
    temp_system = System(host=system.host, planets=[Planet(p.name, p.mass, p.position.copy(), p.velocity.copy(), p.color) for p in system.planets])
    
    total_steps = days * steps_per_day
    sample_rate = max(1, total_steps // 100)
    
    for step in range(0, total_steps, sample_rate):
        for _ in range(sample_rate):
            temp_system.step_forward(dt)
        
        for planet in temp_system.planets:
            positions_x.append(planet.position[0])
            positions_y.append(planet.position[1])
    
    max_abs_x = max(abs(x) for x in positions_x)
    max_abs_y = max(abs(y) for y in positions_y)
    max_position = max(max_abs_x, max_abs_y)
    
    limit = max_position * 1.1
    
    lines = []
    points = []
    
    host_point, = ax.plot([], [], 'yo', markersize=10, label=system.host.name)
    points.append(host_point)
    
    colors = []
    for planet in system.planets:
        if show_trails:
            line, = ax.plot([], [], '-', color=planet.color, alpha=0.3)
            lines.append(line)
        
        point, = ax.plot([], [], 'o', color=planet.color, markersize=6, label=planet.name)
        points.append(point)
        colors.append(planet.color)
    
    orbit_trails = [[] for _ in system.planets] if show_trails else None
    
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_xlabel("X Position (m)")
    ax.set_ylabel("Y Position (m)")
    ax.set_title("Planetary System Simulation")
    ax.grid(True, color='gray', alpha=0.3)
    ax.set_aspect('equal')
    
    legend = ax.legend(loc='upper right', bbox_to_anchor=(1.05, 1))
    plt.setp(legend.get_texts(), color='white')
    
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    
    def init():
        host_point.set_data([system.host.position[0]], [system.host.position[1]])
        for i, planet in enumerate(system.planets):
            if show_trails:
                lines[i].set_data([], [])
            points[i+1].set_data([planet.position[0]], [planet.position[1]])
        return (lines + points) if show_trails else points
    
    def update(frame):
        # Perform multiple smaller steps for accuracy within one visual update interval
        for _ in range(steps_per_frame * sub_steps):
            system.step_forward(dt_calc)
        
        host_point.set_data([system.host.position[0]], [system.host.position[1]])
        
        for i, planet in enumerate(system.planets):
            if show_trails:
                orbit_trails[i].append((planet.position[0], planet.position[1]))
                
                if len(orbit_trails[i]) > 2000:
                    orbit_trails[i].pop(0)
                
                x_trail = [p[0] for p in orbit_trails[i]]
                y_trail = [p[1] for p in orbit_trails[i]]
                lines[i].set_data(x_trail, y_trail)
            
            points[i+1].set_data([planet.position[0]], [planet.position[1]])
        
        return (lines + points) if show_trails else points
    
    anim = animation.FuncAnimation(
        fig, update, init_func=init,
        frames=days * steps_per_day // steps_per_frame, # Keep frames based on visual steps
        interval=20,
        blit=True,
        repeat=True 
    )
    
    plt.tight_layout()
    
    return fig, anim

def main():
    while True:
        mode = input("Enter the mode you want to run the simulation in (2d/3d): ")
        if mode in ["2d", "3d"]:
            break
        else:
            print("Please enter a valid mode")

    if mode == "2d":
        planet_data_list, show_trails = get_user_input2d()
        sun = Planet(name="Sun", mass=1.989e30, position=[0, 0], velocity=[0, 0])
        
        G=6.67430e-11
        planets=[]
        for planet_data in planet_data_list:
            pos=planet_data["position"].copy()
            r=math.hypot(pos[0],pos[1])
            v=math.sqrt(G*sun.mass/r)

            # if the velocity is negative, we need to flip the velocity (to make sure we go in the correct direction)
            vel = [
                0,
                v if planet_data["velocity"][1] >= 0 else -v
            ]
            planets.append(Planet(planet_data["name"],planet_data["mass"],pos,vel,planet_data["color"]))
        
        solar_system = System(host=sun, planets=planets)
        fig, anim = simulate_orbits(solar_system, show_trails=show_trails)
        
        plt.show(block=True)
    
    elif mode == "3d":
        planet3d_list = get_user_input3d()

        sun = Planet("Sun", 1.989e30, [0, 0, 0], [0, 0, 0])
        G = 6.67430e-11
        masses = {"Mercury":3.3011e23,"Venus":4.8675e24,"Earth":5.972e24,"Mars":6.4171e23,"Jupiter":1.8982e27,"Saturn":5.6834e26,"Uranus":8.6810e25,"Neptune":1.02413e26,"Pluto":1.303e22}
        sim_planets = []

        for p3d in planet3d_list:
            x,y = p3d.xPositions[0], p3d.yPositions[0]
            r = math.hypot(x,y)
            v = math.sqrt(G * sun.mass / r)
            vx,vy = 0,v
            sim_planets.append(Planet(p3d.name, masses[p3d.name], [x,y], [vx,vy], p3d.color))

        system_sim = System(host=sun, planets=sim_planets)
        # Extend simulation length significantly (from 2000 to 20000 days)
        # Decrease the days but increase steps_per_day for higher temporal resolution
        days,steps_per_day,sub_steps = 1000,96,10
        dt = 86400/steps_per_day; dt_calc = dt/sub_steps; frames = days*steps_per_day
        
        # Sample rate - collect 1 point per day (reduced from 5 days)
        # to ensure smooth orbital curves
        # to keep the animation smooth but data size manageable
        # Collect points every 6 hours (4 points per day) for smoother orbits
        sample_rate = steps_per_day // 4
        
        print(f"Running {days} day simulation...")
        
        for _ in range(frames):
            for __ in range(sub_steps): system_sim.step_forward(dt_calc)
            
            # Only collect position data at the sample rate
            if _ % sample_rate == 0:
                for i,p in enumerate(sim_planets):
                    planet3d_list[i].xPositions.append(p.position[0])
                    planet3d_list[i].yPositions.append(p.position[1])
                    planet3d_list[i].zPositions.append(0)
                
                # Print progress update
                if _ % (frames // 10) < sample_rate:
                    print(f"Simulation {_ / frames * 100:.1f}% complete")
        
        print("Simulation complete. Preparing visualization...")
        
        # Disable orbit paths as requested
        system3d = System3d(planets=planet3d_list, show_orbit_paths=False)
        # Use a very slow speed factor (0.1 = 10x slower) so animation is easily visible
        print("Starting smooth animation...")
        # Use a moderate speed factor with the new smooth interpolation
        system3d.animateSimulation(speed_factor=0.5)

if __name__ == '__main__':
    main() 
