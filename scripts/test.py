from uav_controller import UAVController
from formation import Formation
from point import Point

formasyon = Formation()
controller = UAVController()
formasyon.createFormation(
    [Point(vector=uav.position()) for uav in controller.uavs], 
    formation_type='yildiz', 
    uav_distance=1, 
    center=Point(None, None, 1)
)

for i in range(controller.s):
    controller.takeoff(i, z=0.1, duration=0.1, sleep=0)

controller.sleep(5)

for i in range(controller.s):
    controller.goTo(i, formasyon.formation_points[i], duration=5, sleep=0)

controller.sleep(20)

for i in range(controller.s):
    controller.land(i, z=0, duration=2, sleep=0)

controller.sleep(5)
