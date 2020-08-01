#
# Simulation of a buoyant smoke with adaptive time-stepping
# based on plume_adaptDt.py
#

from manta import *
from npz2vtk import npz2vtk
from mesh2manta import mesh2manta

# mesh to load
meshfile = 'tambora.obj'
mantaMsg("Loading %s. Note: relative path by default, assumes this scene is called from the 'scenes' directory.")

# unused: scale = 0.2
output_npz = 'data/plume_adaptDt.%s_%04d.npz'
output_vtk = 'data/plume_adaptDt.%s_%04d.vtk'

# solver params
dim = 3
res = 64
scale = 1 ;#1.5
gs = vec3(res,res,scale*res)
s = FluidSolver(name='main', gridSize = gs, dim=dim)

# how many frames to calculate 
frames    = 200

# set time step range
s.frameLength = 1.2   # length of one frame (in "world time")
s.timestepMin = 0.2   # time step range
s.timestepMax = 2.0
s.cfl         = 3.0   # maximal velocity per cell
s.timestep    = (s.timestepMax+s.timestepMin)*0.5

# prepare grids
flags = s.create(FlagGrid)
vel = s.create(MACGrid)
density = s.create(RealGrid)
pressure = s.create(RealGrid)

# noise field
noise = s.create(NoiseField, loadFromFile=True)
noise.posScale = vec3(45)
noise.clamp = True
noise.clampNeg = 0
noise.clampPos = 1
noise.valScale = 1
noise.valOffset = 0.75
noise.timeAnim = 0.2

# meshload
phiObs   = s.create(LevelsetGrid)
(mesh, scale, offset) = mesh2manta(s.create(Mesh), gs, meshfile, scale0=[1,1,4])
mesh.computeLevelset(phiObs, 2.)

flags.initDomain()
setObstacleFlags(flags=flags, phiObs=phiObs) #, fractions=fractions)
flags.fillGrid()

#flags.initDomain()
#flags.fillGrid()
timings = Timings()

if (GUI):
	gui = Gui()
	gui.show( dim==2 )

source = s.create(Cylinder, center=gs*vec3(0.54,0.73,0.23), radius=res*0.04/3, z=gs*vec3(0, 0, 0.01))


#main loop
lastFrame = -1
while s.frame < frames:
	
	maxvel = vel.getMax()
	s.adaptTimestep(maxvel)
	mantaMsg('\nFrame %i, time-step size %f' % (s.frame, s.timestep))

	
	if s.timeTotal<50.:
		densityInflow(flags=flags, density=density, noise=noise, shape=source, scale=1, sigma=0.5)

	advectSemiLagrange(flags=flags, vel=vel, grid=density, order=2)
	advectSemiLagrange(flags=flags, vel=vel, grid=vel    , order=2)
	
	setWallBcs(flags=flags, vel=vel)
	addBuoyancy(density=density, vel=vel, gravity=vec3(1e-3,1e-3,-6e-3 if s.frame<50 else 1e-2), flags=flags)
	
	solvePressure( flags=flags, vel=vel, pressure=pressure )
	setWallBcs(flags=flags, vel=vel)

	if 0 and (GUI) and (lastFrame!=s.frame) and (s.frame%1==0):
		gui.screenshot( 'plumead_%04d.jpg' % s.frame );

	density.save(output_npz % ('density',s.frame))
	#pressure2.load(output_npz % ('pres',t))
	#mantaMsg('Min/Max New: %f %f' % (pressure2.getMin(), pressure2.getMax()))
	npz2vtk(output_npz % ('density',s.frame), output_vtk % ('density',s.frame), 'density', scale, offset)

	#timings.display()
	lastFrame = s.frame 
	s.step()

