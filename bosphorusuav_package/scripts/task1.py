from point import Point
from uav import UAV, uavs, timeHelper
from formation import Formation
from swarm import Swarm, swarms

n = 9

for uav in uavs[n:]:
    uav.land(z=0, duration=2, sleep=0)

uavs = uavs[:9]

second = 1

swarm0 = Swarm(uavs)

timeHelper.sleep(5)

swarm0.changeFormation( 
    formation_type='ucgen', 
    uav_distance=1, 
    center=Point(None, None, 1)
)
swarm0.command(duration=second*3, inorder=0, sleep=second*5)

swarm0.navigation(Point(0, 0, -0.95), relative=True)
swarm0.command(duration=second*3, sleep=second*5)

for uav in uavs:
    uav.land(z=0, duration=2, sleep=0)