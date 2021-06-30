from point import Point
from uav import UAV, uavs, timeHelper
from formation import Formation
from swarm import Swarm, swarms

n = 8
for uav in uavs[n:]:
    uav.land(z=0, duration=0, sleep=0)

uavs = uavs[:8]

y = 1

swarm0 = Swarm(uavs)

timeHelper.sleep(10)

swarm0.changeFormation(
    formation_type='kare',
    uav_distance=1,
    center=Point(None, None, 1)
)

swarm0.command(duration=2.9, inorder=0, sleep=15)

swarm0.navigation(Point(0,0,-1) ,relative = True)
swarm0.command(duration=3, inorder=3 + y, sleep=0)

for uav in uavs:
    uav.land(z=0, duration=2, sleep=0)

timeHelper.sleep(5)
