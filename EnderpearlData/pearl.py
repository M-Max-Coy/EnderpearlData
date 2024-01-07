import math
import random
import pandas as pd

class Pearl:

    def __init__(self, x, y, z, yaw, pitch):
        # Set variables
        self.prevx = x
        self.prevy = y
        self.prevz = z
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch
        self.vx = 0
        self.vz = 0
        self.vy = 0

        # Calculations
        self.x = self.x
        self.y = self.y + (1.8*0.85)
        self.z = self.z
        self.x -= math.cos(self.yaw/180.0 * math.pi) * 0.16
        self.y -= 0.1
        self.z -= math.sin(self.yaw/180 * math.pi) * 0.16
        f = 0.4
        self.vx = -1 * math.sin(self.yaw/180 * math.pi) * math.cos(self.pitch/180 * math.pi) * f
        self.vz = math.cos(self.yaw/180 * math.pi) * math.cos(self.pitch/180 * math.pi) * f
        self.vy = -1 * math.sin(self.pitch/180 * math.pi) * f
        self.set_throwable_heading()

    def set_throwable_heading(self):
        f = math.sqrt(self.vx*self.vx + self.vy*self.vy + self.vz*self.vz)
        self.vx = self.vx/f
        self.vy = self.vy/f
        self.vz = self.vz/f
        self.vx = self.vx + random.gauss(0,1) * 0.0075
        self.vy = self.vy + random.gauss(0,1) * 0.0075
        self.vz = self.vz + random.gauss(0,1) * 0.0075
        self.vx = self.vx * 1.5
        self.vy = self.vy * 1.5
        self.vz = self.vz * 1.5

    def update(self):
        self.prevx = self.x
        self.prevy = self.y
        self.prevz = self.z
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz
        f2 = 0.99
        f3 = 0.03
        self.vx *= f2
        self.vy *= f2
        self.vz *= f2
        self.vy -= f3

    def __str__(self):
        return f"x: {self.x} y: {self.y} z: {self.z} vx: {self.vx} vy: {self.vy} vz: {self.vz} prevx: {self.prevx} prevy: {self.prevy} prevz: {self.prevz}"
    
def get_average_pearl(x, y, z, yaw, pitch, ground):
    sumx = 0
    sumy = 0
    sumz = 0
    trials = 1000
    for i in range (trials):
        pearl = Pearl(x,y,z,yaw,pitch)
        while pearl.y > ground or pearl.vy > 0:
            pearl.update()
        sumx+=pearl.prevx
        sumy+=pearl.prevy
        sumz+=pearl.prevz
    return (sumx/trials, sumy/trials, sumz/trials)

def find_optimal_pitch(x, y, z, yaw, pitch, ground, lb, ub):
    pitch = lb
    max_dist = -100
    opt = 0
    while (pitch <= ub):
        if (not possible_to_reach_ground(y, ground, pitch)):
            pitch += 1
            continue
        cur_dist = get_average_pearl(x,y,z,yaw,pitch,ground)
        if (cur_dist[2] > max_dist):
            max_dist = cur_dist[2]
            opt = pitch
        pitch += 1
    return (opt, max_dist)

def possible_to_reach_ground(y, ground, pitch):
    pearl = Pearl(0.0, y, 0.0, 0.0, pitch)
    max_height = y
    while (pearl.vy > 0):
        pearl.update()
        max_height = max(max_height, pearl.y)
    return max_height > ground

def main():
    x = 0.0
    y = 255.09
    z = 0.0
    yaw = 0.0
    pitch = -15.0
    # res = find_optimal_pitch(x,y,z,yaw,pitch,0.0,-45, 0)
    # print(res)

    heights = [-1*(i)-1 for i in range(29, -1, -1)] + [i for i in range(256)]
    results = [find_optimal_pitch(x,y,z,yaw,pitch,y-height,-90, 0) for height in heights]
    angles = [result[0] for result in results]
    distances = [result[1] for result in results]
    data = {
        'Height' : heights,
        'Optimal Angle' : angles,
        'Average Distance' : distances
    }
    df = pd.DataFrame(data)
    df.to_excel("output_data.xlsx")

main()