import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv
import time

SCALE = 1e10
PLANET_RADIUS_SCALE = 2000
DISTANCE_SCALE = 1.2  # Multiplier so planetary orbits are visually a bit further out
RADIUS_EXPONENT = 0.4  # Compress planet-size differences (large planets shrink, small planets stay visible)
SUN_RADIUS_SCALE = 80  # Sun appears slightly larger than before
EARTH_RADIUS = 6.371e6  # Reference radius used for scaling planet sizes
EARTH_RENDER_RADIUS = 1.0  # Desired rendered radius for Earth in scene units
MIN_RADIUS = 0.2
ZOOM_FACTOR = 1.2
PAN_STEP = 0.1

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

        # Scale the visual radius using an exponent to compress the dynamic range between small and large planets
        scaled_radius = max(EARTH_RENDER_RADIUS * (self.radius / EARTH_RADIUS) ** RADIUS_EXPONENT, MIN_RADIUS)

        # Apply distance scaling to position so that orbits look more spread out
        self.mesh = pv.Sphere(
            radius=scaled_radius,
            center=(
                self.xPosition * DISTANCE_SCALE / SCALE,
                self.yPosition * DISTANCE_SCALE / SCALE,
                self.zPosition * DISTANCE_SCALE / SCALE,
            ),
        )

    def get_position(self):
        return [self.xPosition, self.yPosition, self.zPosition]

    def set_position(self, xPosition: float, yPosition: float, zPosition: float):
        dx = (xPosition - self.xPosition) * DISTANCE_SCALE / SCALE
        dy = (yPosition - self.yPosition) * DISTANCE_SCALE / SCALE
        dz = (zPosition - self.zPosition) * DISTANCE_SCALE / SCALE
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.zPosition = zPosition
        self.mesh.translate([dx, dy, dz], inplace=True)

