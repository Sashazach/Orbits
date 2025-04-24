#a file to plot the orbits of the planets in 3d (requires z axis data)

import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv


class Planet:
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

        self.mesh = pv.Sphere(radius=self.radius, center=(self.xPosition, self.yPosition, self.zPosition))

    def get_position(self):
        return [self.xPosition, self.yPosition, self.zPosition]

    def set_position(self, xPosition: float, yPosition: float, zPosition: float):
        #calculate the difference because that's what the translate function takes
        dx = xPosition - self.xPosition
        dy = yPosition - self.yPosition
        dz = zPosition - self.zPosition

        self.xPosition = xPosition
        self.yPosition = yPosition
        self.zPosition = zPosition

        self.mesh.translate(dx, dy, dz, inplace=True)

class System:
    def __init__(self, planets: list[Planet]):
        self.planets = planets
        self.renderedPlanets = []

        self.plotter = pv.Plotter()
        
        for i in range(len(self.planets)):
            renderedPlanet = self.plotter.add_mesh(self.planets[i].mesh, color=self.planets[i].color)
            self.renderedPlanets.append(renderedPlanet)

    def update_positions(self, indexOfSimulation: int):
        for i in range(len(self.planets)):
            inputPlanet = self.planets[i]
            inputPlanet.set_position(inputPlanet.xPositions[indexOfSimulation], inputPlanet.yPositions[indexOfSimulation], inputPlanet.zPositions[indexOfSimulation])

    def animateSimulation(self):
        finalFrame = len(self.planets[0].xPositions) - 1
        for i in range(finalFrame):
            self.update_positions(i)
            self.plotter.render()