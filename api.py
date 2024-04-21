
import csv
from flask import Flask, jsonify, request

# Definición de la clase Nodo para el árbol AVL
class NodoAVL:
    def __init__(self, id):
        self.id = id
        self.izquierda = None
        self.derecha = None
        self.altura = 1


class ArbolAVL:
    def __init__(self):
        self.raiz = None
        
    def obtener_altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura

  
    def obtener_factor_equilibrio(self, nodo):
        if not nodo:
            return 0
        return self.obtener_altura(nodo.izquierda) - self.obtener_altura(nodo.derecha)

   
    def rotar_derecha(self, nodo_z):
        nodo_y = nodo_z.izquierda
        nodo_t3 = nodo_y.derecha

        nodo_y.derecha = nodo_z
        nodo_z.izquierda = nodo_t3

        nodo_z.altura = 1 + max(self.obtener_altura(nodo_z.izquierda), self.obtener_altura(nodo_z.derecha))
        nodo_y.altura = 1 + max(self.obtener_altura(nodo_y.izquierda), self.obtener_altura(nodo_y.derecha))

        return nodo_y

    
    def rotar_izquierda(self, nodo_y):
        nodo_z = nodo_y.derecha
        nodo_t2 = nodo_z.izquierda

        nodo_z.izquierda = nodo_y
        nodo_y.derecha = nodo_t2

        nodo_y.altura = 1 + max(self.obtener_altura(nodo_y.izquierda), self.obtener_altura(nodo_y.derecha))
        nodo_z.altura = 1 + max(self.obtener_altura(nodo_z.izquierda), self.obtener_altura(nodo_z.derecha))

        return nodo_z

    
    def insertar(self, raiz, id):
        if not raiz:
            return NodoAVL(id)
        elif id < raiz.id:
            raiz.izquierda = self.insertar(raiz.izquierda, id)
        else:
            raiz.derecha = self.insertar(raiz.derecha, id)

        raiz.altura = 1 + max(self.obtener_altura(raiz.izquierda), self.obtener_altura(raiz.derecha))

        factor_equilibrio = self.obtener_factor_equilibrio(raiz)

        if factor_equilibrio > 1:
            if id < raiz.izquierda.id:
                return self.rotar_derecha(raiz)
            else:
                raiz.izquierda = self.rotar_izquierda(raiz.izquierda)
                return self.rotar_derecha(raiz)
        elif factor_equilibrio < -1:
            if id > raiz.derecha.id:
                return self.rotar_izquierda(raiz)
            else:
                raiz.derecha = self.rotar_derecha(raiz.derecha)
                return self.rotar_izquierda(raiz)

        return raiz


class API:
    def __init__(self):
        self.app = Flask(__name__)
        self.arbol = ArbolAVL()

        @self.app.route('/cargar_csv', methods=['GET'])
        def cargar_csv():
            ruta_csv = 'C:/Users/leona/OneDrive/Documentos/ProgrmacionIII/estudiante.csv'
            with open(ruta_csv, newline='', encoding='utf-8') as archivo_csv:
                lector_csv = csv.reader(archivo_csv)
                next(lector_csv)
                for linea in lector_csv:
                    id = linea[0]
                    self.arbol.raiz = self.arbol.insertar(self.arbol.raiz, id)
            return jsonify({'message': 'Carga masiva exitosa'})

        @self.app.route('/agregar_registro', methods=['POST'])
        def agregar_registro():
            datos = request.json
            id = datos['id']
            self.arbol.raiz = self.arbol.insertar(self.arbol.raiz, id)
            return 'Registro agregado exitosamente'

        @self.app.route('/buscar_registro/<id>', methods=['GET'])
        def buscar_registro(id):
            
            return jsonify({'message': f'Registro encontrado con ID {id}'})

        @self.app.route('/informacion_grupo', methods=['GET'])
        def informacion_grupo():
            informacion = {
                'integrantes': [
                    {'nombre': 'Nombre1', 'carnet': '0000001', 'contribuciones': 'Desarrollo de la API'},
                    {'nombre': 'Nombre2', 'carnet': '0000002', 'contribuciones': 'Pruebas y depuración'},
                    {'nombre': 'Nombre3', 'carnet': '0000003', 'contribuciones': 'Documentación y diseño'}
                ]
            }
            return jsonify(informacion)

    def run(self):
        self.app.run(debug=True, host='0.0.0.0', port=8080)

if __name__ == '__main__':
    api = API()
    api.run()
