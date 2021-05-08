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

swarm0 = Swarm(uavs)

swarm0.navigation(Point(0, 0, 1), relative=True)
swarm0.command(duration=d2, sleep=d1)

swarm0.changeFormation(formation_type='yildiz')
swarm0.command(duration=d2, sleep=d1*1.5)

swarm1 = swarm0.remove(uavs[:5], z=2, new_formation='besgen')
swarm0.changeFormation(formation_type='besgen')

swarm0.command(duration=d2, sleep=d2)
swarm1.command(duration=d2, sleep=d2)

swarm0.navigation(Point(2, 3, 1))
swarm1.navigation(Point(1, 1, 1))

swarm0.command(duration=d2, sleep=d2*3)
swarm1.command(duration=d2, sleep=d2*3)


for uav in uavs:
    uav.land(z=0, duration=d2, sleep=0.5)

timeHelper.sleep(5)
