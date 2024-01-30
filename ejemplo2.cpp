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

void arreglo(int x, float y){
    int ARRAY[5]={5,1,4,7,41};
    if(x<y){
        for(int i=0; i<5; i++){
            cout<<ARRAY[i];
        }
    }

}

int main(){
    cout<<"Traductor de codigo:\n";
    int a=0;
    string cad = "*";
    while(a<5){
        cout<<cad;
        cad+="*";
        a++;
    }   
    cout<<"==========================================";
    for(int i=0; i<2; i++){
        cout<<i;
    }
    cout<<"prueva";
    for(int i=0; i<5; i++){
        cout<<"escribir algo";
    }
    cout<<"==========================================";
    int m=2;
    int n=3;
    arreglo(m,n);
    cout<<"==========================================";
    suma(1,2,3);
    return 0;
}

int suma(int a, int b, int c){
    int resul=0;
    resul = a+b+c;
    cout<<"==========================================";
    cout<<"resultado: "+resul;
}