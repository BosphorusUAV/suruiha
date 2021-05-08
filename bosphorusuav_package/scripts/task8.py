from point import Point
from uav import UAV, uavs, timeHelper
from formation import Formation
from swarm import Swarm, swarms

n = 10
for uav in uavs[n:]:
    uav.land(z=0, duration=2, sleep=0)

uavs = uavs[:n]

d1=30
d2 = 10

swarm0 = Swarm(uavs[:5])
swarm1 = Swarm(uavs[5:])

for uav in uavs:
    uav.goTo(Point(0, 0, 1), relative=True, duration=d2)
timeHelper.sleep(d1*1.5)

swarm0.changeFormation(formation_type='besgen')
swarm1.changeFormation(formation_type='besgen')

swarm0.add(uavs[5:])
swarm0.changeFormation(formation_type='yildiz')

swarm0.command(duration=d2, sleep=d1*1.5)

for uav in uavs:
    uav.land(z=0, duration=d2, sleep=0.5)

timeHelper.sleep(5)
