from importlib.util import set_loader
import re
from tabulate import tabulate
import random

# Funcion para Encontrar los Lexemas,
# retorna un arreglo bidimensional que contiene cada lexema encontrado, el tipo de token y la posicion en la linea
# retorna falso si no reconoce el token e imprime el error


def encontrarLexemas(entrada, tokens):
    lexemas = []
    currentLine = 1
    for cadena in entrada:
        posicion = 0
        cadenaRecorrer = cadena
        cadenaRecorrer = re.sub(r"\n$", " ", cadenaRecorrer)
        cadenaRecorrer = cadenaRecorrer.strip('$')
        print(cadenaRecorrer)
        while cadenaRecorrer != "":
            encontrado = False
            if(re.match(' ', cadenaRecorrer)):
                cadenaRecorrer = cadenaRecorrer[1:len(cadenaRecorrer)]
                posicion = posicion+1
            else:
                for token in tokens:
                    encontrar = re.match(tokens[token], cadenaRecorrer)
                    print
                    if(encontrar):
                        inicio = encontrar.start()
                        final = encontrar.end()
                        valor = cadenaRecorrer[encontrar.start(
                        ):encontrar.end()]
                        lexemaencontrado = [currentLine, token, valor]
                        posicion = posicion+final-inicio
                        lexemas.append(lexemaencontrado)
                        cadenaRecorrer = cadenaRecorrer[final: len(
                            cadenaRecorrer)]
                        encontrado = True
                if not encontrado:
                    print('token inesperado: ' +
                          cadenaRecorrer[posicion:len(cadenaRecorrer)]+'\n' +
                          'linea: ' + str(currentLine) + '\n' +
                          cadena+"\n" +
                          " "*(posicion) + "^")
                    return False
        currentLine = currentLine + 1
    return lexemas

# Separa por ;


def separarInstrucciones(tokens, sistemas):
    instrucciones = []
    instruccion = []
    cont = 0
    c = 0
    for token in tokens:
        # guardar tocken temporalmente en instruccion para evaluarla
        instruccion.append(token)
        c = c+1
        # si es el fin de una cadena
        if token[1] == 'finL':
            cont = cont+1
            if (instruccion[0][1] == 'decimal' and instruccion[1][1] in sistemas and instruccion[2][1] == 'finL' and len(instruccion) == 3):
                instrucciones.append(instruccion)
                instruccion = []
            else:
                a = ''
                for i in instruccion:
                    a = a+i[2]
                print('ERROR01: instrucción:', str(cont),
                      'vacía', '->', instruccion[0][2])
                return False
        elif c == len(tokens):
            print('Se esperaba ;')
            return False
    return instrucciones


# Funciones de conversión de números
def convBin(n):
    if n == 0:
        return "0"
    binario = ""
    while n > 0:
        residuo = int(n % 2)
        n = int(n / 2)
        binario = str(residuo) + binario
    return binario


def obtenerCaracterHex(valor):
    valor = str(valor)
    equivalencias = {
        "10": "a",
        "11": "b",
        "12": "c",
        "13": "d",
        "14": "e",
        "15": "f",
    }
    if valor in equivalencias:
        return equivalencias[valor]
    else:
        return valor


def convHex(n):
    hexadecimal = ""
    while n > 0:
        residuo = n % 16
        verdadero_caracter = obtenerCaracterHex(residuo)
        hexadecimal = verdadero_caracter + hexadecimal
        n = int(n / 16)
    return hexadecimal


def convOct(n):
    octal = ""
    while n > 0:
        residuo = n % 8
        octal = str(residuo) + octal
        n = int(n / 8)
    return octal


def convAsc(n):
    if(n > 0 and n <= 177):
        return chr(n)
    else:
        return 'Rango Excedido'


