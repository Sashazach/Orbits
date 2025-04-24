#a file to plot the orbits of the planets in 3d (requires z axis data)

import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv

SCALE = 1e9
SIZE_MULT = 2000

class Planet3d:
    def __init__(self, name: str, xPositions: list[float], yPositions: list[float], zPositions: list[float], color: str = 'blue', radius: float = 1):
        self.name = name
        self.xPositions = xPositions
        self.yPositions = yPositions
        self.zPositions = zPositions
        self.color = color
        self.radius = radius

        self.xPosition = self.xPositions[0]
        self.yPosition = self.yPositions[0]
        self.zPosition = self.zPositions[0]

        self.mesh = pv.Sphere(radius=max(self.radius/SCALE*SIZE_MULT,0.5), center=(self.xPosition/SCALE, self.yPosition/SCALE, self.zPosition/SCALE))

    def get_position(self):
        return [self.xPosition, self.yPosition, self.zPosition]

    def set_position(self, xPosition: float, yPosition: float, zPosition: float):
        #calculate the difference because that's what the translate function takes
        dx = (xPosition - self.xPosition)/SCALE
        dy = (yPosition - self.yPosition)/SCALE
        dz = (zPosition - self.zPosition)/SCALE

        self.xPosition = xPosition
        self.yPosition = yPosition
        self.zPosition = zPosition

        self.mesh.translate([dx, dy, dz], inplace=True)

class System3d  :
    def __init__(self, planets: list[Planet3d]):
        self.planets = planets
        self.plotter = pv.Plotter()
        self.plotter.set_background("black")
        self.renderedPlanets = [self.plotter.add_mesh(p.mesh, color=p.color) for p in self.planets]
        self.plotter.view_isometric(); self.plotter.reset_camera()

    def update_positions(self, indexOfSimulation: int):
        for i in range(len(self.planets)):
            inputPlanet = self.planets[i]
            inputPlanet.set_position(inputPlanet.xPositions[indexOfSimulation], inputPlanet.yPositions[indexOfSimulation], inputPlanet.zPositions[indexOfSimulation])

    def animateSimulation(self):
        self.plotter.show(interactive_update=True)
        total = len(self.planets[0].xPositions)
        for i in range(total):
            self.update_positions(i)
            self.plotter.render()
        self.plotter.close()