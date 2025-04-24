import matplotlib.pyplot as plt
import math
from plotter3d import Planet3d, System3d

class Planet:
    def __init__(self, name: str, mass: float, position: list[float], velocity: list[float], color: str = 'blue', zPosition: float = 0, zVelocity: float = 0):
        self.name = name
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.color = color 
        self.zPosition = zPosition
        self.zVelocity = zVelocity

class System:
    def __init__(self, host: Planet, planets: list[Planet], mode: str = "2d", dimensionalPlanets: list[Planet3d] = []):
        self.host = host
        self.planets = planets
        self.mode = mode

        self.xPositionLog = []
        self.yPositionLog = []
        self.zPositionLog = []

        self.system3d = None
        if self.mode == "3d":
            self.system3d = System3d(dimensionalPlanets)

    def step_forward(self, dt: float):
        G = 6.67430e-11 
        
        #loop through and update each planet's data
        for planet in self.planets:
            # calcuate positon relative to the host (sun)
            rx = planet.position[0] - self.host.position[0]
            ry = planet.position[1] - self.host.position[1]
            if self.mode == "3d":
                rz = planet.position[2] - self.host.position[2]
            
            # calculate r (distanse from host to planet)
            if self.mode == "2d":
                r = math.sqrt(rx**2 + ry**2)
                r_cubed = r**3
                
                ax = -G * self.host.mass * rx / r_cubed
                ay = -G * self.host.mass * ry / r_cubed
            elif self.mode == "3d":
                r = math.sqrt(rx**2 + ry**2 + rz**2)
                r_cubed = r**3
                
                ax = -G * self.host.mass * rx / r_cubed
                ay = -G * self.host.mass * ry / r_cubed
                az = -G * self.host.mass * rz / r_cubed
            # update velocty (vx, vy)
            # v_new = v_old + a * dt
            planet.velocity[0] += ax * dt
            planet.velocity[1] += ay * dt
            if self.mode == "3d":
                planet.velocity[2] += az * dt

            planet.position[0] += planet.velocity[0] * dt
            planet.position[1] += planet.velocity[1] * dt
            if self.mode == "3d":
                planet.position[2] += planet.velocity[2] * dt

            if self.mode == "3d":
                self.xPositionLog.append(planet.position[0])
                self.yPositionLog.append(planet.position[1])
                self.zPositionLog.append(planet.position[2])

    def plot_orbits(self):
        if self.mode == "2d":
            fig, ax = plt.subplots(figsize=(10, 10))
        
            # we start by ploting the host of the system
            # 'yo' defines a yellow circle and is a string arg
            ax.plot(self.host.position[0], self.host.position[1], 'yo', markersize=10, label=self.host.name) 

            max_position = 0
            for planet in self.planets:
                ax.plot(planet.position[0], planet.position[1], 'o', color=planet.color, markersize=6, label=planet.name)
                max_position = max(max_position, abs(planet.position[0]), abs(planet.position[1]))

            # set axis limts with 10% padding
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
