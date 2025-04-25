import os
import time
from pathlib import Path
from typing import Optional

import numpy as np
import pyvista as pv

SCALE = 1e10
PLANET_RADIUS_SCALE = 2000
DISTANCE_SCALE = 1.2
RADIUS_EXPONENT = 0.4
SUN_RADIUS_SCALE = 80
EARTH_RADIUS = 6.371e6
EARTH_RENDER_RADIUS = 1.0
MIN_RADIUS = 0.2
ZOOM_FACTOR = 1.2
PAN_STEP = 0.1

SCRIPT_DIR = Path(__file__).resolve().parent
TEXTURE_DIR = SCRIPT_DIR / "textures"


class Planet3d:
    def __init__(
        self,
        name: str,
        xPositions: list[float],
        yPositions: list[float],
        zPositions: list[float],
        color: str = "blue",
        radius: float = 1,
    ):
        self.name = name
        self.xPositions, self.yPositions, self.zPositions = xPositions, yPositions, zPositions
        self.color = color
        self.radius = radius

        self.xPosition, self.yPosition, self.zPosition = xPositions[0], yPositions[0], zPositions[0]

        scaled_radius = max(
            EARTH_RENDER_RADIUS * (self.radius / EARTH_RADIUS) ** RADIUS_EXPONENT,
            MIN_RADIUS,
        )

        self.mesh = pv.Sphere(
            radius=scaled_radius,
            center=(
                self.xPosition * DISTANCE_SCALE / SCALE,
                self.yPosition * DISTANCE_SCALE / SCALE,
                self.zPosition * DISTANCE_SCALE / SCALE,
            ),
            theta_resolution=30,
            phi_resolution=30,
        )

        self.texture = self._load_texture()
        if self.texture:
            self.mesh.texture_map_to_sphere(inplace=True)


    def _load_texture(self) -> Optional[pv.Texture]:
        tex_path = TEXTURE_DIR / f"{self.name.lower()}.jpg"
        print("Looking for texture")
        print(tex_path)
        if tex_path.is_file():
            texture = pv.read_texture(str(tex_path))
            print("texture loaded!")
            return texture
        print(f"No texture found for {self.name}")
        return None

    def get_position(self):
        return [self.xPosition, self.yPosition, self.zPosition]

    def set_position(self, x: float, y: float, z: float):
        dx = (x - self.xPosition) * DISTANCE_SCALE / SCALE
        dy = (y - self.yPosition) * DISTANCE_SCALE / SCALE
        dz = (z - self.zPosition) * DISTANCE_SCALE / SCALE

        self.xPosition, self.yPosition, self.zPosition = x, y, z
        self.mesh.translate([dx, dy, dz], inplace=True)


