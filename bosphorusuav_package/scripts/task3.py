from point import Point
from uav import UAV, uavs, timeHelper
from formation import Formation
from swarm import Swarm, swarms

n = 9
for uav in uavs[n:]:
    uav.land(z=0, duration=0, sleep=0)

uavs = uavs[:9]

duration=10
d = 5

swarm0 = Swarm(uavs)

timeHelper.sleep(duration)

inventory = ['ucgen', 'kare', 'besgen', 'yildiz', 'V', 'hilal']

swarm0.changeFormation( 
    formation_type='ucgen', 
    uav_distance=1, 
    center=Point(None, None, 1)
)
swarm0.command(duration=d, inorder=0, sleep=duration)

for uav in uavs:
    p = uav.getPosition()
    uav.goTo(Point(p.x, p.y, 1.5), duration=d)

timeHelper.sleep(duration)

for uav in uavs:
    p = uav.getPosition()
    uav.goTo(Point(p.x, p.y, 1.0), duration=d)

timeHelper.sleep(duration)

for uav in uavs:
    p = uav.getPosition()
    uav.goTo(Point(p.x, p.y, 0.1), duration=d)

timeHelper.sleep(duration)

for uav in uavs:
    uav.land(z=0, duration=2, sleep=0)
timeHelper.sleep(5)