import math
import time

import cflib.crtp
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.positioning.motion_commander import MotionCommander


def E(scf, height):
    with MotionCommander(scf) as mc:

        # CODE FOR E - 22 S
        mc.up(1.5)
        mc.move_distance(0.0, height*3/4, 0.0, velocity=0.7)
        mc.move_distance(0.0, 0.0, -height, velocity=0.8)
        mc.move_distance(0.0, -height*3/4, 0.0, velocity=0.7)
        time.sleep(.2)
        mc.move_distance(0.0, height*3/4, 0.0, velocity=0.7)
        time.sleep(.5)
        mc.move_distance(0.0, 0.0, height /2, velocity=0.7)
        time.sleep(.5)
        mc.move_distance(0.0, -height*3/4, 0.0, velocity=0.7)
        time.sleep(1)
        mc.land()


def W(scf, height):
    with MotionCommander(scf) as mc:
        mc.up(height * 1.5)
        mc.move_distance(0.0, -height * 1 / 4, -height, .4)
        time.sleep(.5)
        mc.move_distance(0.0, -height * 1 / 4, height * 3 / 4, .4)
        time.sleep(.5)
        mc.move_distance(0.0, -height * 1 / 4, -height * 3 / 4, .4)
        time.sleep(.5)
        mc.move_distance(0.0, -height * 1 / 4, height, .4)
        time.sleep(.5)
        mc.land()


def U(scf, height):
    with MotionCommander(scf) as mc:
        mc.up(height * 1.5)
        mc.down(height*3/4, .45)
        mc.move_distance(0.0, -height * 2/3, -height*1/3, .45)
        time.sleep(.2)
        mc.move_distance(0.0, -height * 2/3, height*1/3, .45)
        mc.up(height*3/4, .45)
        time.sleep(.5)
        mc.land()

# Change uris according to your setup
URI0 = 'radio://0/80/2M/E7E7E7E703'
URI1 = 'radio://0/80/2M/E7E7E7E712'
URI2 = 'radio://0/80/2M/E7E7E7E713'
#URI3 = 'radio://0/5/2M/E7E7E7E702'
#URI4 = 'radio://0/110/2M/E7E7E7E703'

# d: diameter of circle
# z: altituce
# letter: call function for the letter
params0 = {'letter': E}
params1 = {'letter': W}
params2 = {'letter': U}
params3 = {'letter': 1.0}
params4 = {'letter': 1.0}


uris = {
    URI0,
    URI1,
    URI2,
    # URI3,
    # URI4,
}

params = {
    URI0: [params0],
    URI1: [params1],
    URI2: [params2],
    # URI3: [params3],
    # URI4: [params4],
}


def reset_estimator(scf):
    cf = scf.cf
    cf.param.set_value('kalman.resetEstimation', '1')
    time.sleep(0.1)
    cf.param.set_value('kalman.resetEstimation', '0')
    time.sleep(2)


def poshold(cf, t, z):
    steps = t * 10

    for r in range(steps):
        cf.commander.send_hover_setpoint(0, 0, 0, z)
        time.sleep(0.1)


def run_sequence(scf, params):

    height = 1
    with MotionCommander(scf) as mc:

        # CODE FOR E - 22 S
        if crazyflie_counter == 0:
            mc.up(1.5)
            mc.move_distance(0.0, height*3/4, 0.0, velocity=0.7)
            mc.move_distance(0.0, 0.0, -height, velocity=0.8)
            mc.move_distance(0.0, -height*3/4, 0.0, velocity=0.7)
            time.sleep(.2)
            mc.move_distance(0.0, height*3/4, 0.0, velocity=0.7)
            time.sleep(.5)
            mc.move_distance(0.0, 0.0, height /2, velocity=0.7)
            time.sleep(.5)
            mc.move_distance(0.0, -height*3/4, 0.0, velocity=0.7)
            time.sleep(1)
            mc.land()

        # CODE FOR W: 23 s
        if crazyflie_counter == 1:
            mc.up(height * 1.5)
            mc.move_distance(0.0, -height * 1 / 4, -height, .4)
            time.sleep(.5)
            mc.move_distance(0.0, -height * 1 / 4, height * 3 / 4, .4)
            time.sleep(.5)
            mc.move_distance(0.0, -height * 1 / 4, -height * 3 / 4, .4)
            time.sleep(.5)
            mc.move_distance(0.0, -height * 1 / 4, height, .4)
            time.sleep(.5)
            mc.land()

        #  CODE FOR U:  23 S
        if crazyflie_counter == 2:
            mc.up(height* 1.5)
            mc.down(height*3/4, .45)
            mc.move_distance(0.0, -height * 2/3, -height*1/3, .45)
            # mc.right(height * 3 / 4, .2)
            mc.move_distance(0.0, -height * 2/3, height*1/3, .45)
            mc.up(height*3/4, .45)
            time.sleep(.5)
            mc.land()
    global crazyflie_counter
    crazyflie_counter += 1
    params['letter'](scf, height)

if __name__ == '__main__':
    cflib.crtp.init_drivers(enable_debug_driver=False)

    factory = CachedCfFactory(rw_cache='./cache')
    with Swarm(uris, factory=factory) as swarm:
        swarm.parallel(reset_estimator)
        swarm.parallel(run_sequence)

