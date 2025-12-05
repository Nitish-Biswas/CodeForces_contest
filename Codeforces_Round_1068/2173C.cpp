#include "bits/stdc++.h"
#include <numeric>
#define int long long
#define uint unsigned long long
#define vi vector<int>
#define vvi vector<vi >
#define vb vector<bool>
#define vvb vector<vb >
#define fr(i,n) for(int i=0; i<(n); i++)
#define rep(i,a,n) for(int i=(a); i<=(n); i++)
#define nl cout<<"\n"
#define dbg(var) cout<<#var<<"="<<var<<" "
#define all(v) v.begin(),v.end()
#define srt(v) sort(v.begin(),v.end()) // sort
#define mxe(v) *max_element(v.begin(),v.end()) // find max element in vector
#define mne(v) *min_element(v.begin(),v.end()) // find min element in vector
#define unq(v) v.resize(distance(v.begin(), unique(v.begin(), v.end())));
// make sure to sort before applying unique // else only consecutive duplicates would be removed
#define bin(x,y) bitset<y>(x)
using namespace std;
int MOD=1e9+7; // Hardcoded, directly change from here for functions!

const int MX_SZ=1e5+5;
int par[MX_SZ];

#define fastio() ios_base::sync_with_stdio(false);cin.tie(NULL);cout.tie(NULL)
#define MOD 1000000007
#define MOD1 998244353
#define INF 1e18
#define nline "\n"
#define pb push_back
#define ppb pop_back
#define mp make_pair
#define ff first
#define ss second
#define PI 3.141592653589793238462
#define set_bits __builtin_popcountll
#define sz(x) ((int)(x).size())

typedef long long ll;
typedef unsigned long long ull;
typedef long double lld;
// typedef tree<pair<int, int>, null_type, less<pair<int, int>>, rb_tree_tag, tree_order_statistics_node_update > pbds; // find_by_order, order_of_key

#ifdef DEBUG_LOCAL
#define debug(x) do { cerr << #x << " = "; _print(x); cerr << "\n"; fflush(stderr); } while(0)
#else
#define debug(x)
#endif

void _print(ll t) {cerr << t;}
// void _print(int t) {cerr << t;}
void _print(string t) {cerr << t;}
void _print(char t) {cerr << t;}
void _print(lld t) {cerr << t;}
void _print(double t) {cerr << t;}
void _print(ull t) {cerr << t;}

template <class T, class V> void _print(pair <T, V> p);
template <class T> void _print(vector <T> v);
template <class T> void _print(set <T> v);
template <class T, class V> void _print(map <T, V> v);
template <class T> void _print(multiset <T> v);
template <class T, class V> void _print(pair <T, V> p) {cerr << "{"; _print(p.ff); cerr << ","; _print(p.ss); cerr << "}";}
template <class T> void _print(vector <T> v) {cerr << "[ "; for (T i : v) {_print(i); cerr << " ";} cerr << "]";}
template <class T> void _print(set <T> v) {cerr << "[ "; for (T i : v) {_print(i); cerr << " ";} cerr << "]";}
template <class T> void _print(multiset <T> v) {cerr << "[ "; for (T i : v) {_print(i); cerr << " ";} cerr << "]";}
template <class T, class V> void _print(map <T, V> v) {cerr << "[ "; for (auto i : v) {_print(i); cerr << " ";} cerr << "]";}

void modadd(int &a , int b) {a=((a%MOD)+(b%MOD))%MOD;}
void modsub(int &a , int b) {a=((a%MOD)-(b%MOD)+MOD)%MOD;}
void modmul(int &a , int b) {a=((a%MOD)*(b%MOD))%MOD;}
// ================================== take ip/op like vector,pairs directly!==================================
template<typename typC,typename typD> istream &operator>>(istream &cin,pair<typC,typD> &a) { return cin>>a.first>>a.second; }
template<typename typC> istream &operator>>(istream &cin,vector<typC> &a) { for (auto &x:a) cin>>x; return cin; }
template<typename typC,typename typD> ostream &operator<<(ostream &cout,const pair<typC,typD> &a) { return cout<<a.first<<' '<<a.second; }
template<typename typC,typename typD> ostream &operator<<(ostream &cout,const vector<pair<typC,typD>> &a) { for (auto &x:a) cout<<x<<'\n'; return cout; }
template<typename typC> ostream &operator<<(ostream &cout,const vector<typC> &a) { int n=a.size(); if (!n) return cout; cout<<a[0]; for (int i=1; i<n; i++) cout<<' '<<a[i]; return cout; }
// ===================================END Of the input module ==========================================

constexpr int N = 200005; // No. of vertices
constexpr int L = 20; // ceil(logN / log2) + 1

