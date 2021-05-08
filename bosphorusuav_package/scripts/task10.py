from point import Point
from uav import UAV, uavs, timeHelper
from formation import Formation
from swarm import Swarm, swarms

n = 10
for uav in uavs[n:]:
    uav.land(z=0, duration=2, sleep=0)

uavs = uavs[:n]


swarm0 = Swarm(uavs)

timeHelper.sleep(4)

inventory = ['ucgen', 'kare', 'besgen', 'yildiz', 'V', 'hilal']

for formation_type in inventory:
    swarm0.changeFormation( 
        formation_type=formation_type, 
        uav_distance=1, 
        center=Point(None, None, 1)
    )
    swarm0.command(duration=3, inorder=0, sleep=5)


for uav in uavs:
    uav.land(z=0, duration=2, sleep=0)

timeHelper.sleep(10)
