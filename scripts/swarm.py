import numpy as np

from point import Point
from formation import Formation
from uav import UAV, timeHelper

class Swarm:

    def __init__(self, uavs, name="swarm_0"):

        self.name       = name
        self.formation  = Formation()
        self.uavs       = uavs 

    def navigation(self, point:Point, relative=False):

        self.formation.shift(point, relative=relative)

    
    def rotation(self, angle, relative=True):

        self.formation.rotate(angle, relative=relative)

    
    def changeFormation(self, formation_type='rastgele', uav_distance=0.25, center=Point(None, None, 1), yaw=None):

        self.formation.createFormation(
            uav_points      = [uav.getPosition() for uav in self.uavs],
            formation_type  = formation_type,
            uav_distance    = uav_distance,
            center          = center,
            yaw             = yaw
        )



    def add(self, uavs):
        """
        suruye iha ekler\n
        \n
        uavs: suruye eklencek ihalar (UAV veri tipinde list olmalidir)\n
        """

        # buraya yaz



    
    def remove(self, uavs, z=None, name="removed_swarm"):
        """
        cikarilacak ihalari suruden cikarir yeni suru olusturur\n
        \n
        uavs: suruden cikarilacak ihalar (UAV veri tipinde list olmalidir)\n
        z: cikarlacak ihalarin yeni irtifasi
        """
        new_swarm = Swarm(uavs, name=name)

        ###yapilacaklar
        # uavs'teki ihalar self.uavs'ten cikarilmali
        # new_swarm.formation ozellikleri ayarlanmali (gerekirse yeni fonksiyon parameteleri eklenebilir)

        
        # buraya yaz


        return new_swarm
    

    def command(self, duration=2, inorder=0, sleep=0):

        for uav, to in zip(self.uavs, self.formation.formation_points):

            uav.goTo(to, duration=duration, sleep=inorder)

        timeHelper.sleep(sleep)

swarms = []
