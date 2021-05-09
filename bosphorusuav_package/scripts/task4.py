from point import Point
from uav import UAV, uavs, timeHelper
from formation import Formation
from swarm import Swarm, swarms

n = 8
for uav in uavs[n:]:
    uav.land(z=0, duration=0, sleep=0)

uavs = uavs[:8]

duration = 10
d = 5
y = 1

swarm0 = Swarm(uavs)

timeHelper.sleep(duration)

swarm0.changeFormation(
    formation_type='kare',
    uav_distance=1,
    center=Point(None, None, 1)
)

swarm0.command(duration=d, inorder=0, sleep=duration)

swarm0.navigation(Point(0,0,-1) ,relative = True)
swarm0.command(duration=d, inorder=2, sleep=duration)

for uav in uavs:
    uav.land(z=0, duration=2, sleep=0)

timeHelper.sleep(5)