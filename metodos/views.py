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

        tabla = []

        x = symbols('x')

        f = sympify(funcion)

        derivada = diff(f, x)

        resultado = round(float(f.subs({x: float(x0)})), 4)

        resultado_derivada = round(
            float(derivada.subs({x: float(x0)})),
            4
        )

        nuevo_x = round(
            float(x0) - (resultado / resultado_derivada),
            4
        )

        error = round(abs(nuevo_x - float(x0)), 4)

        tabla.append([
            1,
            nuevo_x,
            resultado,
            resultado_derivada,
            error,
            'Se evaluó la función y se aplicó Newton-Raphson'
        ])

        contador = 1

        while error > float(tolerancia) and contador < int(iteraciones):

            x0 = nuevo_x

            resultado = round(
                float(f.subs({x: float(x0)})),
                4
            )

            resultado_derivada = round(
                float(derivada.subs({x: float(x0)})),
                4
            )

            nuevo_x = round(
                float(x0) - (resultado / resultado_derivada),
                4
            )

            error = round(abs(nuevo_x - float(x0)), 4)

            contador += 1

            tabla.append([
                contador,
                nuevo_x,
                resultado,
                resultado_derivada,
                error,
                'Nueva aproximación calculada'
            ])
            

        datos = {
            'funcion': funcion,
            'x0': x0,
            'tolerancia': tolerancia,
            'iteraciones': iteraciones,
            'resultado': resultado,
            'derivada': derivada,
            'nuevo_x': nuevo_x,
            'tabla': tabla,
            'raiz': nuevo_x,
            'mensaje': 'El método convergió correctamente'
        }

    return render(request, 'newton.html', datos)