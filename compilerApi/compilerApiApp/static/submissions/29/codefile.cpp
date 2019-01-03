 #include<bits/stdc++.h>
using namespace std;
#define PB(x) push_back(x)
#define MP(x,y) make_pair(x,y)
#define ll  long long int 
#define F first
#define S second
#define boost ios_base::sync_with_stdio(false),cin.tie(NULL);
const ll MOD = 1000000007;
//#include <ext/pb_ds/assoc_container.hpp> // Common file 
//#include <ext/pb_ds/tree_policy.hpp>  
//using namespace __gnu_pbds; 
//stringstream ss; string temp; ss<<str(original string) ss>>temp;

int main()
{	
	ll t; cin>>t;
	while(t--)
	{
		ll n;cin>>n;
		ll a[n];
		for(ll i=0;i<n;i++)
		{
			cin>>a[i];
		}
		for(ll i=0;i<n;i++)
		{
			for(ll j=0;j<10;j++)
			{
				cout<<a[i]+a[j]<<endl;
			}
		}
	}
}