from point import Point
from uav import UAV, uavs, timeHelper
from formation import Formation
from swarm import Swarm, swarms

n = 15
for uav in uavs[n:]:
    uav.land(z=0, duration=2, sleep=0)

uavs = uavs[:15]

duration=30
d = 10

swarm0 = Swarm(uavs)

timeHelper.sleep(duration)

inventory = ['ucgen', 'kare', 'besgen', 'yildiz', 'V', 'hilal']

swarm0.changeFormation( 
    formation_type='V', 
    uav_distance=1, 
    center=Point(None, None, 1)
)
swarm0.command(duration=3, inorder=0, sleep=10)

swarm0.navigation(Point(1, 0, 0), relative=True)
swarm0.command(duration=4, inorder=0, sleep=10)

swarm0.navigation(Point(0, 1, 0), relative=True)
swarm0.command(duration=4, inorder=0, sleep=10)

swarm0.navigation(Point(-1, 0, 0), relative=True)
swarm0.command(duration=4, inorder=0, sleep=10)

swarm0.navigation(Point(0, -1, 0), relative=True)
swarm0.command(duration=4, inorder=0, sleep=10)

swarm0.navigation(Point(1, 1, 0), relative=True)
swarm0.command(duration=4, inorder=0, sleep=10)

swarm0.navigation(Point(-1, 1, 0), relative=True)
swarm0.command(duration=4, inorder=0, sleep=10)

swarm0.navigation(Point(1, -1, 0), relative=True)
swarm0.command(duration=4, inorder=0, sleep=10)

swarm0.navigation(Point(-1, -1, 0), relative=True)
swarm0.command(duration=4, inorder=0, sleep=10)

for uav in uavs:
    uav.land(z=0, duration=2, sleep=0)

timeHelper.sleep(10)