// Vertices from 1 to N.
vector<int> adj[N + 1];
int up[N + 1][L];
int level[N + 1];

void dfs(int u, int prev = 0){
    up[u][0] = prev;
    for (auto &v : adj[u]){
        if (v == prev) continue;

        level[v] = level[u] + 1;
        dfs(v, u);
    }
}

void binaryLift(){
    dfs(1);
    for (int i = 1; i < L; i++)
        for (int j = 1; j <= N; j++)
            up[j][i] = up[up[j][i - 1]][i - 1];
}

int LCA(int a, int b){
    if (level[a] > level[b])
        swap(a, b);

    int diff = level[b] - level[a];
    for (int i = 0; i < L; i++){
        if ((diff & (1 << i)))
            b = up[b][i];
    }

    if (a == b) return a;

    for (int i = L - 1; i >= 0; i--){
        if (up[a][i] != up[b][i]){
            a = up[a][i];
            b = up[b][i];
        }
    }
    return up[a][0];
}

void addEdge(int u, int v){
    adj[u].push_back(v);
    adj[v].push_back(u);
}

int dist(int a, int b){
    return level[a] + level[b] - 2 * level[LCA(a, b)];
}
/// ====================================PRIME utility ==================================================
int sz=1e6+5;
bool PrimeSieve[1000005]; // 1e6+5
void buildSieve(){
    for(int i=2;i<=sz;i++) PrimeSieve[i]=1;
    PrimeSieve[0]=0;//
    PrimeSieve[1]=0; // 1 is neither prime nor composite
    for(int i=2;i<sz;i++){
        if(PrimeSieve[i]==0) continue; // the current number itself is composite
        for(int j=2;j*i<sz;j++){
            PrimeSieve[i*j]=0;
        }
    }
}
// add SieveOfEratosthenes
bool isPrime(int n){
    for(int i=2;i*i<=n;i++){
        if(n%i==0) return 0;
    }
    return 1;
}

/// ====================================PRIME utility ENDS here==================================================

template<class T, class U>
// T -> node, U->update.
struct Lsegtree{
    vector<T>st;
    vector<U>lazy;
    int n;
    T identity_element;
    U identity_update;

    /*
        Definition of identity_element: the element I such that combine(x,I) = x
        for all x

        Definition of identity_update: the element I such that apply(x,I) = x
        for all x
    */

    Lsegtree(int n, T identity_element, U identity_update){
        this->n = n;
        this->identity_element = identity_element;
        this->identity_update = identity_update;
        st.assign(4*n,identity_element);
        lazy.assign(4*n, identity_update);
    }

    T combine(T l, T r){
        // change this function as required.
        T ans = (l + r);
        return ans;
    }

    void buildUtil(int v, int tl, int tr, vector<T>&a){
        if(tl == tr){
            st[v] = a[tl];
            return;
        }
        int tm = (tl + tr)>>1;
        buildUtil(2*v + 1, tl, tm,a);
        buildUtil(2*v + 2,tm+1,tr,a);
        st[v] = combine(st[2*v + 1], st[2*v + 2]);
    }

    // change the following 2 functions, and you're more or less done.
    T apply(T curr, U upd, int tl, int tr){
        T ans = (tr-tl+1)*upd;
        // increment range by upd:
        // T ans = curr + (tr - tl + 1)*upd
        return ans;
    }

    U combineUpdate(U old_upd, U new_upd, int tl, int tr){
        U ans = old_upd;
        ans=new_upd;
        return ans;
    }

    void push_down(int v, int tl, int tr){
        //for the below line to work, make sure the "==" operator is defined for U.
        if(lazy[v] == identity_update)return;
        st[v] = apply(st[v], lazy[v], tl, tr);
        if(2*v + 1 <= 4*n - 1){  // Fixed: was <=4*n, potential overflow
            int tm = (tl + tr)>>1;
            lazy[2*v + 1] = combineUpdate(lazy[2*v+1], lazy[v], tl, tm);
            lazy[2*v + 2] = combineUpdate(lazy[2*v+2], lazy[v], tm+1,tr);
        }
        lazy[v] = identity_update;
    }

    T queryUtil(int v, int tl, int tr, int l, int r){
        push_down(v,tl,tr);
        if(l > r)return identity_element;
        if(tr < l or tl > r){
            return identity_element;
        }
        if(l <= tl and r >= tr){
            return st[v];
        }
        int tm = (tl + tr)>>1;
        return combine(queryUtil(2*v+1,tl,tm,l,r), queryUtil(2*v+2,tm+1,tr,l,r));
    }

