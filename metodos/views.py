from django.shortcuts import render
from sympy import symbols, sympify, diff, lambdify
import matplotlib.pyplot as plt
import numpy as np

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
            
            x_vals = np.linspace(-10, 10, 400)

            funcion_numpy = lambdify(x, f, "numpy")

            y_vals = funcion_numpy(x_vals)

            plt.figure(figsize=(8,5))

            plt.axhline(0)
            plt.axvline(0)

            plt.plot(x_vals, y_vals)

            plt.title("Método Newton-Raphson")

            plt.xlabel("x")
            plt.ylabel("f(x)")

            plt.grid(True)

            plt.savefig('metodos/static/grafica.png')

            plt.close()

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


def secante(request):

    datos = {}

    if request.method == 'POST':

        funcion = request.POST['funcion']
        x0 = float(request.POST['x0'])
        x1 = float(request.POST['x1'])
        tolerancia = float(request.POST['tolerancia'])
        max_iter = int(request.POST['iteraciones'])

        x = symbols('x')
        f = sympify(funcion)

        iteraciones = []
        raiz = None
        estado = 'No convergió'

        for i in range(max_iter):
            fx0 = float(f.subs({x: x0}))
            fx1 = float(f.subs({x: x1}))

            if abs(fx1 - fx0) < 1e-12:
                estado = 'División por cero'
                break

            x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
            fx2 = float(f.subs({x: x2}))
            error = abs(x2 - x1)

            iteraciones.append({
                'n': i + 1,
                'x0': round(x0, 6),
                'x1': round(x1, 6),
                'x2': round(x2, 6),
                'fx2': round(fx2, 6),
                'error': round(error, 6),
            })

            if error < tolerancia:
                raiz = round(x2, 6)
                estado = 'Convergió ✅'
                break

            x0, x1 = x1, x2

        import numpy as np
        from sympy import lambdify

        centro = raiz if raiz else (float(request.POST['x0']))
        x_vals = [round(centro - 5 + i * 0.1, 2) for i in range(101)]
        f_lambda = lambdify(x, f, 'numpy')
        y_vals = []
        for val in x_vals:
            try:
                y = float(f_lambda(val))
                y_vals.append(round(y, 4) if abs(y) < 1000 else None)
            except:
                y_vals.append(None)

        datos = {
            'funcion': funcion,
            'x0': request.POST['x0'],
            'x1': request.POST['x1'],
            'tolerancia': request.POST['tolerancia'],
            'iteraciones_param': request.POST['iteraciones'],
            'tabla': iteraciones,
            'raiz': raiz,
            'estado': estado,
            'x_vals': x_vals,
            'y_vals': y_vals,
        }

    return render(request, 'secante.html', datos)