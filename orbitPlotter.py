from models import Planet, System
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
from plotter3d import Planet3d, System3d

def get_user_input3d():
    predefined_planets = {
        "Mercury": Planet3d(
            name="Mercury",
            xPositions=[5.7e10],
            yPositions=[0],
            zPositions=[0],
            color="silver",
            radius=2.44e6
        ),
        "Venus": Planet3d(
            name="Venus",
            xPositions=[1.075e11],
            yPositions=[0],
            zPositions=[0],
            color="yellow",
            radius=6.052e6
        ),
        "Earth": Planet3d(
            name="Earth",
            xPositions=[1.471e11],
            yPositions=[0],
            zPositions=[0],
            color="deepskyblue",
            radius=6.371e6
        ),
        "Mars": Planet3d(
            name="Mars",
            xPositions=[2.066e11],
            yPositions=[0],
            zPositions=[0],
            color="orangered",
            radius=3.389e6
        ),
        "Jupiter": Planet3d(
            name="Jupiter",
            xPositions=[7.4052e11],
            yPositions=[0],
            zPositions=[0],
            color="orange",
            radius=6.9911e7
        ),
        "Saturn": Planet3d(
            name="Saturn",
            xPositions=[1.3526e12],
            yPositions=[0],
            zPositions=[0],
            color="gold",
            radius=5.8232e7
        ),
        "Uranus": Planet3d(
            name="Uranus",
            xPositions=[2.7413e12],
            yPositions=[0],
            zPositions=[0],
            color="cyan",
            radius=2.5362e7
        ),
        "Neptune": Planet3d(
            name="Neptune",
            xPositions=[4.4445e12],
            yPositions=[0],
            zPositions=[0],
            color="dodgerblue",
            radius=2.4622e7
        ),
        "Pluto": Planet3d(
            name="Pluto",
            xPositions=[4.4368e12],
            yPositions=[0],
            zPositions=[0],
            color="sandybrown",
            radius=1.1883e6
        )
    }

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
    
    return selected_planets


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

def simulate_orbits(system, show_trails=True, days=365, steps_per_day=24):
    dt = 86400 / steps_per_day
    
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
        for _ in range(5):
            system.step_forward(dt)
        
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
        frames=days * steps_per_day // 5,
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
        sun_offset = -2e10
        sun = Planet(name="Sun", mass=1.989e30, position=[sun_offset, 0], velocity=[0, 0])
        
        planets = []
        for planet_data in planet_data_list:
            planet = Planet(
                name=planet_data["name"],
                mass=planet_data["mass"],
                position=planet_data["position"],
                velocity=planet_data["velocity"],
                color=planet_data["color"]
            )
            planets.append(planet)
        
        solar_system = System(host=sun, planets=planets)
        fig, anim = simulate_orbits(solar_system, show_trails=show_trails)
        
        plt.show(block=True)
    
    elif mode == "3d":
        planet_data_list = get_user_input3d()
        system3d = System3d(planets=planet_data_list)
        system3d.animateSimulation()

if __name__ == '__main__':
    main() 
