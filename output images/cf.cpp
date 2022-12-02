#include<bits/stdc++.h>
using namespace std;
int main(){
    int t;
    cin>>t;
    while(t--){
        int a,b;
        string s="";
        string x="01";
        strinf z="0";
        string o="1";
        s.clear();
        cin>>a>>b;
        //a 0s and b 1s
        if(a>b){
            int p=b;
            while(p--)
            strcat(s,x);
            int m=a-b;
            while(m--)
            strcat(s,z);
        }
        else{
            int p=a;
            while(p--)
            strcat(s,x);
            int m=b-a;
            while(m--)
            strcat(s,o);
        }
        cout<<s<<'\n';
    }
    return
}