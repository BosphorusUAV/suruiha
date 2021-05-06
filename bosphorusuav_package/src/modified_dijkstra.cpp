#include<bits/stdc++.h>
#include"nearest_distance.h"
#define ii pair<int,int>
#define all(x) (x).begin(),(x).end()
#define sz(x) ((int)(x).size())
using namespace std;

const int64_t INF = 1e17;
const int mod = 1e9+7;

const double X = 350, Y = 350, Z = 200; 
const double EX = 20, EY = 20, EZ = 20;
const int K = 4;
const int NX = X/EX, NY = Y/EY, NZ = Z/EZ;

const double risk_threshold = 30;

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

long double dist(Point a, Point b){
	return sqrt((a.x-b.x)*(a.x-b.x) + (a.y-b.y)*(a.y-b.y) + (a.z-b.z)*(a.z-b.z));
}

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
	long double val=INF;
      bool visited = false;

	Cube(Point _point=Point(), double _val=INF, int _k=0):point(_point), val(_val), k(_k){}
	bool operator>(const Cube& A)const{
		return val < A.val;
	}
      bool operator<(const Cube& A)const{
		return val > A.val;
	}

      void debug(){
            cerr <<"("<< point.x << ", " << point.y << ") [" << ix << "][" << iy << "][" << iz << "][" << k << "] " << val << "\n";
      }
} cubes[NX+3][NY+3][NZ+3][K+1];

Cube* inside(Point A, int k = 0){
      int ix = A.x / EX;
      int iy = A.y / EY;
      int iz = A.z / EZ;
      return &cubes[ix][iy][iz][k];
}
double risk_func(double dist){
      // cerr << dist << "\n";
      if(dist <= risk_threshold) return 1;
      else return 0;
}
bool risk(Point& A, Point& B){
      double ret = 0;
      for(auto r : risk_points){
            if(risk_func(nearestDistance(A, B, r))) return true;
      }
      return false;
}

vector<Point> find_path(Cube* s, Cube* e){

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
                  if(!risk(adj->point, from->point)){
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
            // cerr << "path ";
            // curr->debug();
            ret.push_back(curr->point);
            if(!curr->k) break;
            curr = curr->from;

            if(!--cnt)cerr << "PATH YOK!\n";
            return vector<Point>();
      }
      ret.push_back(s->point);
      return ret;
}


int main(int f, char** files){
      ios_base::sync_with_stdio(false);
      cin.tie(NULL);
      
      if(f > 1){
            const char* input_file = files[1];
            cerr << "input file: " << input_file << endl;
            freopen(input_file, "r", stdin);
      }
      if(f > 2){
            const char* output_file = files[2];
            cerr << "output file: " << output_file << endl;
            freopen(output_file, "w", stdout);
      }
      cerr << NX*NY*NZ*K << " units\n";

	double sx, sy, sz, ex, ey, ez;
      cin >> sx >> sy >> sz >> ex >> ey >> ez;

      int r;
      cin >> r;
      for(int i = 0; i < r; i++){
            double x, y, z;
            cin >> x >> y >> z;
            risk_points.push_back(Point(x, y, z));
      }

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
      
      Cube* s = inside(Point(sx, sy, sz), 0);
      Cube* e = inside(Point(ex, ey, ez), K-1);

      vector<vector<Point>> T;
      for(int i = 0; i < 10; i++){
            T.push_back(find_path(s, e));
            for(int ix = 0; ix <= NX; ix++){
                  for(int iy = 0; iy <= NY; iy++){
                        for(int iz = 0; iz <= NZ; iz++){
                              for(int k = 0; k < K; k++){
                                    Cube* cube = &cubes[ix][iy][iz][k];
                                    cube->val = INF;
                                    cube->from = cube;
                                    cube->visited = false;
                              }
                        }
                  }
            }
      }
      auto P = find_path(s, e);

      for(auto p : P){
            p.print();
            cout << "\n";
      }
}