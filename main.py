from flask import Flask, Flask,request
from flask.json import jsonify
from flask_cors import CORS
import xml.etree.ElementTree as ET
from usuarios import Usuario
from xml.dom.minidom import *
from tkinter import filedialog
from tkinter import Tk
from colorama import Fore, Back, Style
import json
import datetime
import re


from recurso import Recursos
from usuarios import Usuario
from instancia import Instancias
from clases import *



app=Flask(__name__)
app.config["DEBUG"]=True
CORS(app)


@app.route('/')
def home():
    return "Los alumnos de IPC2 B van a ganar"

@app.route('/autor')
def autor():
    return "Dwight Fenando Gabriel Chinchilla Hernandez - 202106208"


@app.route('/cargarArchivo',methods=['POST'])
def readXML():
    ruta=request.data.decode('utf-8')
    
    global lista_recursos, lista_categorias, lista_clientes, lista_consumos
    lista_recursos = []
    lista_categorias = []
    lista_clientes = []
    domTree = parseString(ruta)
    rootNode = domTree.documentElement
    #print(rootNode.nodeName)

    lrecursos= rootNode.getElementsByTagName("listaRecursos")
    print("\n Lista Recursos")
    for lrecursor in lrecursos:

        recursos= lrecursor.getElementsByTagName("recurso")
        for recurso in recursos:
            if recurso.hasAttribute("id") and recurso.getElementsByTagName("metrica")!=None:
                print("ID:",recurso.getAttribute("id"))
                # elemento de nombre
                nombre = recurso.getElementsByTagName("nombre")[0]
                print(nombre.nodeName, ":", nombre.childNodes[0].data)
                # elemento telefónico
                abreviatura = recurso.getElementsByTagName("abreviatura")[0]
                print(abreviatura.nodeName, ":", abreviatura.childNodes[0].data)

                metrica = recurso.getElementsByTagName("metrica")[0]
                print(metrica.nodeName, ":", metrica.childNodes[0].data)

                tipo = recurso.getElementsByTagName("tipo")[0]
                print(tipo.nodeName, ":", tipo.childNodes[0].data)
                
                valorXhora = recurso.getElementsByTagName("valorXhora")[0]
                print(valorXhora.nodeName, ":", valorXhora.childNodes[0].data)
                valorH=valorXhora.childNodes[0].data.replace(" ", "")
                
                lista_recursos.append(Recursos(recurso.getAttribute("id"), nombre.childNodes[0].data, abreviatura.childNodes[0].data,  metrica.childNodes[0].data, tipo.childNodes[0].data,valorH))


    print("\n Lista Categorias")
    categorias= rootNode.getElementsByTagName("categoria")
    for categoria in categorias:
        if categoria.hasAttribute("id"):
            print("ID:",categoria.getAttribute("id"))
            # elemento de nombre
            nombreC = categoria.getElementsByTagName("nombre")[0]
            print(nombreC.nodeName, ":", nombreC.childNodes[0].data)
            # elemento telefónico
            descripcion = categoria.getElementsByTagName("descripcion")[0]
            print(descripcion.nodeName, ":", descripcion.childNodes[0].data)

            cargaTrabajo = categoria.getElementsByTagName("cargaTrabajo")[0]
            print(cargaTrabajo.nodeName, ":", cargaTrabajo.childNodes[0].data)

            Objeto_Categoria=Categoria(recurso.getAttribute("id"), nombreC.childNodes[0].data, descripcion.childNodes[0].data, cargaTrabajo.childNodes[0].data)
            lista_categorias.append(Objeto_Categoria)

            configuraciones= categoria.getElementsByTagName("configuracion")
            
            #print("\nLista de Puntos")
            for configuracion in configuraciones:
                if configuracion.hasAttribute("id"):
                    print("ID:", configuracion.getAttribute("id"))

                    nombreConfi = configuracion.getElementsByTagName("nombre")[0]
                    print(nombreConfi.nodeName, ":", nombreConfi.childNodes[0].data)

                    descripcionConfi = configuracion.getElementsByTagName("descripcion")[0]
                    print(descripcionConfi.nodeName, ":", descripcionConfi.childNodes[0].data)

                    Objeto_Configuracion = Configuracion(configuracion.getAttribute("id"),nombreConfi.childNodes[0].data,descripcionConfi.childNodes[0].data)

                    Objeto_Categoria.lista_configuraciones.append(Objeto_Configuracion)



                    #print("DATOS DE SUCURSAL CARGADOS CORRECTAMENTE")
                    recursos= configuracion.getElementsByTagName("recurso")
                    #print("\nLista de Escritorios")
                    for recurso in recursos:
                        
                        if recurso.hasAttribute("id"):
                            print("ID:", recurso.getAttribute("id"))

                            cantidad = recurso.childNodes[0].data
                            print(recurso.nodeName, ":", recurso.childNodes[0].data)

                            Objeto_Configuracion.lista_recursos.append(RecursosC(recurso.getAttribute("id"),recurso.childNodes[0].data))


    clientes= rootNode.getElementsByTagName("cliente")
    for cliente in clientes:
        if cliente.hasAttribute("nit"):
            print("NIT:",cliente.getAttribute("nit"))
            # elemento de nombre
            nombreCliente = cliente.getElementsByTagName("nombre")[0]
            print(nombreCliente.nodeName, ":", nombreCliente.childNodes[0].data)

            usuario = cliente.getElementsByTagName("usuario")[0]
            print(usuario.nodeName, ":", usuario.childNodes[0].data)

            clave = cliente.getElementsByTagName("clave")[0]
            print(clave.nodeName, ":", clave.childNodes[0].data)

            direccion = cliente.getElementsByTagName("direccion")[0]
            print(direccion.nodeName, ":", direccion.childNodes[0].data)  

            correo = cliente.getElementsByTagName("correoElectronico")[0]
            print(correo.nodeName, ":", correo.childNodes[0].data) 

            Objeto_Cliente=Usuario(cliente.getAttribute("nit"), nombreCliente.childNodes[0].data, usuario.childNodes[0].data, clave.childNodes[0].data, direccion.childNodes[0].data, correo.childNodes[0].data)
            lista_clientes.append(Objeto_Cliente)

            instancias= cliente.getElementsByTagName("instancia") 

            for instancia in instancias:
                if instancia.hasAttribute("id"):
                    print("ID:", instancia.getAttribute("id"))

                    idConfi = instancia.getElementsByTagName("idConfiguracion")[0]
                    print(idConfi.nodeName, ":", idConfi.childNodes[0].data)

                    nombreInstancia = instancia.getElementsByTagName("nombre")[0]
                    print(nombreInstancia.nodeName, ":", nombreInstancia.childNodes[0].data)

                    fechaInicio = instancia.getElementsByTagName("fechaInicio")[0]
                    prog = re.compile(r'(\d{2})/(\d{2})/(\d{4})')
                    result = prog.search(str(fechaInicio.childNodes[0].data))
                    if result!=None:
                        FechaINICIO=result.group()
                        print(fechaInicio.nodeName, ":", result.group())
                    else:
                        print(fechaFinal.nodeName, ":", fechaInicio.childNodes[0].data, "NADA")
                        FechaINICIO=None 
                    

                    estado = instancia.getElementsByTagName("estado")[0]
                    print(estado.nodeName, ":", estado.childNodes[0].data)

                    fechaFinal = instancia.getElementsByTagName("fechaFinal")[0]
                    prog2 = re.compile(r'(\d{2})/(\d{2})/(\d{4})')
                    fechaFinal_Re = prog2.search(str(fechaFinal.childNodes[0].data))
                    if fechaFinal_Re!=None:
                        FechaFINAL=fechaFinal_Re.group()
                        print(fechaFinal.nodeName, ":", fechaFinal_Re.group())
                    else:
                        print(fechaFinal.nodeName, ":", fechaFinal.childNodes[0].data, "NADA")
                        FechaFINAL=None 

                    Objeto_Cliente.lista_instancias.append(Instancias(instancia.getAttribute("id"),idConfi.childNodes[0].data, nombreInstancia.childNodes[0].data, FechaINICIO, estado.childNodes[0].data, FechaFINAL))
                            
    return jsonify({'ok':True,'data':'Datos cargados con exito'}),200                      



