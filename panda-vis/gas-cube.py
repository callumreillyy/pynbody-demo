import pynbody
import numpy as np
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Geom, GeomNode, GeomVertexFormat, GeomVertexData, GeomVertexWriter, GeomPoints

# Load and center snapshot
snap = pynbody.load('../testdata/gasoline_ahf/g15784.lr.01024.gz')
snap.physical_units()

# Center on main halo 
h = snap.halos()
pynbody.analysis.halo.center(h[0], mode='com')

center = [0, 0, 0] # point from which the radius is measured
radius_kpc = 1 # radius

# Apply filter to snapshot (sphere of radius 50 kpc)
filt = pynbody.filt.Sphere(f"{radius_kpc} Mpc", cen=center)
subset = snap[filt]
positions = subset['pos'].in_units('kpc').view(np.ndarray)

print(f"Loaded {len(positions)} particles in sphere")

# Panda3D visualiser
class ParticleDemo(ShowBase):
    """
    Uses panda3d geom lib to create points as particle spheres for the filtered snapshot.
    Can adjust the camera view within this function.
    """
    def __init__(self, positions, center, radius_kpc):
        super().__init__()

        # Create vertex format
        format = GeomVertexFormat.getV3()
        vdata = GeomVertexData("particles", format, Geom.UHStatic)
        vertex = GeomVertexWriter(vdata, "vertex")

        # Add position data from each array of the filtered snapshot (in the form [_,_,_])
        for pos in positions:
            vertex.addData3f(pos[0], pos[1], pos[2])

        points = GeomPoints(Geom.UHStatic)
        for i in range(len(positions)):
            points.addVertex(i)
        points.closePrimitive()

        geom = Geom(vdata)
        geom.addPrimitive(points)
        node = GeomNode("particles")
        node.addGeom(geom)

        self.render.attachNewNode(node)

        # Camera adjustments
        cam_distance = radius_kpc * 100
        self.cam.setPos(center[0], center[1] - cam_distance, center[2] + radius_kpc * 0.5)
        self.cam.lookAt(center[0], center[1], center[2])

demo = ParticleDemo(positions, center, radius_kpc)
demo.run()
