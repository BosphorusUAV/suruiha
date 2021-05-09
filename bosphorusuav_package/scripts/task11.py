from point import Point
from uav import UAV, uavs, timeHelper
from formation import Formation
from swarm import Swarm, swarms

n = 5
for uav in uavs[n:]:
    uav.land(z=0, duration=0, sleep=0)

uavs = uavs[:n]

swarm0 = Swarm(uavs)

timeHelper.sleep(10)

inventory = ['ucgen', 'kare', 'besgen', 'yildiz', 'V', 'hilal']

swarm0.changeFormation( 
    formation_type='besgen', 
    uav_distance=1, 
    center=Point(None, None, 1)
)
swarm0.command(duration=2.7, inorder=0, sleep=15)

swarm0.navigation(Point(-2, 0, 0), relative=True)
swarm0.command(duration=2.5, inorder=0, sleep=15)

swarm0.navigation(Point(0, -2, 0), relative=True)
swarm0.command(duration=2.5, inorder=0, sleep=15)

swarm0.navigation(Point(2, 2, 0), relative=True)
swarm0.command(duration=2.5, inorder=0, sleep=15)

for uav in uavs:
    uav.land(z=0, duration=2.5, sleep=0)

timeHelper.sleep(10)
