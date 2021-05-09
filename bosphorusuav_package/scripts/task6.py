from point import Point
from uav import UAV, uavs, timeHelper
from formation import Formation
from swarm import Swarm, swarms

n = 6
for uav in uavs[n:]:
    uav.land(z=0, duration=0, sleep=0)

"""
duration : inisten onceki bekleyis
"""

duration = 5

swarm0 = Swarm(uavs[:4])

timeHelper.sleep(10)

for uav in uavs[:4]:
    p = uav.getPosition()
    uav.goTo(Point(p.x, p.y, 1), duration=3)

timeHelper.sleep(10)
#swarm0.navigation(Point(0, 0, 1))
#swarm0.command(duration=2, inorder=0, sleep=10)

swarm0.changeFormation( 
    formation_type='kare', 
    uav_distance=1.41421, 
    center=Point(None, None, 1)
)

swarm0.command(duration=5, inorder=0, sleep=10)

swarm0.add([uavs[4]])
swarm0.changeFormation(
    formation_type='besgen',
    center=Point(None,None,1)
)
swarm0.command(duration=4.5, inorder=0, sleep=0)

timeHelper.sleep(15)

swarm0.add([uavs[5]])
swarm0.changeFormation(
    formation_type='altigen',
    center=Point(None,None,1)
)
swarm0.command(duration=4.5, inorder=0, sleep=10)

timeHelper.sleep(15)

swarm0.navigation(Point(0,0,-1), relative=True)
swarm0.command(duration=5, inorder=0, sleep=10)

for uav in uavs[:n-1]:
    uav.land(z=0, duration=2, sleep=0.5)
