#include<bits/stdc++.h>
using namespace std;

const int64_t inf = 1e17;

struct Point{
	double x, y, z;
	Point(double _x, double _y, double _z): x(_x), y(_y), z(_z){}
	void print(){
		cout  << x << " " << y << " " << z << " ";
	}
};
double dist(Point a, Point b){
	return sqrt((a.x-b.x)*(a.x-b.x) + (a.y-b.y)*(a.y-b.y) + (a.z-b.z)*(a.z-b.z));
}

pair<double, int> dp[21][1<<20];

double totaldist = 0;

vector<int> bitmaskDP(vector<Point>& formation_points, vector<Point>& uav_points){     
	// fonksiyon girdi olarak formasyonda yerleşilecek noktaları ve ihaların bulunduğu noktayı alır. 
	// i. ihanın kaçıncı formasyon noktasına yerleştirileceğini dizi olarak döndürür.
	
	int M = formation_points.size();
	int N = uav_points.size();

	int optimum_mask = (1<<M)-1;


	for(int i = 0; i <= N; i++){
		for(int j = 0; j < (1<<M); j++)
			dp[i][j] = {inf, -1};
	}
	dp[0][0].first = 0;

	for(int i = 1; i <= N; i++){
		for(int mask = 0; mask < (1 << M); mask++){
			for(int j = 0; j < M; j++){
				if(mask & (1 << j)){
					dp[i][mask] = min(
						dp[i][mask], 
						{
							dp[i-1][mask ^ (1 << j)].first + dist(uav_points[i-1], formation_points[j]), 
							j
						}
						);
				}
			}
			if(i == N && dp[i][mask] < dp[i][optimum_mask]) optimum_mask = mask;
		}
	}
		
	vector<int> placements(N, -1);

	totaldist = dp[N][optimum_mask].first;


	for(int i = N; i >= 1; i--){
		placements[i-1] = dp[i][optimum_mask].second;
		optimum_mask ^= (1 << dp[i][optimum_mask].second);
	}

	return placements;
}


int32_t main(){
	ios_base::sync_with_stdio(false);
	cin.tie(NULL);
	
	freopen("points.in", "r", stdin);
	freopen("points.out", "w", stdout);
	
	int N, M;
	cin >> N >> M;

	vector<Point> A, B;
	for(int i = 0; i < N; i++){
		double x, y, z;
		cin >> x >> y >> z;
		B.push_back(Point(x, y, z));
	}
	for(int i = 0; i < M; i++){
		double x, y, z;
		cin >> x >> y >> z;
		A.push_back(Point(x, y, z));
	}
	vector<int> placements = bitmaskDP(A, B);

	cout << totaldist << endl;
	for(int i = 0; i < N; i++){
		cout << placements[i] << " ";
	}
}