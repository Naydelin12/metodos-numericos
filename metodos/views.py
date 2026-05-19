from django.shortcuts import render

from sympy import symbols
from sympy import sympify
from sympy import diff

def inicio(request):
    return render(request, 'inicio.html')

def newton(request):

    datos = {}

    if request.method == 'POST':

        funcion = request.POST['funcion']
        x0 = request.POST['x0']
        tolerancia = request.POST['tolerancia']
        iteraciones = request.POST['iteraciones']

        x = symbols('x')

        f = sympify(funcion)
        derivada = diff(f, x)

        resultado = round(float(f.subs({x: float(x0)})), 4)
        resultado_derivada = round(float(derivada.subs({x: float(x0)})), 4)

        nuevo_x = round(
        float(x0) - (resultado / resultado_derivada),
        4
        )

        datos = {
    'funcion': funcion,
    'x0': x0,
    'tolerancia': tolerancia,
    'iteraciones': iteraciones,
    'resultado': resultado,
    'derivada': derivada,
    'nuevo_x': nuevo_x
}

    return render(request, 'newton.html', datos)