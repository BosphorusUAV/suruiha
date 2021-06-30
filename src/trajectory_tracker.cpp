#include<bits/stdc++.h>
#include"geometry.h"
#include"nearest_distance.h"
#include"modified_dijkstra.h"
using namespace std;

const double X = 3.5, Y = 3.5, Z = 2; 
const double EX = 0.2, EY = 0.2, EZ = 0.2;
const int K = 5;
const int NX = X/EX, NY = Y/EY, NZ = Z/EZ;

int grid[NX][NY][NZ];


int path[6][3] = {
    {1, 0, 0},
    {-1, 0, 0},
    {0, 1, 0},
    {0, -1, 0},
    {0, 0, 1},
    {0, 0, -1}
};


vector<Point> risk_points;


Cube cubes[NX+3][NY+3][NZ+3][K+1];

Cube* inside(Point A, int k = 0){
    int ix = A.x / EX;
    int iy = A.y / EY;
    int iz = A.z / EZ;
    return &cubes[ix][iy][iz][k];
}



int main(int f, char** files){
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    if(f > 1){
        const char* input_file = files[1];
        freopen(input_file, "r", stdin);
    }
    if(f > 2){
        const char* output_file = files[2];
        freopen(output_file, "w", stdout);
    }

    //////////////////// INITIALIZATION //////////////////////////

    for(int ix = 0; ix <= NX; ix++){
        for(int iy = 0; iy <= NY; iy++){
            for(int iz = 0; iz <= NZ; iz++){
                for(int k = 0; k < K; k++){
                    Cube* cube = &cubes[ix][iy][iz][k];
                    cube->ix = ix;
                    cube->iy = iy;
                    cube->iz = iz;
                    cube->k = k;
                    cube->point = Point(EX*ix, EY*iy, EZ*iz);
                    cube->from = cube->self = cube;
                    if(k) cube->prev_k = &cubes[ix][iy][iz][k-1];
                    if(k+1<K) cube->next_k = &cubes[ix][iy][iz][k+1];

                    for(int i = 0; i < 6; i++){
                        int x = ix + path[i][0];
                        int y = iy + path[i][1];
                        int z = iz + path[i][2];
                        if(0 <= x && x <= NX && 0 <= y && y <= NY && 0 <= z && z <= NZ){
                            cube->adj.push_back(&cubes[x][y][z][k]);
                        }
                    }
                }
            }
        }
    }
    ////////////////////////////////////////////////////////////////
    

    int n;
    cin >> n;

    vector<Point> S, E;

    for(int i = 0; i < n; i++){
        double sx, sy, sz, ex, ey, ez;
        cin >> sx >> sy >> sz >> ex >> ey >> ez;
        S.push_back(Point(sx, sy, sz));
        E.push_back(Point(ex, ey, ez));
    }

    for(auto p : S) risk_points.push_back(p);
    for(auto p : E) risk_points.push_back(p);


    int r;
    cin >> r;
    for(int i = 0; i < r; i++){
        double x, y, z;
        cin >> x >> y >> z;
        risk_points.push_back(Point(x, y, z));
    }

    for(int i = 0; i < n; i++){
        Cube* s = inside(S[i], 0);
        Cube* e = inside(E[i], K-1);

        auto P = find_path(s, e, risk_points);
        
        cout << P.size() << "\n";
        for(auto p : P) cout << p.x << " " << p.y << " " << p.z << "\n";
        
        
        for(int j = 1; j < P.size(); j++){
            for(double a = 0; a <= 1; a += 0.1){
                risk_points.push_back(
                    Point(
                        P[j-1].x + (P[j].x - P[j-1].x) * a,
                        P[j-1].y + (P[j].y - P[j-1].y) * a,
                        P[j-1].z + (P[j].z - P[j-1].z) * a
                    )
                );
            }
        }
        
        for(int ix = 0; ix <= NX; ix++){
            for(int iy = 0; iy <= NY; iy++){
                for(int iz = 0; iz <= NZ; iz++){
                    for(int k = 0; k < K; k++){
                        cubes[ix][iy][iz][k].reset();
                    }
                }
            }
        }

    }

}