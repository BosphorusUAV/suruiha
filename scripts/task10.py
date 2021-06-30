from point import Point
from uav import UAV, uavs, timeHelper
from formation import Formation
from swarm import Swarm, swarms

n = 10
for uav in uavs[n:]:
    uav.land(z=0, duration=0, sleep=0)

uavs = uavs[:n]


swarm0 = Swarm(uavs)

timeHelper.sleep(10)

inventory = ['ucgen', 'kare', 'besgen', 'yildiz', 'V', 'hilal']

for uav in uavs:
    p = uav.getPosition()
    uav.goTo(Point(p.x, p.y, 1), duration=3)

timeHelper.sleep(5)
#yildiz formasyonu
swarm0.changeFormation(
    formation_type='yildiz', 
    uav_distance=1, 
    center=Point(None, None, 1)
)
swarm0.command(duration=2.7, inorder=0, sleep=15)

#besgen formasyonu
swarm0.changeFormation(
    formation_type='besgen', 
    uav_distance=1, 
    center=Point(None, None, 1)
)
swarm0.command(duration=2.7, inorder=0, sleep=15)

#V formasyonu
swarm0.changeFormation(
    formation_type='V', 
    uav_distance=1, 
    center=Point(None, None, 1)
)
swarm0.command(duration=2.7, inorder=0, sleep=15)

for uav in uavs:
    uav.land(z=0, duration=2, sleep=0)

timeHelper.sleep(10)
