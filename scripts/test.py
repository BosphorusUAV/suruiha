from point import Point
from uav import UAV, uavs, timeHelper
from formation import Formation
from swarm import Swarm, swarms


swarm0 = Swarm(uavs)

swarms.append(swarm0)

timeHelper.sleep(10)

swarm0.changeFormation( 
    formation_type='yildiz', 
    uav_distance=1, 
    center=Point(None, None, 2)
)

swarm0.command(duration=10, inorder=0, sleep=20)


for uav in uavs:
    uav.land(z=0, duration=2, sleep=0)

timeHelper.sleep(5)
