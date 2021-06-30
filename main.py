import logging
from scripts.controller import UAVController
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

from scripts.controller import UAVController



URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

logging.basicConfig(level=logging.ERROR)

position_estimate = [0, 0, 0]

def log_pos_callback(timestamp, data, logconf):
    print(data)
    global position_estimate
    position_estimate[0] = data['stateEstimate.x']
    position_estimate[1] = data['stateEstimate.y']
    position_estimate[2] = data['stateEstimate.z']


if __name__ == '__main__':
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        
        logconf = LogConfig(name='Position', period_in_ms=20)
        logconf.add_variable('stateEstimate.x', 'float')
        logconf.add_variable('stateEstimate.y', 'float')
        logconf.add_variable('stateEstimate.z', 'float')
        scf.cf.log.add_config(logconf)
        logconf.data_received_cb.add_callback(log_pos_callback)

        
        with MotionCommander(scf, default_height=0.2) as mc:
            
            uav = UAVController(mc)

            begin = time.time()

            while time.time() - begin < 1.5:

                uav.locationTuner(
                    position_estimate[0],
                    position_estimate[1],
                    position_estimate[2]
                )
                uav.move(0, 0, 0.5, duration=begin+2-time.time())

                print(f'remaining time: {time.time() - begin + 2} second')
                
            
