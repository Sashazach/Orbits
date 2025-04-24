import matplotlib.pyplot as plt
import math

class Planet:
    def __init__(self, name: str, mass: float, position: list[float], velocity: list[float], color: str = 'blue'):
        self.name = name
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.color = color

class System:
    def __init__(self, host: Planet, planets: list[Planet]):
        self.host = host
        self.planets = planets

    def step_forward(self, dt: float):
        """Velocity Verlet integrator in two dimensions."""
        G = 6.67430e-11

        accelerations = []
        for planet in self.planets:
            rx = planet.position[0] - self.host.position[0]
            ry = planet.position[1] - self.host.position[1]
            r = math.hypot(rx, ry)
            r_cubed = r**3 if r else 1e-30
            ax = -G * self.host.mass * rx / r_cubed
            ay = -G * self.host.mass * ry / r_cubed
            accelerations.append((ax, ay))

        half_dt = 0.5 * dt

        for idx, planet in enumerate(self.planets):
            acc = accelerations[idx]
            planet.velocity[0] += acc[0] * half_dt
            planet.velocity[1] += acc[1] * half_dt

            planet.position[0] += planet.velocity[0] * dt
            planet.position[1] += planet.velocity[1] * dt

        new_accelerations = []
        for planet in self.planets:
            rx = planet.position[0] - self.host.position[0]
            ry = planet.position[1] - self.host.position[1]
            r = math.hypot(rx, ry)
            r_cubed = r**3 if r else 1e-30
            ax = -G * self.host.mass * rx / r_cubed
            ay = -G * self.host.mass * ry / r_cubed
            new_accelerations.append((ax, ay))

        for idx, planet in enumerate(self.planets):
            new_acc = new_accelerations[idx]
            planet.velocity[0] += new_acc[0] * half_dt
            planet.velocity[1] += new_acc[1] * half_dt

    def plot_orbits(self):
        fig, ax = plt.subplots(figsize=(10, 10))
        
        ax.plot(self.host.position[0], self.host.position[1], 'yo', markersize=10, label=self.host.name) 

        max_position = 0
        for planet in self.planets:
            ax.plot(planet.position[0], planet.position[1], 'o', color=planet.color, markersize=6, label=planet.name)
            max_position = max(max_position, abs(planet.position[0]), abs(planet.position[1]))

        limit = max_position * 1.1
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)

        ax.set_xlabel("X Position (m)")
        ax.set_ylabel("Y Position (m)")
        ax.set_title("Planetary System Orbits")
        ax.legend(loc='upper right', bbox_to_anchor=(1.05, 1), borderaxespad=0.) 
        ax.set_aspect('equal', adjustable='box') 
        plt.grid(True)
        
        plt.tight_layout() 
        plt.show() 
