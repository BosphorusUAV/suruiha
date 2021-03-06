from point import Point
from uav import UAV, uavs, timeHelper
from formation import Formation
from swarm import Swarm, swarms
from random import shuffle

shuffle(uavs)

n = 10
inventory = ['ucgen', 'kare', 'besgen', 'yildiz', 'V', 'hilal']

for uav in uavs[n:]:
    uav.land(z=0, duration=0, sleep=0)


uavs = uavs[:n]

swarm0 = Swarm(uavs)

timeHelper.sleep(10)

for uav in uavs:
    p = uav.getPosition()
    uav.goTo(Point(p.x, p.y, 1), duration=3)

swarm0.changeFormation( 
    formation_type='hilal',
    uav_distance=1,
    center=Point(None, None, 1)
)
swarm0.command(duration=2.5, inorder=0, sleep=15)

swarm0.remove([uavs[n-1]])
uavs[n-1].land(z=0, duration=2, sleep=0.5)

timeHelper.sleep(15)

swarm0.navigation(Point(0,0,-1), relative=True)
swarm0.command(duration=2.5, inorder=0, sleep=5)

for uav in uavs[:n-1]:
    uav.land(z=0, duration=0, sleep=0)
