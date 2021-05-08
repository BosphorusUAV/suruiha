#include<bits/stdc++.h>
#include"geometry.h"
using namespace std;

#ifndef NEAREST_DISTANCE
#define NEAREST_DISTANCE

Point normalize(Point a){
    long double length = sqrt(a.x * a.x + a.y * a.y + a.z * a.z);
    return Point(a.x / length, a.y / length, a.z / length);
}

Point crossProduct(Point a, Point b){
    return Point(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x);
}

long double dotProduct(Point a, Point b){
    return a.x * b.x + a.y * b.y + a.z * b.z;
}

long double nearestDistance(Point a1tmp, Point a2tmp, Point btmp){
    Point X, Y, Z, a1, a2, b;

    X = Point(a2tmp.x - a1tmp.x, a2tmp.y - a1tmp.y, a2tmp.z - a1tmp.z);
    X = normalize(X);
    Z = crossProduct(X, Point(btmp.x - a1tmp.x, btmp.y - a1tmp.y, btmp.z - a1tmp.z));
    Z = normalize(Z);
    Y = crossProduct(Z,X);

    const Point& O = a1tmp;

    long double x0 = 0, y0 = 0;
    long double x1 = sqrt((a2tmp.x - a1tmp.x) * (a2tmp.x - a1tmp.x) + (a2tmp.y - a1tmp.y) * (a2tmp.y - a1tmp.y) + (a2tmp.z - a1tmp.z) * (a2tmp.z - a1tmp.z)), y1 = 0;
    long double x2 = dotProduct(Point(btmp.x - a1tmp.x, btmp.y - a1tmp.y, btmp.z - a1tmp.z),X), y2 = dotProduct(Point(btmp.x - a1tmp.x, btmp.y - a1tmp.y, btmp.z - a1tmp.z),Y);        

    a1 = Point(x0, y0, 0);
    a2 = Point(x1, y1, 0);
    b = Point(x2, y2, 0);

    long double egim1a, egim1b, egim2a, egim2b, egim2, sbt1, sbt2;

    if(a1.x == a2.x && a1.y == a2.y){ // a1 esittir a2
        return sqrt((a1.x-b.x)*(a1.x-b.x)+(a1.y-b.y)*(a1.y-b.y));
    }

    double dist1 = sqrt(((a1.x-b.x)*(a1.x-b.x))+((a1.y-b.y)*(a1.y-b.y))), dist2 = sqrt(((a2.x-b.x)*(a2.x-b.x))+((a2.y-b.y)*(a2.y-b.y)));

    egim1a = a2.y - a1.y;
    egim1b = a2.x - a1.x;
    
    if(egim1a == 0){ // a1 ile a2 yan yana
        if(((a1.x <= b.x) && (b.x <= a2.x)) || ((a2.x <= b.x) && (b.x <= a1.x))){
            return abs(b.y - a1.y);
        }
        return min(dist1, dist2);
    }

    if(egim1b == 0){ // a1 ile a2 ust uste

        if(((a1.y <= b.y) && (b.y <= a2.y)) || ((a2.y <= b.y) && (b.y <= a1.y))){
            return abs(b.x - a1.x);
        }

        return min(dist1, dist2);
    }

    egim2a = -egim1b;
    egim2b = egim1a;

    egim2 = egim2a / egim2b;

    sbt1 = a1.y - egim2 * a1.x;
    sbt2 = a2.y - egim2 * a2.x;

    if((egim2 * b.x + sbt1 <= b.y && b.y <= egim2 * b.x +sbt2) || (egim2 * b.x + sbt2 <= b.y && b.y <= egim2 * b.x +sbt1)){
        long double kesisimx = ((b.y - egim2 * b.x) - (a1.y - (egim1a / egim1b) * a1.x)) / ((egim1a / egim1b) - egim2);
        long double kesisimy = kesisimx * egim2 + (b.y - egim2 * b.x);
        
        return sqrt((kesisimx-b.x)*(kesisimx-b.x)+(kesisimy-b.y)*(kesisimy-b.y));
    }

    return min(dist1, dist2);
}

#endif