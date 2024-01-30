#include <iostream>
using namespace std;

class MiClase {
public:
    string mark;
    int variablePublica;
    MiClase() {
        mark = "hombre";
        variablePublica = 0;
    }
private:
    ~MiClase();

    void descripcion(string nuevo) {
        mark = nuevo;
    }

    void setVariable(int valor, int a) {
        variablePublica = valor;
    }

    int getVariable() {
        return variablePublica;
    }
};

void markWill(int x, int y){
    int mark;
    int will = 0;
    int ARRAY[5]={0,1,2,3,4};
    if(4<5){
        int z= 5;
    }
    while(mark == will){
        if(mark){
            will=true;
        }else{int a = 5;}
    }

}

int main(){
    int a=0;
    if(a==0){int a=0;}
    while(a>5){
        if(a==0){int a=0;}
        cout<<"prueva";
    }   
    for(int i=0; i<5; i++){
        cout<<"escribir algo";
    }
    
    func(1,2,3);
    return 0;
}

int func(int a, int b, int c){
    int resul=0;
    resul = a+b+c;
    cout<<resul;
}