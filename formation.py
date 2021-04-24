import sys, os
import numpy as np
os.system('g++ -O3 -o bitmaskdp.exe bitmaskdp.cpp')

class Point:
      def __init__(self, x=0., y=0., z=0.):
            self.x = x
            self.y = y
            self.z = z

      def vector(self):
            return [self.x, self.y, self.z]
      
      def __getitem__(self, i):
            return self.vector()[i]

def distance(a:Point, b:Point):      
      dx = a.x - b.x
      dy = a.y - b.y
      dz = a.z - b.z
      return np.sqrt(dx*dx + dy*dy + dz*dz)



class Formation:

      def __init__(self):
            self.center = Point() # merkez
            self.yaw = 0 # formasyon acisi 
            self.uav_points = [] # ihalarin baslangic noktasi
            self.formation_type = None # formasyon tipi
            self.formation_points = [] # aciya bagli belirlenen formasyon noktalari
            
            self.N = 0 # iha sayisi

            self.__K = 10
            self.__angles = np.linspace(0, np.pi, self.__K, endpoint=False)
            self.__distance = None  
 
            self.inventory = {
                  'ucgen': self.ucgen,
                  'kare': self.kare,
                  'besgen': self.besgen,
                  'yildiz': self.yildiz,
                  'V': self.V,
                  'hilal': self.hilal,
                  'rastgele': self.rastgele
            }

      def createFormation(self, uav_points, formation_type='rastgele', uav_distance=0.25, center=Point(None, None, None), yaw=None):
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
            
            try:
                  for angle in angles:
                        
                        formation_points = self.__getFormationPoints(angle)
                        
                        dist, formation_points = self.__bitmaskdp(formation_points)

                        if self.__distance == None or self.__distance > dist:
                              self.__distance = dist
                              self.yaw = angle
                              self.formation_points = formation_points
            
            except:
                  print(f"{self.N} iha ile {formation_type} olusturma desteklenmiyor", file=sys.stderr)
                  
      
      def __getcenter(self, center):
            x = np.mean([p.x for p in self.uav_points]) if center.x == None else center.x
            y = np.mean([p.y for p in self.uav_points]) if center.y == None else center.y
            z = np.mean([p.z for p in self.uav_points]) if center.z == None else center.z
            return Point(x, y, z)

      
      
      def __bitmaskdp(self, formation_points):
            
            print(self.N, len(formation_points), file=open('points.in', 'w'))
            with open('points.in', 'a') as f:
                  np.savetxt(f, [p.vector() for p in self.uav_points], fmt='%.5f')
                  np.savetxt(f, [p.vector() for p in formation_points], fmt='%.5f')
            
            os.system('bitmaskdp.exe')

            with open('points.out', 'r') as f:
                  dist = float(f.readline())
                  chosen = np.loadtxt(f, int)

            return dist, formation_points[chosen]
                  
      
      
      def __getFormationPoints(self, yaw):
            return np.array(self.inventory[self.formation_type](self.center, yaw, self.N, self.uav_distance))
      
      
      
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
            edge_length = ((N+2)/3) * uav_distance  
            
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

                  #xy kenarı
                  edge_points.append(Point( gx + g - (i+1) * (g * (1+cos60)/((N+2)/3)),
                                            gy + (i+1) * (g * (sin60)/((N+2)/3))      ,                                
                                            gz                                        ))
                  #xz kenarı                          
                  edge_points.append(Point( gx + g - (i+1) * (g * (1+cos60)/((N+2)/3)),                           
                                            -(gy + (i+1) * (g * (sin60)/((N+2)/3)))   ,        
                                            gz                                        ))
                  #yz kenarı                          
                  edge_points.append(Point( gx - (g * cos60)                          ,
                                            gy + (g * sin60) - (i+1) * (uav_distance) ,
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


            return formation_points
      
      
      def kare(self, center, yaw, N, uav_distance):
            formation_points = []

            #buraya yaz

            return formation_points
      
      
      def besgen(self, center, yaw, N, uav_distance):
            formation_points = []

            assert N <= 5
            # 10 iha ile besgen olusturma eklenebilir (her kenarin ortasina bir iha)

            Rate = uav_distance
            gx = center.x
            gy = center.y
            gz = center.z

            #noktalar
            formation_points.append( Point( gx,                      gy+0.8506508083520*Rate, gz ) )
            formation_points.append( Point( gx+0.8090169943749*Rate, gy+0.2628655560596*Rate, gz ) )
            formation_points.append( Point( gx-0.8090169943749*Rate, gy+0.2628655560596*Rate, gz ) )
            formation_points.append( Point( gx-0.5*Rate,             gy-0.6881909602356*Rate, gz ) )
            formation_points.append( Point( gx+0.5*Rate,             gy-0.6881909602356*Rate, gz ) )

            #merkez etrafinda aci kadar gore dondurme
            for point in formation_points:
                  point.x -= gx
                  point.y -= gy
                  tempx = point.x * np.cos(yaw) - point.y * np.sin(yaw)
                  tempy = point.x * np.sin(yaw) + point.y * np.cos(yaw)
                  point.x = tempx+gx
                  point.y = tempy+gy

            return formation_points
      
      
      def yildiz(self, center, yaw, N, uav_distance):
            formation_points = []

            assert N <= 10
            
            #katsayilar
            Rate = uav_distance
            smallStarRate = 0.6180339887499
            bigStarRate = 1.6180339887499

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

            #merkez etrafinda aci kadar gore dondurme
            for point in formation_points:
                  point.x -= gx
                  point.y -= gy
                  tempx = point.x * np.cos(yaw) - point.y * np.sin(yaw)
                  tempy = point.x * np.sin(yaw) + point.y * np.cos(yaw)
                  point.x = tempx + gx
                  point.y = tempy + gy

            return formation_points
      
      
      def V(self, center, yaw, N, uav_distance):
            formation_points = []

            Rate = uav_distance
            gx = center.x
            gy = center.y
            gz = center.z
            sin60 = (1 / 2) * (3**(1/2))

            #noktalar
            formation_points.append( Point( gx - Rate / 2, gy ,               gz ) )
            formation_points.append( Point( gx + Rate / 2, gy ,               gz ) )
            formation_points.append( Point( gx - Rate,     gy + Rate * sin60, gz ) )
            formation_points.append( Point( gx + Rate,     gy + Rate * sin60, gz ) )
            formation_points.append( Point( gx ,           gy - Rate * sin60, gz ) )

            #merkez etrafinda aci kadar gore dondurme
            for point in formation_points:
                  point.x -= gx
                  point.y -= gy
                  tempx = point.x * np.cos(yaw) - point.y * np.sin(yaw)
                  tempy = point.x * np.sin(yaw) + point.y * np.cos(yaw)
                  point.x = tempx+gx
                  point.y = tempy+gy

            return formation_points
      
      
      def hilal(self, center, yaw, N, uav_distance):
            formation_points = []

            assert N <= 6

            Rate = uav_distance
            gx = center.x
            gy = center.y
            gz = center.z

            #noktalar
            formation_points.append(Point(gx-Rate*0.86602540378, gy+Rate*0.5, gz))
            formation_points.append(Point(gx-Rate*0.95105651629, gy-Rate*0.3090169943, gz))
            formation_points.append(Point(gx-Rate*0.40673664307, gy-Rate*0.9135454576, gz))
            formation_points.append(Point(gx+Rate*0.40673664307, gy-Rate*0.9135454576, gz))
            formation_points.append(Point(gx+Rate*0.95105651629, gy-Rate*0.3090169943, gz))
            formation_points.append(Point(gx+Rate*0.86602540378, gy+Rate*0.5, gz))

            #merkez etrafinda aci kadar gore dondurme
            for point in formation_points:
                  point.x -= gx
                  point.y -= gy
                  tempx = point.x * np.cos(yaw) - point.y * np.sin(yaw)
                  tempy = point.x * np.sin(yaw) + point.y * np.cos(yaw)
                  point.x = tempx+gx
                  point.y = tempy+gy

            return formation_points


if __name__ == '__main__':
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
            Point(0.5, 0.5, 0)
      ]

      formasyon = Formation()
      formasyon.createFormation(ihalar[:5], 'besgen', uav_distance=0.5, center=Point(None, None, 1)) 
      #test etmek icin formasyon tipini degistir

      from matplotlib import pyplot as plt

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
