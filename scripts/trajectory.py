import numpy as np
import sys, os
from point import Point

os.system('g++ -O3 -o trajectory_tracker.exe ./../src/trajectory_tracker.cpp')

input_file = 'trajectory.in'
output_file = 'trajectory.out'

def set_input(uavs, goals):
    with open(input_file, 'w') as f:
        print(len(uavs), file=f)

        for uav, goal in zip(uavs, goals):
            print(uav.x, uav.y, uav.z, goal.x, goal.y, goal.z, file=f)
        
        print(0, file=f)

def run():
    os.system("trajectory_tracker.exe " + input_file + ' ' + output_file)

def get_output(n):

    trajectory = []

    with open(output_file, 'r') as f:
        
        for uav in range(n):
            
            trajectory.append([])
            
            n_points = int(f.readline())
            
            for i in range(n_points):

                trajectory[uav].append(Point(vector=list(map(float, f.readline().split(' ')))))

    return trajectory


if __name__ == '__main__':
    from matplotlib import pyplot as plt
    
    ihalar = [
        Point(0, 0, 1),
        Point(3, 0, 1),
        Point(2, 0, 1),
        Point(0, 2, 1),
        Point(1, 3, 1),
        Point(0, 1, 1)
    ]
    hedefler = [
        Point(3, 3, 1),
        Point(0, 3, 1),
        Point(2, 3, 1),
        Point(3, 2, 1),
        Point(3, 1, 1),
        Point(1, 0, 1)
    ]
    # ihalar = [
    #     Point(1, 2, 1),
    #     Point(2, 2, 1),
    # ]
    # hedefler = [
    #     Point(3, 2, 1),
    #     Point(0, 2, 1),
    # ]

    set_input(ihalar, hedefler)
    run()

    def visualize(trajectory):

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        for iha in trajectory:
            ax.plot(
                [p.x for p in iha],
                [p.y for p in iha],
                [p.z for p in iha],
                # color='red',
                linewidth=3 
            )
            ax.scatter(
                iha[0].x,
                iha[0].y,
                iha[0].z,
                s=200,
                color='blue'
            )
            ax.scatter(
                iha[-1].x,
                iha[-1].y,
                iha[-1].z,
                s=500,
                color='black',
                marker='$iha$'
            )
        
        ax.scatter(0, 0, 0, color='white')
        ax.scatter(3.5, 3.5, 2, color='white')

        plt.show()

    visualize(get_output(len(ihalar)))
