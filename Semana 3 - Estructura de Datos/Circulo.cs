using System;

public class Circulo
{
    private double radio;

    public Circulo(double radio)
    {
        this.radio = radio;
    }

    // Método para calcular el área del círculo
    public double CalcularArea()
    {
        return Math.PI * radio * radio;
    }

    // Método para calcular el perímetro del círculo
    public double CalcularPerimetro()
    {
        return 2 * Math.PI * radio;
    }
}