@app.route('/cargarArchivoConsumos',methods=['POST'])
def readXML2():
    ruta=request.data.decode('utf-8')
    
    global lista_recursos, lista_categorias, lista_clientes, lista_consumos
    lista_consumos = []
    domTree = parseString(ruta)
    rootNode = domTree.documentElement
    #print(rootNode.nodeName)

    consumos= rootNode.getElementsByTagName("consumo")
    for recurso in consumos:
        if recurso.hasAttribute("nitCliente") and recurso.hasAttribute("idInstancia"):
            print("Nit:",recurso.getAttribute("nitCliente"))
            print("Id Instancia:",recurso.getAttribute("idInstancia"))
            # elemento de nombre
            tiempo = recurso.getElementsByTagName("tiempo")[0]
            print(tiempo.nodeName, ":", tiempo.childNodes[0].data)
            # elemento telefónico

            fechaHora = recurso.getElementsByTagName("fechaHora")[0]
            prog = re.compile(r'(\d{2})/(\d{2})/(\d{4})')
            result = prog.search(str(fechaHora.childNodes[0].data))
            if result!=None:
                FechaHORA=result.group()
                print(fechaHora.nodeName, ":", result.group())
            else:
                print(fechaHora.nodeName, ":", fechaHora.childNodes[0].data, "NADA")
                FechaHORA=None 

            lista_consumos.append(Consumos(recurso.getAttribute("nitCliente"),recurso.getAttribute("idInstancia"), tiempo.childNodes[0].data, FechaHORA))    


    return jsonify({'ok':True,'data':'Datos cargados con exito'}),200 