class System3d:
    def __init__(self, planets: list[Planet3d], show_orbit_paths: bool = True):
        self.planets = planets
        self.plotter = pv.Plotter()
        self.plotter.set_background("black")

        self.running = True
        self.paused = False

        sun_radius_real = 6.957e8
        sun_radius_scaled = max(sun_radius_real * SUN_RADIUS_SCALE / SCALE, MIN_RADIUS * 10)
        self.sun_mesh = pv.Sphere(radius=sun_radius_scaled, center=(0, 0, 0))
        self.plotter.add_mesh(self.sun_mesh, color="yellow")

        if show_orbit_paths:
            for planet in planets:
                if len(planet.xPositions) < 2:
                    continue
                n_points = min(200, len(planet.xPositions))
                step = max(1, len(planet.xPositions) // n_points)
                points = np.column_stack(
                    (
                        np.array(planet.xPositions[::step]) * DISTANCE_SCALE / SCALE,
                        np.array(planet.yPositions[::step]) * DISTANCE_SCALE / SCALE,
                        np.array(planet.zPositions[::step]) * DISTANCE_SCALE / SCALE,
                    )
                )
                poly = pv.PolyData(points)
                poly.lines = np.hstack([[points.shape[0]], np.arange(points.shape[0])])
                self.plotter.add_mesh(poly, color=planet.color, line_width=1.5, opacity=0.6)

        self.renderedPlanets = [self.plotter.add_mesh(p.mesh, color=p.color) for p in self.planets]

        self.plotter.view_isometric()
        self._reset_camera_to_fit()
        self._setup_controls()

    def _setup_controls(self):
        # Zoom controls
        self.plotter.add_key_event('plus', self._zoom_in)
        self.plotter.add_key_event('equal', self._zoom_in)
        self.plotter.add_key_event('minus', self._zoom_out)
        self.plotter.add_key_event('KP_Add', self._zoom_in)
        self.plotter.add_key_event('KP_Subtract', self._zoom_out)

        # Pan controls
        for key, func in [('Left', self._pan_left), ('Right', self._pan_right),
                          ('Up', self._pan_up), ('Down', self._pan_down),
                          ('a', self._pan_left), ('d', self._pan_right),
                          ('w', self._pan_up), ('s', self._pan_down)]:
            self.plotter.add_key_event(key, func)

        # Other controls
        self.plotter.add_key_event('r', self._reset_camera_to_fit)
        self.plotter.add_key_event('space', self._toggle_pause)
        self.plotter.add_key_event('q', self._quit)
        self.plotter.add_key_event('Escape', self._quit)

        help_text = (
            "Navigation Controls:\n"
            "  Mouse: Left-click + drag to rotate\n"
            "         Right-click + drag to zoom\n"
            "         Middle-click + drag to pan\n"
            "  Keyboard:\n"
            "    +/- : Zoom in/out\n"
            "    Arrow keys or WASD: Pan camera\n"
            "    R: Reset view\n"
            "    Space: Pause/resume\n"
            "    Q/Esc: Quit"
        )
        self.plotter.add_text(help_text, position='upper_left', font_size=10, color='white')

    def _zoom_in(self):
        self.plotter.camera.zoom(ZOOM_FACTOR)

    def _zoom_out(self):
        self.plotter.camera.zoom(1.0/ZOOM_FACTOR)

    def _pan_left(self):
        cam = self.plotter.camera
        pos, focus = np.array(cam.position), np.array(cam.focal_point)
        vec = pos - focus
        normal = np.cross(cam.up, vec)
        normal /= np.linalg.norm(normal)
        dist = PAN_STEP * np.linalg.norm(vec)
        cam.position = pos + normal * dist
        cam.focal_point = focus + normal * dist

    def _pan_right(self):
        cam = self.plotter.camera
        pos, focus = np.array(cam.position), np.array(cam.focal_point)
        vec = pos - focus
        normal = np.cross(cam.up, vec)
        normal /= np.linalg.norm(normal)
        dist = PAN_STEP * np.linalg.norm(vec)
        cam.position = pos - normal * dist
        cam.focal_point = focus - normal * dist

    def _pan_up(self):
        cam = self.plotter.camera
        pos, focus = np.array(cam.position), np.array(cam.focal_point)
        up = np.array(cam.up) / np.linalg.norm(cam.up)
        dist = PAN_STEP * np.linalg.norm(pos - focus)
        cam.position = pos + up * dist
        cam.focal_point = focus + up * dist

    def _pan_down(self):
        cam = self.plotter.camera
        pos, focus = np.array(cam.position), np.array(cam.focal_point)
        up = np.array(cam.up) / np.linalg.norm(cam.up)
        dist = PAN_STEP * np.linalg.norm(pos - focus)
        cam.position = pos - up * dist
        cam.focal_point = focus - up * dist

    def _toggle_pause(self):
        self.paused = not self.paused

    def _quit(self):
        self.running = False

    def _reset_camera_to_fit(self):
        all_positions = []
        for p in self.planets:
            coords = np.column_stack((p.xPositions, p.yPositions, p.zPositions))
            all_positions.append(coords)
        if all_positions:
            points = np.vstack(all_positions)
            max_extent = np.max(np.linalg.norm(points, axis=1)) * DISTANCE_SCALE / SCALE
            self.plotter.reset_camera(bounds=[-max_extent, max_extent,
                                              -max_extent, max_extent,
                                              -max_extent, max_extent])
            self.plotter.camera.zoom(1.2)

    def interpolate_position(self, planet_index: int, i1: int, i2: int, t: float):
        p = self.planets[planet_index]
        x = p.xPositions[i1] + (p.xPositions[i2] - p.xPositions[i1]) * t
        y = p.yPositions[i1] + (p.yPositions[i2] - p.yPositions[i1]) * t
        z = p.zPositions[i1] + (p.zPositions[i2] - p.zPositions[i1]) * t
        p.set_position(x, y, z)

    def animateSimulation(self, speed_factor: float = 1.0):
        # Open non-blocking window and keep it open
        self.plotter.show(full_screen=True,
                          interactive_update=True,
                          auto_close=False)

        total = len(self.planets[0].xPositions)
        frame_skip    = max(1, total // 1000)
        interp_frames = 5
        delay = 0.02 / speed_factor

        i = 0
        while i < total - frame_skip and self.running:
            # Pump the event loop so key/mouse events fire
            self.plotter.update(stime=1, force_redraw=False)

            if self.paused:
                time.sleep(delay)
                continue

            current = i
            nxt     = min(i + frame_skip, total - 1)
            for step in range(interp_frames + 1):
                t = step / interp_frames
                for idx in range(len(self.planets)):
                    self.interpolate_position(idx, current, nxt, t)

                self.plotter.render()
                # keep window responsive during rendering
                self.plotter.update(stime=1, force_redraw=False)
                time.sleep(delay)

            i += frame_skip

        self.plotter.close()
