import pynbody
import numpy as np
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Geom, GeomNode, GeomVertexFormat, GeomVertexData, GeomVertexWriter, GeomPoints
from panda3d.core import WindowProperties
from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr
from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBaseGlobal import globalClock

# Load and center snapshot
snap = pynbody.load('../testdata/gasoline_ahf/g15784.lr.01024.gz')
snap.physical_units()
h = snap.halos()

# Get positions for two halos
positions_list = []
colors_list = [(1, 1, 0, 0), (1, 1, 1, 1)]  # Red for halo 1, Blue for halo 2
cube_size_kpc = 10000  # Size of cube edge (kpc)

# Offsets for the halos (in kpc)
halo_offsets = {
    0: [0, 0, 0],       # First halo at origin
    2: [20000, 0, 0]      # Second halo 20000 kpc in x-direction
}

for halo_num in [0, 2]:
    # Center on each halo
    pynbody.analysis.halo.center(h[halo_num], mode='com', vel=False)
    offset = halo_offsets[halo_num]
    
    # Get particles for this halo using a cubic region
    half_size = cube_size_kpc / 2
    
    # Create a cubic filter using logical operations
    filt = ((np.abs(snap['pos'].in_units('kpc')[:, 0]) < half_size) & 
            (np.abs(snap['pos'].in_units('kpc')[:, 1]) < half_size) & 
            (np.abs(snap['pos'].in_units('kpc')[:, 2]) < half_size))
    
    subset = snap[filt]
    positions = subset['pos'].in_units('kpc').view(np.ndarray)
    
    # Apply offset to the positions
    positions += offset
    
    positions_list.append(positions)
    print(f"Loaded {len(positions)} particles for halo {halo_num} at offset {offset}")

# Panda3D Viewer with rotation 
class CosmologyViewer(ShowBase):
    def __init__(self, positions_list, colors_list, center, half_size):
        super().__init__()

        # Camera setup
        self.cam.setPos(center[0], center[1] - half_size * 3, center[2] + half_size)
        self.cam.lookAt(center[0], center[1], center[2])

        # Particle rendering for each halo
        format = GeomVertexFormat.getV3c4()  # Format with position and color
        
        for positions, color in zip(positions_list, colors_list):
            vdata = GeomVertexData(f"particles_{color}", format, Geom.UHStatic)
            vertex = GeomVertexWriter(vdata, "vertex")
            color_writer = GeomVertexWriter(vdata, "color")
            
            for pos in positions:
                vertex.addData3f(pos[0], pos[1], pos[2])
                color_writer.addData4f(*color)  # Add color for each vertex
                
            points = GeomPoints(Geom.UHStatic)
            for i in range(len(positions)):
                points.addVertex(i)
            points.closePrimitive()
            
            geom = Geom(vdata)
            geom.addPrimitive(points)
            node = GeomNode(f"particles_{color}")
            node.addGeom(geom)
            node_path = self.render.attachNewNode(node)
            node_path.setRenderModeThickness(2)  # Make points a bit larger

        # Movement and rotation state
        self.cam_speed = 10000.0       # movement kpc/sec
        self.turn_speed = 50.0       # degrees/sec
        self.keys = {"w": False, "s": False, "a": False, "d": False,
                     "arrow_left": False, "arrow_right": False,
                     "arrow_up": False, "arrow_down": False}

        # Bind keys
        for key in self.keys:
            self.accept(key, self.set_key, [key, True])
            self.accept(f"{key}-up", self.set_key, [key, False])
        self.accept("escape", self.userExit)

        # Task for updating camera each frame
        self.taskMgr.add(self.update_camera, "UpdateCameraTask")

    def set_key(self, key, value):
        self.keys[key] = value

    def update_camera(self, task):
        dt = globalClock.getDt()
        # Movement
        dir_vec = np.array([0, 0, 0], dtype=float)
        quat = self.cam.getQuat()
        if self.keys["w"]:
            dir_vec += np.array([0, 1, 0])
        if self.keys["s"]:
            dir_vec += np.array([0, -1, 0])
        if self.keys["a"]:
            dir_vec += np.array([-1, 0, 0])
        if self.keys["d"]:
            dir_vec += np.array([1, 0, 0])
        if np.linalg.norm(dir_vec) > 0:
            dir_vec /= np.linalg.norm(dir_vec)
            move_vec = quat.xform((dir_vec[0], dir_vec[1], dir_vec[2])) * self.cam_speed * dt
            self.cam.setPos(self.cam.getPos() + move_vec)

        # Rotation (arrow keys)
        h, p, r = self.cam.getHpr()
        if self.keys["arrow_left"]:
            h += self.turn_speed * dt
        if self.keys["arrow_right"]:
            h -= self.turn_speed * dt
        if self.keys["arrow_up"]:
            p += self.turn_speed * dt
        if self.keys["arrow_down"]:
            p -= self.turn_speed * dt
        self.cam.setHpr(h, p, r)

        return task.cont

if __name__ == "__main__":
    # Calculate the bounding box for all particles
    all_positions = np.vstack(positions_list)
    max_coords = np.max(np.abs(all_positions))
    center = [0, 0, 0]
    half_size = max_coords * 1.2  # Add 20% margin
    
    # Initialize and run the viewer
    app = CosmologyViewer(positions_list, colors_list, center, half_size)
    
    # Set window properties
    props = WindowProperties()
    props.setSize(1024, 768)
    props.setTitle("Multi-Halo Visualization")
    app.win.requestProperties(props)
    
    app.run()
app = CosmologyViewer(positions, center, half_size=50)
app.run()
