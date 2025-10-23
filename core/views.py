from django.shortcuts import render

def inicio(request):
    """
    Vista principal del sistema municipal de gas.
    Muestra el menú de navegación con enlaces a las funcionalidades.
    """
    return render(request, 'core/inicio.html')
