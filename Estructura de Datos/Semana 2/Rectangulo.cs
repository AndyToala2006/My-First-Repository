using System;

class Program
{
    static void Main(string[] args)
    {
        // Crear objeto Circulo con radio 5
        Circulo miCirculo = new Circulo(5);
        Console.WriteLine("Área del Círculo: " + miCirculo.CalcularArea());
        Console.WriteLine("Perímetro del Círculo: " + miCirculo.CalcularPerimetro());

        // Crear objeto Rectángulo con base 4 y altura 3
        Rectangulo miRectangulo = new Rectangulo(4, 3);
        Console.WriteLine("Área del Rectángulo: " + miRectangulo.CalcularArea());
        Console.WriteLine("Perímetro del Rectángulo: " + miRectangulo.CalcularPerimetro());
    }
}
