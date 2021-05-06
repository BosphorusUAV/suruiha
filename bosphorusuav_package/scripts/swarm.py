import numpy as np

from point import Point
from formation import Formation
from uav import UAV, timeHelper

class Swarm:

    def __init__(self, uavs, name="swarm_0"):

        self.name       = name
        self.formation  = Formation()
        self.uavs       = uavs 

        self.changeFormation(uav_distance=1)

    def navigation(self, point:Point, relative=False):

        self.formation.shift(point, relative=relative)

    
    def rotation(self, angle, relative=True):
        
        if not relative:
            angle -= self.formation.yaw

        self.formation.rotate(angle)

    
    def changeFormation(self, formation_type='rastgele', uav_distance=None, center=Point(None, None, None), yaw=None):

        if uav_distance == None:
            uav_distance = self.formation.uav_distance

        self.formation.createFormation(
            uav_points      = [uav.getPosition() for uav in self.uavs],
            formation_type  = formation_type,
            uav_distance    = uav_distance,
            center          = center,
            yaw             = yaw
        )

    def update(self):
        """
        surudeki yeni iha sayisina gore formasyonu gunceller
        """

        self.changeFormation(
            formation_type  = self.formation.formation_type,
            uav_distance    = self.formation.uav_distance,
            center          = self.formation.center,
            yaw             = self.formation.yaw
        )

    def add(self, uavs):
        """
        suruye iha ekler\n
        uavs: suruye eklencek ihalar (UAV veri tipinde list olmalidir)\n
        """

        for uav in uavs:
            self.uavs.append(uav)

        self.update()


    
    def remove(self, uavs, z=None, new_formation=None, name="removed_swarm"):
        """
        cikarilacak ihalari suruden cikarir yeni suru olusturur\n
        \n
        uavs: suruden cikarilacak ihalar (UAV veri tipinde list olmalidir)\n
        z: cikarlacak ihalarin yeni irtifasi
        """
        self.uavs = [uav for uav in self.uavs if not uav in uavs]

        if z == None:
            z = self.formation.center.z + 0.5
        if new_formation == None:
            new_formation = self.formation.formation_type

        new_swarm = Swarm(uavs, name=name)
        new_swarm.changeFormation(
            formation_type  = new_formation,
            uav_distance    = self.formation.uav_distance,
            center          = Point(None, None, z),
            yaw             = self.formation.yaw
        )

        self.update()

        return new_swarm
    

    def command(self, duration=2, inorder=0, sleep=0):
        """
        ihalari belirlenen noktalara gonderir
        """

        for uav, to in zip(self.uavs, self.formation.formation_points):

            uav.goTo(to, duration=duration, sleep=inorder)

        timeHelper.sleep(sleep)

swarms = []
