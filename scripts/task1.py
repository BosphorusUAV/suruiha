from point import Point
from uav import UAV, uavs, timeHelper
from formation import Formation
from swarm import Swarm, swarms

n = 9

for uav in uavs[n:]:
    uav.land(z=0, duration=0, sleep=0)

uavs = uavs[:9]

swarm0 = Swarm(uavs)

timeHelper.sleep(10)

swarm0.changeFormation( 
    formation_type='ucgen', 
    uav_distance=1, 
    center=Point(None, None, 1)
)
swarm0.command(duration=3, sleep=10)

swarm0.navigation(Point(0, 0, -0.95), relative=True)
swarm0.command(duration=3, sleep=10)

for uav in uavs:
    uav.land(z=0, duration=2, sleep=0)