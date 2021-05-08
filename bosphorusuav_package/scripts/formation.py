import sys, os
import numpy as np
from point import Point, distance, rotate

os.system('g++ -O3 -o bitmaskdp.exe ./../src/bitmaskdp.cpp')

class Formation:

    def __init__(self):
        self.center           = Point() # merkez
        self.yaw              = 0       # formasyon acisi 
        self.uav_points       = []      # ihalarin baslangic noktasi
        self.formation_type   = None    # formasyon tipi
        self.formation_points = []      # aciya bagli belirlenen formasyon noktalari
        self.N                = 0       # iha sayisi

        self.__K = 10
        self.__angles = np.linspace(0, np.pi, self.__K, endpoint=False)
        self.__distance = None  
 
        self.inventory = {
            'ucgen':    self.ucgen,
            'kare':     self.kare,
            'besgen':   self.besgen,
            'altigen':  self.altigen,
            'yildiz':   self.yildiz,
            'V':        self.V,
            'hilal':    self.hilal,
            'rastgele': self.rastgele
        }

    def createFormation(self, uav_points, formation_type='rastgele', uav_distance=1, center=Point(None, None, None), yaw=None):
        """
        uav_points: ihalarin baslangic noktasi\n
        formation_type: formasyon tipi\n
        uav_distance: ihalar arasi mesafe\n
        center: formasyon merkezi (None ise agirlik merkezine gore hesaplanir)\n
        yaw: formasyon acisi (None ise optimum aci secilir)(radyan)\n
        """
        self.N = len(uav_points)

        if self.N == 0:
            print("Warning: formasyon olustururken iha sayisi 0 olamaz", file=sys.stderr)
            return 

        self.uav_points = np.array(uav_points)
        self.formation_type = formation_type

        self.uav_distance = uav_distance

        self.center = self.__getcenter(center)

        angles = self.__angles if yaw == None else [yaw]
        if self.N > 15:
            angles = [0]
        
        try:
            self.__distance = None
            for angle in angles:
                
                formation_points = self.__getFormationPoints(angle)
                
                dist, formation_points = self.__bitmaskdp(formation_points)

                if self.__distance == None or self.__distance > dist:
                    self.__distance = dist
                    self.yaw = angle
                    self.formation_points = formation_points
        
        except:
            print(f"{self.N} iha ile {formation_type} olusturma desteklenmiyor", file=sys.stderr)


    
    def rotate(self, angle):

        rotate(self.formation_points, self.center, angle)

        self.yaw += (self.yaw + angle) % (2*np.pi)


    
    def shift(self, vector:Point, relative=True):
        """
        merkezi ve tum formasyon noktalarini vector kadar kaydirir\n
        eger relative=False ise merkez vector noktasinda olacak sekilde kaydirilir
        """
        
        if not relative:
            vector.x -= self.center.x
            vector.y -= self.center.y
            vector.z -= self.center.z
        
        for point in self.formation_points:
            point.x += vector.x
            point.y += vector.y
            point.z += vector.z

        self.center.x += vector.x
        self.center.y += vector.y
        self.center.z += vector.z


    def __getcenter(self, center):
        return Point(
            np.mean([p.x for p in self.uav_points]) if center.x == None else center.x,
            np.mean([p.y for p in self.uav_points]) if center.y == None else center.y,
            np.mean([p.z for p in self.uav_points]) if center.z == None else center.z
        )

    
    
    def __bitmaskdp(self, formation_points):
        
        print(self.N, len(formation_points), file=open('points.in', 'w'))
        with open('points.in', 'a') as f:
            np.savetxt(f, [p.vector() for p in self.uav_points], fmt='%.5f')
            np.savetxt(f, [p.vector() for p in formation_points], fmt='%.5f')
        
        os.system('./bitmaskdp.exe')

        with open('points.out', 'r') as f:
            dist = float(f.readline())
            chosen = np.loadtxt(f, int)

        return dist, formation_points[chosen]
            
    
    
    def __getFormationPoints(self, yaw):
        return np.array(self.inventory[self.formation_type](self.center, yaw, self.N, self.uav_distance))[:self.N]
    
    
    def rastgele(self, center, yaw, N, uav_distance):
        formation_points = []
        
        for _ in range(N):
            
            eligible = False
            
            while not eligible:
                eligible = True
            
                point = Point(
                    (np.random.rand()-0.5)*uav_distance*N/2,
                    (np.random.rand()-0.5)*uav_distance*N/2,
                    0
                )
            
                for j in formation_points:
                    if distance(point, j) < uav_distance:
                        eligible = False
            
            formation_points.append(point)
    
        for point in formation_points:
            point.x += center.x
            point.y += center.y
            point.z = center.z

        return formation_points
            

    def ucgen(self, center, yaw, N, uav_distance):
        formation_points = []

        #ucgenin bir kenar uzunluğu
        edge_length = ((int)((N+2)/3)) * uav_distance  
        
        #agırlık merkezinin koselere uzaklığı
        g = edge_length / (3 ** (0.5))

        sin60 = (np.sin((np.pi)/3))
        cos60 = (np.cos((np.pi)/3))

        gx = center.x
        gy = center.y
        gz = center.z

        #koseler
        x_vertex = Point( gx + g           , gy               , gz )
        y_vertex = Point( gx - (g * cos60) , gy + (g * sin60) , gz )
        z_vertex = Point( gx - (g * cos60) , gy - (g * sin60) , gz ) 

        #kenarlar uzerindeki noktalar
        edge_points = []
        
        for i in range((int)((N-1)/3)):

            a = (int) ((N+2)/3)

            #xy kenarı
            edge_points.append(Point( gx + g - (i+1) * (g * (1+cos60)/a),
                              gy + (i+1) * (g * (sin60)/a)      ,                                
                              gz                                        ))
            #xz kenarı                          
            edge_points.append(Point( gx - (g * cos60) + (i+1) * (g * (1+cos60)/a),                           
                              gy - (g * sin60) + (i+1) * (g * sin60/a),        
                              gz                                        ))
            #yz kenarı                          
            edge_points.append(Point( gx - (g * cos60)                          ,
                              gy + (g * sin60) - (i+1) * (2 * g * sin60 / a) ,
                              gz                                        ))
        
        if N == 1:

            #koseler
            formation_points.append(x_vertex)

        elif N == 2:

            #koseler
            formation_points.append(x_vertex)
            formation_points.append(y_vertex)

        else:

            #koseler
            formation_points.append(x_vertex)
            formation_points.append(y_vertex)
            formation_points.append(z_vertex)
            
            #kenarlar uzerindeki noktalar
            for i in range(N-3):

                formation_points.append(edge_points[i])      


        #merkez etrafinda aci kadar gore dondurme
        rotate(formation_points, center, yaw)

        return formation_points
    
    
    def kare(self, center, yaw, N, uav_distance):
        formation_points = []

        # add (N - 4) / 4 points to each side
        pointsNeeded = int(np.ceil((N - 4) / 4))
        distanceNew = uav_distance * (pointsNeeded + 1)

        gx = center.x
        gy = center.y
        gz = center.z

        # calculate main 4 points
        formation_points.append(Point(gx+distanceNew/2, gy+distanceNew/2, gz))
        formation_points.append(Point(gx+distanceNew/2, gy-distanceNew/2, gz))
        formation_points.append(Point(gx-distanceNew/2, gy-distanceNew/2, gz))
        formation_points.append(Point(gx-distanceNew/2, gy+distanceNew/2, gz))

        for i in range(1, pointsNeeded + 1):
            formation_points.append(
                Point(formation_points[0].x, formation_points[0].y - uav_distance * i, formation_points[0].z))
            formation_points.append(
                Point(formation_points[1].x - uav_distance * i, formation_points[1].y, formation_points[1].z))
            formation_points.append(
                Point(formation_points[2].x, formation_points[2].y + uav_distance * i, formation_points[2].z))
            formation_points.append(
                Point(formation_points[3].x + uav_distance * i, formation_points[3].y, formation_points[3].z))

        # merkez etrafinda aci kadar gore dondurme
        rotate(formation_points, center, yaw)

        return formation_points
    
    def besgen(self, center, yaw, N, uav_distance):
        formation_points = []
        
        assert N<=20

        Rate = uav_distance
        gx = center.x
        gy = center.y
        gz = center.z

        Rate*=(N-1)//5+1

        #kose noktalar
        A= Point( gx,                      gy+0.8506508083520*Rate, gz )
        B= Point( gx-0.8090169943749*Rate, gy+0.2628655560596*Rate, gz )
        C= Point( gx+0.8090169943749*Rate, gy+0.2628655560596*Rate, gz )
        D= Point( gx-0.5*Rate,             gy-0.6881909602356*Rate, gz )
        E= Point( gx+0.5*Rate,             gy-0.6881909602356*Rate, gz )

        formation_points.append( A )
        formation_points.append( B )
        formation_points.append( C )
        formation_points.append( D )
        formation_points.append( E )

        #orta noktalar
        for i in range(1,(N-1)//5+1):
            formation_points.append( Point( A.x+i*(B.x-A.x)/((N-1)//5+1) , A.y-i*(A.y-B.y)/((N-1)//5+1) , gz ) )
            formation_points.append( Point( A.x-i*(A.x-C.x)/((N-1)//5+1) , A.y-i*(A.y-C.y)/((N-1)//5+1) , gz ) )
            formation_points.append( Point( D.x-i*(D.x-B.x)/((N-1)//5+1) , D.y+i*(B.y-D.y)/((N-1)//5+1) , gz ) )
            formation_points.append( Point( C.x-i*(C.x-E.x)/((N-1)//5+1) , C.y-i*(C.y-E.y)/((N-1)//5+1) , gz ) )
            formation_points.append( Point( D.x+i*(E.x-D.x)/((N-1)//5+1) , D.y+i*(D.y-E.y)/((N-1)//5+1) , gz ) )



        #merkez etrafinda aci kadar gore dondurme
        rotate(formation_points, center, yaw)

        return formation_points[:N]
    
    def altigen(self, center, yaw, N, uav_distance):
        formation_points = []

        assert N <= 6

        gx = center.x
        gy = center.y
        gz = center.z

        sin30 = (np.sin((np.pi)/6))
        cos30 = (np.cos((np.pi)/6))

        formation_points.append(Point(gx - uav_distance, gy, gz))
        formation_points.append(Point(gx + uav_distance, gy, gz))
        formation_points.append(Point(gx - uav_distance * sin30, gy + uav_distance * cos30, gz))
        formation_points.append(Point(gx + uav_distance * sin30, gy + uav_distance * cos30, gz))
        formation_points.append(Point(gx - uav_distance * sin30, gy - uav_distance * cos30, gz))
        formation_points.append(Point(gx + uav_distance * sin30, gy - uav_distance * cos30, gz))

        rotate(formation_points, center, yaw)
        
        return formation_points[:N]

    
    def yildiz(self, center, yaw, N, uav_distance):
        formation_points = []

        assert N <= 20
        
        #katsayilar
        Rate = uav_distance
        smallStarRate = 0.6180339887499
        bigStarRate = 1.6180339887499

        if N>10:
            Rate*=2

        #merkez noktasi
        gx = center.x
        gy = center.y
        gz = center.z

        #buyuk besgenin noktalari
        formation_points.append( Point( gx,                                  gy+0.8506508083520*Rate*bigStarRate, gz ) )
        formation_points.append( Point( gx-0.8090169943749*Rate*bigStarRate, gy+0.2628655560596*Rate*bigStarRate, gz ) )
        formation_points.append( Point( gx+0.8090169943749*Rate*bigStarRate, gy+0.2628655560596*Rate*bigStarRate, gz ) )
        formation_points.append( Point( gx-0.5*Rate*bigStarRate,             gy-0.6881909602356*Rate*bigStarRate, gz ) )
        formation_points.append( Point( gx+0.5*Rate*bigStarRate,             gy-0.6881909602356*Rate*bigStarRate, gz ) )
        
        #kucuk besgenin noktalari
        formation_points.append( Point( gx,                                    gy-0.8506508083520*Rate*smallStarRate, gz ) )
        formation_points.append( Point( gx-0.8090169943749*Rate*smallStarRate, gy-0.2628655560596*Rate*smallStarRate, gz ) )
        formation_points.append( Point( gx+0.8090169943749*Rate*smallStarRate, gy-0.2628655560596*Rate*smallStarRate, gz ) )
        formation_points.append( Point( gx-0.5*Rate*smallStarRate,             gy+0.6881909602356*Rate*smallStarRate, gz ) )
        formation_points.append( Point( gx+0.5*Rate*smallStarRate,             gy+0.6881909602356*Rate*smallStarRate, gz ) )

        #orta noktalar
        formation_points.append( Point( (formation_points[0].x+formation_points[8].x)/2 , (formation_points[0].y+formation_points[8].y)/2 , gz ) )
        formation_points.append( Point( (formation_points[0].x+formation_points[9].x)/2 , (formation_points[0].y+formation_points[9].y)/2 , gz ) )
        formation_points.append( Point( (formation_points[1].x+formation_points[8].x)/2 , (formation_points[1].y+formation_points[8].y)/2 , gz ) )
        formation_points.append( Point( (formation_points[1].x+formation_points[6].x)/2 , (formation_points[1].y+formation_points[6].y)/2 , gz ) )
        formation_points.append( Point( (formation_points[2].x+formation_points[9].x)/2 , (formation_points[2].y+formation_points[9].y)/2 , gz ) )
        formation_points.append( Point( (formation_points[2].x+formation_points[7].x)/2 , (formation_points[2].y+formation_points[7].y)/2 , gz ) )
        formation_points.append( Point( (formation_points[3].x+formation_points[6].x)/2 , (formation_points[3].y+formation_points[6].y)/2 , gz ) )
        formation_points.append( Point( (formation_points[3].x+formation_points[5].x)/2 , (formation_points[3].y+formation_points[5].y)/2 , gz ) )
        formation_points.append( Point( (formation_points[4].x+formation_points[5].x)/2 , (formation_points[4].y+formation_points[5].y)/2 , gz ) )
        formation_points.append( Point( (formation_points[4].x+formation_points[7].x)/2 , (formation_points[4].y+formation_points[7].y)/2 , gz ) )

        #merkez etrafinda aci kadar gore dondurme
        rotate(formation_points, center, yaw)

        return formation_points[:N]
    
    
    def V(self, center, yaw, N, uav_distance, alfa = (np.pi)/3):
        formation_points = []

        Rate = uav_distance * 2
        gx = center.x
        gy = center.y
        gz = center.z
        
        sinal = np.sin(alfa / 2)
        cosal = np.cos(alfa / 2)

        #noktalar
        formation_points.append( Point( gx , gy - Rate * cosal, gz ) )
        for i in range(1, int(N / 2) + 1):
            formation_points.append(
                Point(formation_points[0].x - i * Rate * sinal / 2, formation_points[0].y + i * Rate * cosal / 2, formation_points[0].z))
            formation_points.append(
                Point(formation_points[0].x + i * Rate * sinal / 2, formation_points[0].y + i * Rate * cosal / 2, formation_points[0].z))

                
        #merkez etrafinda aci kadar gore dondurme
        rotate(formation_points, center, yaw)

        return formation_points[:N]
    
    
    def hilal(self, center, yaw, N, uav_distance):
        formation_points = []
        Rate = uav_distance
        gx = center.x
        gy = center.y
        gz = center.z
        
        if N>6:
            Rate = Rate * 1.5
            
        if N>11:
            Rate = Rate * 1.5
        
        #noktalar
        formation_points.append(Point(gx-Rate*0.86602540378, gy+Rate*0.5,          gz))
        formation_points.append(Point(gx-Rate*0.95105651629, gy-Rate*0.3090169943, gz))
        formation_points.append(Point(gx-Rate*0.40673664307, gy-Rate*0.9135454576, gz))
        formation_points.append(Point(gx+Rate*0.40673664307, gy-Rate*0.9135454576, gz))
        formation_points.append(Point(gx+Rate*0.95105651629, gy-Rate*0.3090169943, gz))
        formation_points.append(Point(gx+Rate*0.86602540378, gy+Rate*0.5,          gz))
        formation_points.append(Point(gx-Rate*0.99452189536, gy+Rate*0.10452846326, gz))
        formation_points.append(Point(gx-Rate*0.74314482547, gy-Rate*0.66913060635, gz))
        formation_points.append(Point(gx, gy-Rate, gz))
        formation_points.append(Point(gx+Rate*0.74314482547, gy-Rate*0.66913060635, gz))
        formation_points.append(Point(gx+Rate*0.99452189536, gy+Rate*0.10452846326, gz))
        formation_points.append(Point(gx-Rate*0.95105651629, gy+Rate*0.30901699437, gz))
        formation_points.append(Point(gx-Rate*0.99452189536, gy-Rate*0.10452846326, gz))
        formation_points.append(Point(gx-Rate*0.86602540378, gy-Rate*0.5, gz))
        formation_points.append(Point(gx-Rate*0.58778525229, gy-Rate*0.80901699437, gz))
        formation_points.append(Point(gx-Rate*0.20791169081, gy-Rate*0.97814760073, gz))
        formation_points.append(Point(gx+Rate*0.20791169081, gy-Rate*0.97814760073, gz))
        formation_points.append(Point(gx+Rate*0.58778525229, gy-Rate*0.80901699437, gz))
        formation_points.append(Point(gx+Rate*0.86602540378, gy-Rate*0.5, gz))
        formation_points.append(Point(gx+Rate*0.99452189536, gy-Rate*0.10452846326, gz))
        formation_points.append(Point(gx+Rate*0.95105651629, gy+Rate*0.30901699437, gz))

        #merkez etrafinda aci kadar gore dondurme
        rotate(formation_points, center, yaw)

        return formation_points[:N]


if __name__ == '__main__':
    from matplotlib import pyplot as plt
    from time import time

    ihalar = [
        Point(0, 0, 0),
        Point(1, 1, 0),
        Point(1, 0, 0),
        Point(0, 1, 0),
        Point(-1, -1, 0),
        Point(-1, 0, 0),
        Point(0, -1, 0),
        Point(0.5, -0.5, 0),
        Point(-0.5, 0.5, 0),
        Point(0.5, 0.5, 0),
        Point(0.05, 0.05, 0),
        Point(0.05, 0.05, 0),
        Point(0.05, 0.05, 0),
        Point(0.05, 0.05, 0),
        Point(0.05, 0.05, 0),
        Point(0.05, 0.05, 0),
        Point(0.05, 0.05, 0),
        Point(0.05, 0.05, 0),
        Point(0.05, 0.05, 0),
        Point(0.05, 0.05, 0),
        Point(0.05, 0.05, 0),
        Point(0.05, 0.05, 0),
        Point(0.05, 0.05, 0),
        Point(0.05, 0.05, 0),
        Point(0.05, 0.05, 0)
    ]

    formasyon = Formation()
    b = time()
    formasyon.createFormation(ihalar[:20], 'ucgen', uav_distance=1, center=Point(None, None, 1)) 
    print(time()-b, 'second')
    #test etmek icin formasyon tipini degistir


    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    
    for i in range(formasyon.N):
        ax.scatter(formasyon.uav_points[i][0], formasyon.uav_points[i][1], formasyon.uav_points[i][2], s = 500, color='black', marker='$İHA$')
        ax.scatter(formasyon.formation_points[i][0], formasyon.formation_points[i][1], formasyon.formation_points[i][2], s = 200, color='blue')
        ax.plot(
            [formasyon.uav_points[i].x, formasyon.formation_points[i].x], 
            [formasyon.uav_points[i].y, formasyon.formation_points[i].y],
            [formasyon.uav_points[i].z, formasyon.formation_points[i].z], 
            linewidth=3, color='red')

    plt.show()
