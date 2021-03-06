#include<bits/stdc++.h>
#include"geometry.h"
#include"nearest_distance.h"
using namespace std;

#ifndef MODIFIED_DIJKSTRA
#define MODIFIED_DIJKSTRA

const double risk_threshold = 0.3;

double risk_func(double dist){
    if(dist <= risk_threshold) return 1;
    else return 0;
}
bool risk(Point& A, Point& B, vector<Point>& risk_points, Cube* s, Cube* e){
    double ret = 0;
    for(auto r : risk_points){
        if(
            dist(A, s->point) > risk_threshold &&
            dist(B, e->point) > risk_threshold &&
            risk_func(nearestDistance(A, B, r))) return true;
    }
    return false;
}

vector<Point> find_path(Cube* s, Cube* e, vector<Point>& risk_points){

    priority_queue<Cube> Q;
    s->val = 0;

    Q.push(*s);

    while(!Q.empty()){
        Cube* cube = Q.top().self;
        Cube* from = cube->from;
        Cube* next = cube->next_k;
        Q.pop();
        if(cube->visited) continue;
        cube->visited = true;
        // cube->debug();

        for(auto adj : cube->adj){
            if(!risk(adj->point, from->point, risk_points, s, e)){
                if(adj->val > from->val + dist(from->point, adj->point)){
                    adj->val = from->val + dist(from->point, adj->point);
                    adj->from = from;
                    Q.push(*adj);
                }
            }
        }
        if(next != nullptr && next->val >= cube->val){
            next->val = cube->val;
            next->from = cube;
            Q.push(*next);
        }
    }

    vector<Point> ret;
    Cube* curr = e;
    int cnt = 30;
    while(curr != nullptr){
        
        ret.push_back(curr->point);
        if(!curr->k) break;
        curr = curr->from;

        if(!--cnt){
            cerr << "PATH YOK!\n";
            return vector<Point>();
        }
    }

    ret.push_back(s->point);
    return ret;
}

#endif