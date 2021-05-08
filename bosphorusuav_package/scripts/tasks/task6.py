from point import Point
from uav import UAV, uavs, timeHelper
from formation import Formation
from swarm import Swarm, swarms

n = 4
for uav in uavs[n:]:
    uav.land(z=0, duration=2, sleep=0)

"""
duration : inisten onceki bekleyis
"""

duration = 30 

swarm0 = Swarm(uavs[:n])

timeHelper.sleep(10)

swarm0.navigation(Point(0, 0, 1))
swarm0.command(duration=2, inorder=0, sleep=10)

swarm0.changeFormation( 
    formation_type='kare', 
    uav_distance=1.41421, 
    center=Point(None, None, 1)
)
swarm0.command(duration=2, inorder=0, sleep=10)

swarm0.add(uavs[4])
swarm0.changeFormation('besgen')
swarm0.command(duration=4, inorder=0, sleep=10)


swarm0.add(uavs[5])
swarm0.changeFormation('altigen')
swarm0.command(duration=4, inorder=0, sleep=10)

timeHelper.sleep(duration)

for uav in uavs:
    uav.land(z=0, duration=2, sleep=0.5)
