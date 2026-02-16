import java.util.*;

public class Grafo {
    public static void main(String[] args) {
        Map<String, List<String>> grafo = new HashMap<>();
        grafo.put("A", Arrays.asList("B","C"));
        grafo.put("B", Arrays.asList("A","D"));
        grafo.put("C", Arrays.asList("A","D"));
        grafo.put("D", Arrays.asList("B","C","E"));
        grafo.put("E", Arrays.asList("D"));

        for(String nodo : grafo.keySet()){
            System.out.println("Nodo " + nodo + ": " + grafo.get(nodo));
        }
    }
}