from point import Point
from uav import UAV, uavs, timeHelper
from formation import Formation
from swarm import Swarm, swarms


swarm0 = Swarm(uavs)

timeHelper.sleep(10)

inventory = ['ucgen', 'kare', 'besgen', 'yildiz', 'V', 'hilal']

for formation_type in inventory[:4]:
    swarm0.changeFormation( 
        formation_type=formation_type, 
        uav_distance=1, 
        center=Point(None, None, 1)
    )

    swarm0.command(duration=5, inorder=0, sleep=10)


swarm1 = swarm0.remove(uavs[5:], z=2, new_formation='besgen')

swarm0.changeFormation('besgen')

swarm0.command(duration=5, inorder=0, sleep=0)
swarm1.command(duration=5, inorder=0, sleep=10)

swarm0.add(uavs[5:])
swarm0.changeFormation('kare')
swarm0.command(duration=5, inorder=0, sleep=10)

swarm0.rotation(0.2)
swarm0.command(duration=5, inorder=0, sleep=0.1)
swarm0.rotation(0.2)
swarm0.command(duration=5, inorder=0, sleep=0.1)
swarm0.rotation(0.2)
swarm0.command(duration=5, inorder=0, sleep=10)

swarm0.navigation(Point(-1, 0, 0), relative=True)
swarm0.command(duration=5, inorder=0, sleep=10)


swarm0.navigation(Point(0, -1, 0), relative=True)
swarm0.command(duration=5, inorder=0, sleep=10)


swarm0.navigation(Point(0, 0, -0.5), relative=True)
swarm0.command(duration=5, inorder=0, sleep=10)

for uav in uavs:
    uav.land(z=0, duration=2, sleep=0.5)

timeHelper.sleep(5)