    void updateUtil(int v, int tl, int tr, int l, int r, U upd){
        push_down(v,tl,tr);
        if(tr < l or tl > r)return;
        if(tl >=l and tr <=r){
            lazy[v] = combineUpdate(lazy[v],upd,tl,tr);
            push_down(v,tl,tr);
        } else{
            int tm = (tl + tr)>>1;
            updateUtil(2*v+1,tl,tm,l,r,upd);
            updateUtil(2*v+2,tm+1,tr,l,r,upd);
            st[v] = combine(st[2*v + 1], st[2*v+2]);
        }
    }

    void build(vector<T>a){
        assert( (int)a.size() == n);
        buildUtil(0,0,n-1,a);
    }

    T query(int l, int r){
        return queryUtil(0,0,n-1,l,r);
    }

    void update(int l,int r, U upd){
        updateUtil(0,0,n-1,l,r,upd);
    }
};

// ========================================MATH UTIL BEGINS==============================================
//==================================== compute higher powers with mod ===================================
uint power(int x, int y, int p = MOD)
{
    unsigned long long res = 1;

    x = x % p;
    while (y > 0)
    {

        if (y & 1)
            res = (res * x) % p;

        y = y >> 1;
        x = (x * x) % p;
    }
    return res;
}

// =============================================================================================================

uint modInverse(int n, int p=MOD) // using fermats little thm. [p needs to be prime which is mostly the case as mod value generally is 1e9+7]
{
    return power(n, p - 2, p);
}
// can also derive this using extended euclidean... however this has a much simpler code....

// =========================================Used to calculate nCr of higher values ===================================
uint nCr(int n, int r, int p=MOD) // faster calculation..
{
    if (n < r)
        return 0;

    if (r == 0)
        return 1;

    vector<int> fac(n+1,0);
    fac[0] = 1;
    for (int i = 1; i <= n; i++)
        fac[i] = (fac[i - 1] * i) % p;

    return (fac[n] * modInverse(fac[r], p) % p * modInverse(fac[n - r], p) % p) % p;
}
// ==================================== MATH UTIL ENDS=======================================================//

// ==================================== SOLUTION =======================================================//

void solve(){
    int n,k;
    cin>>n>>k;
    vi a(n);
    cin>>a;
    set<long long> look_a(a.begin(), a.end());
    vi set_a(look_a.begin(), look_a.end());
    vector<long long> b;
    
    set<long long> visit;
    
    for(long long num : set_a) {
        if(visit.find(num) == visit.end()) {
            long long curr = num;
            while(curr <= k) {
                if(look_a.find(curr) == look_a.end()) {
                    cout << -1 << endl;
                    return;
                }
                
                visit.insert(curr);
                curr += num;
            }
            b.push_back(num);
        }
    }
    
    cout << b.size() << endl;
    for(size_t i = 0; i < b.size(); ++i) {
        cout << b[i] << (i == b.size() - 1 ? "" : " ");
    }
    cout << endl;
}
    
    
    




#ifdef DEBUG_LOCAL
#include <fstream>

#pragma push_macro("int")
#undef int   // prevent #define int long long from breaking overrides

class InputTeeStreambuf : public std::streambuf {
private:
    std::streambuf* source;
    std::ofstream* logFile;
public:
    InputTeeStreambuf(std::streambuf* source, std::ofstream* logFile)
        : source(source), logFile(logFile) {}
protected:
    virtual int underflow() override { return source->sgetc(); }
    virtual int uflow() override {
        int c = source->sbumpc();
        if (c != EOF && logFile && logFile->is_open()) {
            logFile->put(c);
            logFile->flush();
        }
        return c;
    }
};

#pragma pop_macro("int")  // restore int = long long
#endif



// #region [TEMPLATE] Lazy Segment Tree
int32_t main(){
    #ifdef DEBUG_LOCAL
        string filepath = __FILE__;
        string directory = filepath.substr(0, filepath.find_last_of("/\\"));
        string inputFile = directory + "/input.txt";
        string errorFile = directory + "/Error.txt";
        
        // Save original cin buffer
        static std::streambuf* cinOriginal = cin.rdbuf();
        
        // Create file to save input
        static ofstream inputCopy(inputFile);
        
        // Create tee buffer
        static InputTeeStreambuf teeBuffer(cinOriginal, &inputCopy);
        
        // Replace cin's buffer
        cin.rdbuf(&teeBuffer);
        
        // Redirect stderr
        if (freopen(errorFile.c_str(), "w", stderr) == NULL) {
            perror("freopen error");
        } else {
            cerr << "--- DEBUG SESSION STARTED ---" << "\n\n\n";
        }
    #endif
    
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);

    int T = 1;
    cin >> T;
    while (T--)
    {
        solve();
    }
    return 0;
}
// #endregion




// ================================== TEMPLATE ENDS HERE==========================================