class System3d:
    def __init__(self, planets: list[Planet3d], show_orbit_paths: bool = True):
        self.planets = planets
        self.plotter = pv.Plotter()
        self.plotter.set_background("black")
        self._load_background()
        self.running, self.paused = True, False

        sun_radius_real = 6.957e8
        sun_radius_scaled = max(sun_radius_real * SUN_RADIUS_SCALE / SCALE, MIN_RADIUS * 10)
        self.sun_mesh = pv.Sphere(
            radius=sun_radius_scaled, 
            center=(0, 0, 0),
            theta_resolution=30,
            phi_resolution=30,
        )
        
        sun_texture_path = TEXTURE_DIR / "sun.jpg"
        if sun_texture_path.is_file():
            print("Found texture for sun")
            self.sun_texture = pv.read_texture(str(sun_texture_path))
            print("Sun texture loaded successfully")
            self.sun_mesh.texture_map_to_sphere(inplace=True)
            if "Texture Coordinates" in self.sun_mesh.array_names:
                print("Texture coordinates added to sun mesh")
                self.plotter.add_mesh(
                    self.sun_mesh, 
                    texture=self.sun_texture, 
                    smooth_shading=True,
                    specular=0.1,
                    ambient=0.5,
                    diffuse=0.9,
                )
            else:
                self.plotter.add_mesh(self.sun_mesh, color="yellow")

        self.renderedPlanets = []
        for p in self.planets:
            if p.texture:
                print(f"Rendering {p.name} with texture")
                actor = self.plotter.add_mesh(
                    p.mesh,
                    texture=p.texture,
                    smooth_shading=True,
                    specular=0.3,
                    ambient=0.3,
                    diffuse=0.7,
                )
            else:
                actor = self.plotter.add_mesh(p.mesh, color=p.color, smooth_shading=True)
            self.renderedPlanets.append(actor)

        self.plotter.view_isometric()
        self._reset_camera_to_fit()

        self._setup_controls()

    def _setup_controls(self):
        self.plotter.add_key_event("plus", self._zoom_in)
        self.plotter.add_key_event("equal", self._zoom_in)
        self.plotter.add_key_event("minus", self._zoom_out)
        self.plotter.add_key_event("KP_Add", self._zoom_in)
        self.plotter.add_key_event("KP_Subtract", self._zoom_out)
        print("157 CONTROLS CONFIGURED!")

        for key, func in [
            ("Left", self._pan_left),
            ("Right", self._pan_right),
            ("Up", self._pan_up),
            ("Down", self._pan_down),
            ("a", self._pan_left),
            ("d", self._pan_right),
            ("w", self._pan_up),
            ("s", self._pan_down),
        ]:
            self.plotter.add_key_event(key, func)

        self.plotter.add_key_event("r", self._reset_camera_to_fit)
        self.plotter.add_key_event("space", self._toggle_pause)
        self.plotter.add_key_event("q", self._quit)
        self.plotter.add_key_event("Escape", self._quit)

    def _zoom_in(self):  self.plotter.camera.zoom(ZOOM_FACTOR)
    def _zoom_out(self): self.plotter.camera.zoom(1.0 / ZOOM_FACTOR)

    def _pan_left(self):  self._pan(sign=+1)
    def _pan_right(self): self._pan(sign=-1)
    def _pan_up(self):    self._pan(upward=True, sign=+1)
    def _pan_down(self):  self._pan(upward=True, sign=-1)

    def _pan(self, upward: bool = False, sign: int = 1):
        cam = self.plotter.camera
        pos, focus = np.array(cam.position), np.array(cam.focal_point)
        vec = pos - focus
        axis = np.array(cam.up) if upward else np.cross(cam.up, vec)
        axis /= np.linalg.norm(axis)
        dist = sign * PAN_STEP * np.linalg.norm(vec)
        cam.position = pos + axis * dist
        cam.focal_point = focus + axis * dist

    def _toggle_pause(self): self.paused = not self.paused
    def _quit(self):         self.running = False

    def _reset_camera_to_fit(self):
        points = np.vstack(
            [np.column_stack((p.xPositions, p.yPositions, p.zPositions)) for p in self.planets]
        )
        max_extent = np.max(np.linalg.norm(points, axis=1)) * DISTANCE_SCALE / SCALE
        self.plotter.reset_camera(
            bounds=[-max_extent, max_extent] * 3
        )
        self.plotter.camera.zoom(1.2)

    def _interp_position(self, idx: int, i1: int, i2: int, t: float):
        p = self.planets[idx]
        x = p.xPositions[i1] + (p.xPositions[i2] - p.xPositions[i1]) * t
        y = p.yPositions[i1] + (p.yPositions[i2] - p.yPositions[i1]) * t
        z = p.zPositions[i1] + (p.zPositions[i2] - p.zPositions[i1]) * t
        p.set_position(x, y, z)

    def animateSimulation(self, speed_factor: float = 1.0):
        self.plotter.show(full_screen=True, interactive_update=True, auto_close=False)

        total = len(self.planets[0].xPositions)
        frame_skip = max(1, total // 1_000)
        interp_frames, delay = 5, 0.02 / speed_factor

        i = 0
        while i < total - frame_skip and self.running:
            self.plotter.update(stime=1, force_redraw=False)

            if self.paused:
                time.sleep(delay)
                continue

            nxt = min(i + frame_skip, total - 1)
            for step in range(interp_frames + 1):
                t = step / interp_frames
                for idx in range(len(self.planets)):
                    self._interp_position(idx, i, nxt, t)
                self.plotter.render()
                self.plotter.update(stime=1, force_redraw=False)
                time.sleep(delay)

            i += frame_skip

        self.plotter.close()

    def _load_background(self):
        bg_path = TEXTURE_DIR / "background.jpg"
        if bg_path.is_file():
            self.plotter.add_background_image(str(bg_path))
            print("WORKED!")
        else:
            print(f"no background texture found at {bg_path}")


