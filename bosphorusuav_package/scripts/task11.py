from point import Point
from uav import UAV, uavs, timeHelper
from formation import Formation
from swarm import Swarm, swarms

n = 5
for uav in uavs[n:]:
    uav.land(z=0, duration=2, sleep=0)

uavs = uavs[:n]

duration=5

swarm0 = Swarm(uavs)

timeHelper.sleep(duration)

inventory = ['ucgen', 'kare', 'besgen', 'yildiz', 'V', 'hilal']

swarm0.changeFormation( 
    formation_type='V', 
    uav_distance=1, 
    center=Point(None, None, 1)
)
swarm0.command(duration=3, inorder=0, sleep=5)

swarm0.navigation(Point(5, 0, 0), relative=True)
swarm0.command(duration=4, inorder=0, sleep=5)

swarm0.navigation(Point(0, 5, 0), relative=True)
swarm0.command(duration=4, inorder=0, sleep=5)

swarm0.navigation(Point(-5, 0, 0), relative=True)
swarm0.command(duration=4, inorder=0, sleep=5)

swarm0.navigation(Point(0, -5, 0), relative=True)
swarm0.command(duration=4, inorder=0, sleep=5)

swarm0.navigation(Point(5, 5, 0), relative=True)
swarm0.command(duration=4, inorder=0, sleep=5)

swarm0.navigation(Point(-5, 5, 0), relative=True)
swarm0.command(duration=4, inorder=0, sleep=5)

swarm0.navigation(Point(5, -5, 0), relative=True)
swarm0.command(duration=4, inorder=0, sleep=5)

swarm0.navigation(Point(-5, -5, 0), relative=True)
swarm0.command(duration=4, inorder=0, sleep=5)

for uav in uavs:
    uav.land(z=0, duration=2, sleep=0)

timeHelper.sleep(10)
