import random
import string
import csv


matriculas_generadas = set()

def obtener_nombres_empresas():
    nombres_empresas = []
    with open('companies.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            nombres_empresas.append(row[1])  # La segunda columna contiene los nombres de las empresas
    return nombres_empresas

def generar_matricula():
    letras = ''.join(random.choices(string.ascii_uppercase, k=3))
    numeros = ''.join(random.choices(string.digits, k=4))
    return f"{letras}{numeros}"

def generar_datos_fichero(num_camiones):
    nombres_empresas = obtener_nombres_empresas()
    with open('0000.dat', 'w') as data:
        for i in range(num_camiones):
            id_camion = i + 1
            matricula = generar_matricula()
            while matricula in matriculas_generadas:
                matricula = generar_matricula()
            matriculas_generadas.add(matricula)
            kilometros = random.randint(0, 500000)
            nombre_empresa = random.choice(nombres_empresas)
            data.write(f"{id_camion};{matricula};{nombre_empresa};{kilometros}\n")
            #data.write(f"{nombre_empresa} \n")

#generar_datos_fichero(10)
generar_datos_fichero(20000000)

