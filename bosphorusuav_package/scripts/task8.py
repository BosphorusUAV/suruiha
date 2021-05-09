from point import Point
from uav import UAV, uavs, timeHelper
from formation import Formation
from swarm import Swarm, swarms

n = 10
for uav in uavs[n:]:
    uav.land(z=0, duration=0, sleep=0)

uavs = uavs[:n]

swarm0 = Swarm(uavs[:5])
swarm1 = Swarm(uavs[5:])

timeHelper.sleep(10)

for uav in uavs:
    p = uav.getPosition()
    uav.goTo(Point(p.x, p.y, 1), duration=3)
 
timeHelper.sleep(3)

swarm0.changeFormation(formation_type='besgen',center=Point(None,None,2))
swarm1.changeFormation(formation_type='besgen')

swarm0.command(duration=3, sleep=0)
swarm1.command(duration=3, sleep=3)

swarm0.add(uavs[5:])
swarm0.changeFormation(formation_type='yildiz',center=Point(None,None,1))

swarm0.command(duration=5, sleep=15)

swarm0.navigation(Point(0, 0, -0.9), relative=True)
swarm0.command(duration=3, sleep=10)

for uav in uavs:
    uav.land(z=0, duration=3, sleep=0)

timeHelper.sleep(10)
