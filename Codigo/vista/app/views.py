from __future__ import unicode_literals

from django.shortcuts import render

from .forms import FormularioReconocimiento
from .models import Integrante

from controlador.configuracion import *
from controlador.api_autocaras import *
api = APIAutocaras()

from modelo.utilitarios.conversor import Conversor

"""
***********************************************************************
Vista para cargar la seccion de reconocimiento del sistema
***********************************************************************
"""
def reconocimiento(request):

    form = FormularioReconocimiento(request.POST or None, request.FILES or None)
    if form.is_valid():
        imagen = form.save(commit=False)
        imagen.file = request.FILES['file']
        imagen.save()
        print(imagen.file.url)

        ruta_img = imagen.file.url
        ruta_img = os.path.split(ruta_img)[1]
        ruta_img = os.path.join(Configuracion.RUTA_MEDIA, ruta_img)

        # Ejecucion del reconocimiento de rostros
        contexto = api.ejecutar_clasificacion(ruta_img)

        #Creacion de la imagen PNG en el directorio media
        Conversor.guardar_imagen(str(ruta_img))

        # Conversion de la imagen buscada a formato .PNG
        ruta_img = Conversor.convertir_pgm_a_png(str(imagen.file.url))

        # Se agrega la llave ruta_img que contiene la imagen que se muestra en el resultado
        contexto['ruta_img'] = ruta_img

        # Llamado al template de resultados, pasando como contexto la respuesta del reconocimiento
        return render(request, 'app/reconocimientoRes.html', contexto)

    context = {
        'form': form,
    }
    return render(request, 'app/reconocimiento.html', context)





"""
***********************************************************************
Vista para cargar los datos del entrenamiento
***********************************************************************
"""


def entrenamiento(request):
    if(request.method == 'POST'):
        porcentaje_coleccion = int(request.POST.get('porcentaje_coleccion',""))
        porcentaje_valores = int(request.POST.get('porcentaje_valores',""))
        porcentaje_aceptacion = int(request.POST.get('porcentaje_aceptacion',""))
        print("Valores de Entrenamiento Solicitados: ")
        print('Porcentaje de Coleccion '+ str(porcentaje_coleccion))
        print('Porcentaje de Valores '+ str(porcentaje_valores))
        print('Porcentaje de Aceptacion '+str(porcentaje_aceptacion))

        # Ejecucion del entrenamiento del sistema
        contexto = api.ejecutar_entrenamiento(porcentaje_coleccion, porcentaje_valores, porcentaje_aceptacion)
        contexto['porcentaje_coleccion'] = str(porcentaje_coleccion)
        contexto['porcentaje_valores'] = str(porcentaje_valores)
        contexto['porcentaje_aceptacion'] = str(porcentaje_aceptacion)
        # Llamado al template de resultados, pasando como contexto la respuesta del entrenamiento
        return render(request, 'app/entrenamientoRes.html',contexto)

    return render(request, 'app/entrenamiento.html', {})






"""
***********************************************************************
Vista para controlar la seccion AcercaDe que contiene
los datos del Codigo y los integrantes
***********************************************************************
"""


def acercaDe(request):
    integrantes = Integrante.objects.all()
    context = {'integrantes': integrantes}
    return render(request, 'app/acercaDe.html', context)
