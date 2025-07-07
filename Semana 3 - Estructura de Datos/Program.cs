using System;
using System.Drawing;

class Program
{
    private static void Main(string[] args)
    {
        // Crear objeto Circulo con radio 5
        Circulo miCirculo = new Circulo(5);
        Console.WriteLine("Área del Círculo: " + miCirculo.CalcularArea());
        Console.WriteLine("Perímetro del Círculo: " + miCirculo.CalcularPerimetro());

        // Crear objeto Rectángulo con base 4 y altura 3
        Rectangle miRectangulo = new Rectangle(4, 3);
        Console.WriteLine("Área del Rectángulo: " + miRectangulo.CalcularArea());
        Console.WriteLine("Perímetro del Rectángulo: " + miRectangulo.CalcularPerimetro());
    }
}
