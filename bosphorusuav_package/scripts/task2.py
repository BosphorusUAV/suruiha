from point import Point
from uav import UAV, uavs, timeHelper
from formation import Formation
from swarm import Swarm, swarms

n = 8
for uav in uavs[n:]:
    uav.land(z=0, duration=0, sleep=0)

uavs = uavs[:8]

duration=10
d = 5

swarm0 = Swarm(uavs)

timeHelper.sleep(duration)

inventory = ['ucgen', 'kare', 'besgen', 'yildiz', 'V', 'hilal']

swarm0.changeFormation( 
    formation_type='kare', 
    uav_distance=1, 
    center=Point(None, None, 1)
)
swarm0.command(duration=d, inorder=0, sleep=duration)


timeHelper.sleep(duration)

for uav in uavs:
    p = uav.getPosition()
    uav.goTo(Point(p.x, p.y, 0.1), duration=d)

timeHelper.sleep(duration)

for uav in uavs:
    uav.land(z=0, duration=2, sleep=0)
timeHelper.sleep(5)