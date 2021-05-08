#include<bits/stdc++.h>
using namespace std;

#ifndef GEOMETRY
#define GEOMETRY

struct Point{
    long double x, y, z;
    Point(double _x=0, double _y=0, double _z=0): x(_x), y(_y), z(_z){}

    bool operator==(Point A){
        return x == A.x && y == A.y && z == A.z;
    }
    void print(){
        std::cout << x << " " << y << " " << z << " ";
    }
    void err(){
        cerr << x << " " << y << " " << z << "\n";
    }
};

struct Cube{
    //constant
    int ix, iy, iz;
    int k;
    Point point;
    Cube* self = nullptr;
    Cube* next_k = nullptr;
    Cube* prev_k = nullptr;
    vector<Cube*> adj;
    
    // variable
    Cube* from = nullptr;
    long double val = 1e18;
    bool visited = false;

    Cube(Point _point=Point(), double _val=1e18, int _k=0):point(_point), val(_val), k(_k){}
    
    bool operator>(const Cube& A)const{
        return val < A.val;
    }
    bool operator<(const Cube& A)const{
        return val > A.val;
    }

    void reset(){
        from = self;
        val = 1e18;
        visited = false;
    }

    void debug(){
        cerr <<"("<< point.x << ", " << point.y << ", "<< point.z << ") [" << ix << "][" << iy << "][" << iz << "][" << k << "] " << val << "\n";
    }
};

long double dist(Point a, Point b){
    return sqrt((a.x-b.x)*(a.x-b.x) + (a.y-b.y)*(a.y-b.y) + (a.z-b.z)*(a.z-b.z));
}


#endif