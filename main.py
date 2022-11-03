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