@app.route('/recursos',methods=['GET'])
def obtener_recursos():
    global lista_recursos, lista_categorias, lista_clientes
    json=[]
    for i in lista_recursos:
        recurso={
            'id':i.id,
            'nombre':i.nombre,
            'abreviatura':i.abreviatura,
            'metrica':i.metrica,
            'tipo':i.tipo,
            'valor_hora ':i.valor_hora 
        }
        json.append(recurso)

    return jsonify(json),200

@app.route('/categorias',methods=['GET'])
def obtener_categorias():
    global lista_recursos, lista_categorias, lista_clientes
    json=[]
    for i in lista_categorias:
        categoria={
            'N':'Categoria',
            'id':i.id,
            'nombre':i.nombre,
            'descripcion':i.descripcion,
            'cargaTrabajo':i.cargaTrabajo,
        }
        json.append(categoria)

        for j in i.lista_configuraciones:
            configuracion={
                'N':'Configuracion',
                'id':j.id,
                'nombre':j.nombre,
                'descripcion':j.descripcion,
            }
            json.append(configuracion)

            for k in j.lista_recursos:
                recurso={
                    'N':'Recurso',
                    'id':k.id,
                    'cantidad':k.cantidad
                }
                json.append(recurso)

    return jsonify(json),200

@app.route('/clientes',methods=['GET'])
def obtener_clientes():
    global lista_recursos, lista_categorias, lista_clientes
    json=[]
    for i in lista_clientes:
        cliente={
            'N':'Cliente',
            'nit':i.nit,
            'nombre':i.nombre,
            'usuario':i.usuario
        }
        json.append(cliente)

        for j in i.lista_instancias:
            instancia={
                'N':'Instancia',
                'id':j.id,
                'id_configuracion':j.id_configuracion,
                'nombre':j.nombre,
                'fecha_inicio':j.fecha_inicio,
                'estado':j.estado,
                'fecha_final':j.fecha_final
            }
            json.append(instancia)

    return jsonify(json),200


