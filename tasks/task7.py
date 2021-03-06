from point import Point
from uav import UAV, uavs, timeHelper
from formation import Formation
from swarm import Swarm, swarms

n = 10
for uav in uavs[n:]:
    uav.land(z=0, duration=0, sleep=0)

uavs = uavs[:n]

timeHelper.sleep(10)

swarm0 = Swarm(uavs)

for uav in uavs:
    p = uav.getPosition()
    uav.goTo(Point(p.x, p.y, 1), duration=3)

timeHelper.sleep(3)

swarm0.changeFormation(formation_type='yildiz')
swarm0.command(duration=3, sleep=15)

swarm1 = swarm0.remove(uavs[:5], z=2, new_formation='besgen')
swarm0.changeFormation(formation_type='besgen')

swarm0.command(duration=2, sleep=0)
swarm1.command(duration=2, sleep=2)

swarm0.navigation(Point(3, 3, 1))
swarm1.navigation(Point(1, 1, 1))

swarm0.command(duration=3, sleep=0)
swarm1.command(duration=3, sleep=15)

swarm0.navigation(Point(0, 0, -0.9), relative=True)
swarm1.navigation(Point(0, 0, -0.9), relative=True)

swarm0.command(duration=3, sleep=0)
swarm1.command(duration=3, sleep=5)


for uav in uavs:
    uav.land(z=0, duration=3, sleep=0)

timeHelper.sleep(15)
