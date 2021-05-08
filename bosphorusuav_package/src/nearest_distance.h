#include<bits/stdc++.h>
#include"geometry.h"
using namespace std;

#ifndef NEAREST_DISTANCE
#define NEAREST_DISTANCE

double distanceBetween2Points(Point a, Point b){
    double xfark = (a.x - b.x)*(a.x - b.x);
    double yfark = (a.y - b.y)*(a.y - b.y);
    double zfark = (a.z - b.z)*(a.z - b.z);
    return sqrt(xfark + yfark + zfark);
}

double nearestDistance(Point a1tmp, Point a2tmp, Point btmp){
    if(a1tmp == a2tmp){
        return distanceBetween2Points(a1tmp,btmp);
    }
    
    double lineSegment, side1, side2, halfPerimeter, area, bx, by;
    Point a1, a2, b;

    lineSegment = distanceBetween2Points(a1tmp, a2tmp);
    side1 = distanceBetween2Points(a1tmp, btmp);
    side2 = distanceBetween2Points(a2tmp, btmp);

    halfPerimeter = (lineSegment + side1 + side2)/2.0;
    area = sqrt(halfPerimeter * (halfPerimeter - side1) * (halfPerimeter - side2) * (halfPerimeter - lineSegment));

    by = ((2 * area) / lineSegment);
    bx = (side2*side2 - side1*side1 - lineSegment*lineSegment)/(-2*lineSegment);

    if(lineSegment < 0.00001) lineSegment = 0;
    if(abs(bx) < 0.00001) bx = 0;
    if(abs(by) < 0.00001) by = 0;
    
    a1 = Point(0, 0, 0);
    a2 = Point(lineSegment, 0, 0);
    b = Point(bx, by, 0);

    double egim1a, egim1b, egim2a, egim2b, egim2, sbt1, sbt2;

    if(a1.x == a2.x && a1.y == a2.y){ // a1 esittir a2
        return sqrt((a1.x-b.x)*(a1.x-b.x)+(a1.y-b.y)*(a1.y-b.y));
    }

    double dist1 = sqrt(((a1.x-b.x)*(a1.x-b.x))+((a1.y-b.y)*(a1.y-b.y))), dist2 = sqrt(((a2.x-b.x)*(a2.x-b.x))+((a2.y-b.y)*(a2.y-b.y)));

    egim1a = a2.y - a1.y;
    egim1b = a2.x - a1.x;

    if(abs(egim1a) < 0.00001){ // a1 ile a2 yan yana
        if(((a1.x <= b.x) && (b.x <= a2.x)) || ((a2.x <= b.x) && (b.x <= a1.x))){
            return abs(b.y - a1.y);
        }
        return min(dist1, dist2);
    }

    if(abs(egim1b) < 0.00001){ // a1 ile a2 ust uste

        if(((a1.y <= b.y) && (b.y <= a2.y)) || ((a2.y <= b.y) && (b.y <= a1.y))){
            return abs(b.x - a1.x);
        }

        return min(dist1, dist2);
    }

    egim2a = -egim1b;
    egim2b = egim1a;

    egim2 = egim2a / egim2b;
    cout << egim2b << endl;
    sbt1 = a1.y - egim2 * a1.x;
    sbt2 = a2.y - egim2 * a2.x;

    if((egim2 * b.x + sbt1 <= b.y && b.y <= egim2 * b.x +sbt2) || (egim2 * b.x + sbt2 <= b.y && b.y <= egim2 * b.x +sbt1)){
        double kesisimx = ((b.y - egim2 * b.x) - (a1.y - (egim1a / egim1b) * a1.x)) / ((egim1a / egim1b) - egim2);
        double kesisimy = kesisimx * egim2 + (b.y - egim2 * b.x);
        
        return sqrt((kesisimx-b.x)*(kesisimx-b.x)+(kesisimy-b.y)*(kesisimy-b.y));
    }

    return min(dist1, dist2);
}

#endif
