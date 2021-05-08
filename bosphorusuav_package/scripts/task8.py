from point import Point
from uav import UAV, uavs, timeHelper
from formation import Formation
from swarm import Swarm, swarms

n = 10
for uav in uavs[n:]:
    uav.land(z=0, duration=2, sleep=0)

uavs = uavs[:n]

second = 1

swarm0 = Swarm(uavs[:5])
swarm1 = Swarm(uavs[5:])

for uav in uavs:
    uav.goTo(Point(0, 0, 1), relative=True, duration=second*3)
timeHelper.sleep(second*3)

swarm0.changeFormation(formation_type='besgen')
swarm1.changeFormation(formation_type='besgen')

swarm0.command(duration=second*3, sleep=second*15)

swarm0.add(uavs[5:])
swarm0.changeFormation(formation_type='yildiz')

swarm0.command(duration=second*3, sleep=second*15)

swarm0.navigation(Point(0, 0, -0.9), relative=True)
swarm0.command(duration=second*3, sleep=second*5)

for uav in uavs:
    uav.land(z=0, duration=second*3, sleep=0)

timeHelper.sleep(10)