def convRom(n):
    romano = ''
    while n > 0:
        if(n >= 1000):
            romano = romano + 'M'
            n -= 1000
        elif(n >= 500):
            romano = romano + 'D'
            n -= 500
        elif(n >= 500):
            romano = romano + 'C'
            n -= 100
        elif(n >= 50):
            romano = romano + 'L'
            n -= 50
        elif(n >= 10):
            romano = romano + 'X'
            n -= 10
        elif(n >= 5):
            romano = romano + 'V'
            n -= 5
        else:
            romano = romano + 'I'
            n -= 1
    return romano


def convAle(n):
    instruccionAleatoria = random.choice((list(Sistemas.keys())))
    if(instruccionAleatoria == 'binario'):
        return convBin(n)
    elif(instruccionAleatoria == 'octal'):
        return convOct(n)
    elif(instruccionAleatoria == 'hexadecimal'):
        return convHex(n)
    elif(instruccionAleatoria == 'romano'):
        return convRom(n)
    elif(instruccionAleatoria == 'asc'):
        return convAsc(n)
    else:
        return convAle(n)

# Toma la lista de instrucciones y devuelve los resultados


def operar(instrucciones):
    resultados = []
    for instruccion in instrucciones:
        match instruccion[1][1]:
            case 'binario': resultados.append(convBin(int(instruccion[0][2])))
            case 'octal': resultados.append(convOct(int(instruccion[0][2])))
            case 'hexadecimal': resultados.append(convHex(int(instruccion[0][2])))
            case 'romano': resultados.append(convRom(int(instruccion[0][2])))
            case 'aleatorio': resultados.append(convAle(int(instruccion[0][2])))
            case 'ascii': resultados.append(convAsc(int(instruccion[0][2])))
    return resultados


def validaciónFinalCadena(cadena):
    dolar = 0
    for elements in cadena:
        if re.match('\$', elements):
            dolar = dolar + 1
    if(re.search(r"\$$", cadena)):
        if dolar > 1:
            print(" ERROR05: Se encontró más de un operador final $")
            return False
        else:
            return True
    else:
        print('ERROR04: no se encontró el operador final $')
        return(False)


# Diccionario de tokens de sistemas numericos a convertir
Sistemas = {'binario': 'bin', 'octal': 'oct', 'hexadecimal': 'hex',
            'romano': 'rom', 'aleatorio': 'ale', 'ascii': 'asc'}

# Diccionario de tokens permitidos por el analizador lexico
tokens = {'decimal': '\d+', 'binario': 'bin', 'octal': 'oct', 'hexadecimal': 'hex',
          'romano': 'rom', 'aleatorio': 'ale', 'ascii': 'asc', 'finL': ';'}

# abriendo el archivo y uniendo las lineas en un solo string
f = open('./entrada.txt', 'r')
entradaLimpia = ""
entrada = []
for x in f:
    # eliminamos los saltos de linea
    x = re.sub(r"\n$", " ", x)
    entradaLimpia = entradaLimpia+x
    entrada.append(x)

# ---->eliminamos espacios en blanco
entradaLimpia = (entradaLimpia.replace(" ", "")).replace(
    '\n', '').replace('\t', '')

# inicio
cadenaValida = validaciónFinalCadena(entradaLimpia)
if(cadenaValida):
    encuentra = encontrarLexemas(entrada, tokens)
    if(encuentra):
        print('\n---- ANÁLISIS LÉXICO ----\n')
        print('\nCADENA DE TOKENS\n')
        header = ['Linea', 'token', 'LEXEMA']
        print(tabulate(encuentra, header))
        separa = separarInstrucciones(encuentra, Sistemas)
        if(separa and len(separa) > 0):
            print('\nINSTRUCCIONES ENCONTRADAS\n-------------------------')
            for i in separa:
                print(i[0][2]+i[1][2]+i[2][2])
            resultados = operar(separa)
            # preparando resultados
            print('\n---- ANÁLISIS SINTÁCTICO ----\n')
            print('\nRESULTADOS\n----------')
            cont = 0
            for resultado in resultados:
                print(separa[cont][0][2]+separa[cont][1][2], '->', resultado)
                cont = cont+1

        else:
            print('ERROR 03: se encontró una instrucción no válida')
    else:
        print('ERROR 03: Error de sintaxis')
