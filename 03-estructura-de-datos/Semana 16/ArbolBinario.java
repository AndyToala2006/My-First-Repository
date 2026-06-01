class Nodo {
    int valor;
    Nodo izquierda, derecha;

    Nodo(int item){
        valor = item;
        izquierda = derecha = null;
    }
}

public class ArbolBinario {
    Nodo raiz;

    void preOrden(Nodo nodo){
        if(nodo != null){
            System.out.print(nodo.valor + " ");
            preOrden(nodo.izquierda);
            preOrden(nodo.derecha);
        }
    }

    public static void main(String[] args){
        ArbolBinario arbol = new ArbolBinario();
        arbol.raiz = new Nodo(50);
        arbol.raiz.izquierda = new Nodo(30);
        arbol.raiz.derecha = new Nodo(70);
        arbol.raiz.izquierda.izquierda = new Nodo(20);
        arbol.raiz.izquierda.derecha = new Nodo(40);
        arbol.raiz.derecha.izquierda = new Nodo(60);
        arbol.raiz.derecha.derecha = new Nodo(80);

        System.out.print("Recorrido preorden: ");
        arbol.preOrden(arbol.raiz);
    }
}