@app.route('/crear_recursos',methods=['POST'])
def crear_recursos():
    json=request.get_json()
    existe=False

    for i in lista_recursos:
        if(json['id']==i.id):
            existe=True

    if(existe==False):
        lista_recursos.append(Recursos(json['id'],json['nombre'],json['abreviatura'],json['metrica'], json['tipo'],json['valor_hora']))
        return jsonify({'ok':True, 'data':'Recurso añadida con exito'}),200
    else:
        return jsonify({'ok':False, 'data':'Id ingresada, ya esta registrada '}),200      


@app.route('/crear_categorias',methods=['POST'])
def crear_categorias():
    json=request.get_json()
    existe=False

    for i in lista_categorias:
        if(json['id']==i.id):
            existe=True

    if(existe==False):
        lista_categorias.append(Categoria(json['id'],json['nombre'],json['descripcion'],json['cargaTrabajo']))
        return jsonify({'ok':True, 'data':'Categoria añadida con exito'}),200
    else:
        return jsonify({'ok':False, 'data':'Id ingresada, ya esta registrada '}),200   

@app.route('/crear_configuraciones',methods=['POST'])
def crear_configuraciones():
    json=request.get_json()
    existe=False
    existe2=False

    for i in lista_categorias:
        if(json['id_categoria']==i.id):
            objeto=i
            existe=True

    if(existe==True):
        for j in objeto.lista_configuraciones:
            if(j.id==json['id']):
                existe2=True        

    if(existe==True) and (existe2==False):
        objeto.lista_configuraciones.append(Configuracion(json['id'],json['nombre'],json['descripcion']))
        return jsonify({'ok':True, 'data':'Configuracion añadida con exito a categoria'}),200
    else:
        return jsonify({'ok':False, 'data':'Ocurrio un problema al momento de ingresar la informacion'}),200   

@app.route('/crear_recursosconfiguracio',methods=['POST'])
def crear_recursosconfiguracio():
    json=request.get_json()
    existe=False
    existe2=False
    existe3=False

    for i in lista_categorias:
        if(json['id_categoria']==i.id):
            objeto=i
            existe=True

    if(existe==True):
        for j in objeto.lista_configuraciones:
            if(j.id==json['id_configuracion']):
                objetocategoria=j
                existe2=True       

    if(existe2==True):
        for k in objetocategoria.lista_recursos:
            if(k.id==json['id']):
                existe3=True       


    if(existe==True) and (existe2==True) and (existe3==False):
        objetocategoria.lista_recursos.append(RecursosC(json['id'],json['cantidad']))
        return jsonify({'ok':True, 'data':'Recurso añadido con exito a configuracion'}),200
    else:
        return jsonify({'ok':False, 'data':'Ocurrio un problema al momento de ingresar la informacion'}),200   





@app.route('/crear_clientes',methods=['POST'])
def crear_clientes():
    json=request.get_json()
    existe=False

    for i in lista_clientes:
        if(i.nit==json['nit']):
            existe=True

    if(existe==False):
        lista_clientes.append(Usuario(json['nit'],json['nombre'],json['usuario'],json['clave'], json['direccion'],json['correo']))
        return jsonify({'ok':True, 'data':'Cliente añadido con exito'}),200
    else:
        return jsonify({'ok':False, 'data':'Nit ingresada, ya esta registrada'}),200     

@app.route('/crear_instancia',methods=['POST'])
def crear_instancia():
    json=request.get_json()
    existe=False
    existe2=False

    for i in lista_clientes:
        if(json['id_cliente']==i.id):
            objeto=i
            existe=True

    if(existe==True):
        for j in objeto.lista_instancias:
            if(j.id==json['id']):
                existe2=True        

    if(existe==True) and (existe2==False):
        objeto.lista_instancias.append(Instancias(json['id'],json['id_configuracion'],json['nombre'],json['fecha_inicio'],json['estado'],json['fecha_final']))
        return jsonify({'ok':True, 'data':'Configuracion añadida con exito a categoria'}),200
    else:
        return jsonify({'ok':False, 'data':'Ocurrio un problema al momento de ingresar la informacion'}),200     