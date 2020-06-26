#Maria Venegas Berrocal
#Alejandro Centeno Chaves
#Hilary González Abarca
# CONSTANTES

import string
import os
import math
from string_with_arrows import *
# Conjuntos de valores numericos y caracteres.
# Serán utilizados para la generación de tokens.

DIGITOS = '0123456789'
LETRAS = string.ascii_letters
LETRAS_DIGITOS = LETRAS + DIGITOS
NUM_LINEA = 0 # Linea de código en lectura.


#######################################
# Clase encargada del manejo de errores.
# Solamente es capaz de identificar la linea
# y el token que posee el fallo.
#######################################

    
class Error:
    def __init__(self, pos_inicio, pos_fin, error_nombre, detalles):
        self.pos_inicio = pos_inicio
        self.pos_fin = pos_fin
        self.error_nombre = error_nombre
        self.detalles = detalles
    
    def as_string(self):
        resultado = 'La línea {}, Con error sintáctico, cercano al toquen {}'.format(NUM_LINEA, self.error_nombre)
        return resultado

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)


#######################################
# NODES
#######################################

## Aqui es donde clasifica algo como un numero, operacion binaria o unary
class Numero:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end
    def __repr__(self):
        return self.tok

class OpBinaria:
    def __init__(self, nodo_izq, op, nodo_der):
        self.nodo_izq = nodo_izq
        self.op = op
        self.nodo_der = nodo_der

    def __repr__(self):
        return self.nodo_izq, self.op, self.nodo_der

class AccesarVarNodo:
    def __init__(self, var_nombre_tok):
        self.var_nombre_tok = var_nombre_tok

        self.pos_start = self.var_nombre_tok.pos_start
        self.pos_end = self.valor_node.pos_end

class AsignarVarNodo:
    def __init__(self, var_nombre_tok, valor_node):
        self.var_nombre_tok = var_nombre_tok
        self.valor_node = valor_node

        self.pos_start = self.var_nombre_tok.pos_start
        self.pos_end = self.valor_node.pos_end

class OpUn:
    def __init__(self, op, nodo):
        self.op = op
        self.nodo = nodo

    def __repr__(self):
        return self.op, self.nodo
#######################################
# PARSE RESULT
#######################################

class Resultado:
    def __init__(self):
        self.error = None
        self.nodo = None
        self.avanzar_cont = 0

    def registro_avanzado(self):
        self.avanzar_cont += 1

    def registrar(self, res):
        if isinstance(res, Resultado):
            if res.error: 
                self.error = res.error
            return res.nodo
        return res

    def exito(self, nodo): #Si se pudo cerrar la expresion todo bien entonces retorna eso para seguir parseando
        self.nodo = nodo
        return self

    def fallo(self, error): #En caso que no se pudo hacer la expresion por algun error sintactico, termina y manda a avisar
        self.error = error
        return self

#######################################
# PARSER
#######################################

class analizadorSintactico:
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_indice = -1
        self.avanzar()

    def avanzar(self,):
        self.tok_indice += 1
        if self.tok_indice < len(self.tokens):
            self.tok_actual = self.tokens[self.tok_indice]
        return self.tok_actual

    def enlazar(self): # Es la que inicia todo, manda la expresion a parsear y retorna un error o la expresion
        res = self.expr()
        if not res.error and self.tok_actual.tipo != TOK_EOF:
            return res.fallo(Error(
                self.tok_actual.pos_start, self.tok_actual.pos_end,self.tok_actual.tipo,
                "Reporte de Error"))
        return res

    ###################################
    def atom(self):
        res = Resultado()
        tok = self.tok_actual

        if tok.tipo == TOK_TIPO:
            res.registro_avanzado()
            self.avanzar()
            return res.exito(Numero(tok))

        elif tok.tipo == TOK_IDENTIFICADOR:
            res.registro_avanzado()
            self.avanzar()
            return res.exito(AccesarVarNodo(tok))

        elif tok.type == TOK_PARENIZQ:
            res.registro_avanzado()
            self.avanzar()
            expr = res.registrar(self.expr())
            if res.error: return res
            if self.tok_actual.tipo == TOK_PARENDER:
                res.registro_avanzado()
                self.avanzar()
                return res.exito(expr)
            else:
                return res.falla(InvalidSyntaxError(self.tok_actual.pos_start, self.tok_actual.pos_end,"Se esperaba un ')'"))

            return res.falla(InvalidSyntaxError(tok.pos_start, tok.pos_end,"Se esperaba un int, float, identifier, '+', '-' o '('"))


    def power(self):
        return self.bin_op(self.atom, (TOK_POT, ), self.factor)

    
    def factor(self):
        res = Resultado()
        tok = self.tok_actual
        if tok.tipo in (TOK_SUM, TOK_RESTA): ## si es suma o resta entonces lo clasifica como op unary
            res.registrar(self.avanzar())
            factor = res.registrar(self.factor())
            if res.error: return res
            return res.exito(OpUn(tok, factor))
        
        return self.power()
    
    def term(self): #Clasificar como termino 
        return self.bin_op(self.factor, (TOK_MUL, TOK_DIV))

    def expr(self): #Clasificar como expresion
        res = Resultado()

        if (self.tok_actual.iguales(TOK_TIPO,'ent')) or (self.tok_actual.iguales(TOK_TIPO,'ent[]')) or (self.tok_actual.iguales(TOK_TIPO,'Cadena[]')) or (self.tok_actual.iguales(TOK_TIPO,'Cadena')) or (self.tok_actual.iguales(TOK_TIPO,'bool')):
            res.registrar(self.avanzar())

        if self.tok_actual.tipo != TOK_IDENTIFICADOR:
            return res.fallo(InvalidSyntaxError(self.tok_actual.pos_start, self.tok_actual.pos_end,"Se esperaba un identificador"))

        nombre_var = self.tok_actual
        res.registrar(self.avanzar())

        if self.tok_actual.tipo != TOK_ASIG:
            return res.fallo(InvalidSyntaxError(self.tok_actual.pos_start, self.tok_actual.pos_end,"Se esperaba un '='"))

        res.registrar(self.avanzar())
        expr = res.registrar(self.expr())
        if res.error: return res
        return res.exito(AsignarVarNodo(nombre_var,expr))

        
        return self.bin_op(self.term, (TOK_SUM, TOK_RESTA))

    ###################################

    def bin_op(self, func, ops): #Revisa si es una operacion de multiplicacion o division para mandar a clasificarlo
        res = Resultado()
        izq = res.registrar(func())
        if res.error: return res
        while self.tok_actual.tipo in ops:
            op_tok = self.tok_actual
            res.registrar(self.avanzar())
            der = res.registrar(func())
            if res.error: return res
            izq = OpBinaria(izq, op_tok, der)

        return res.exito(izq)

    


#######################################
# La clase Posición se encarga de llevar
# el control del avance de la lectura de
# la linea.
#######################################

class Posicion:
    def __init__(self, indice, linea, col, fin, ftxt):
        self.indice = indice
        self.linea = linea
        self.col = col
        self.fin = fin
        self.ftxt = ftxt

    def avanzar(self, char_actual=None):
        self.indice += 1
        self.col += 1

        if char_actual == '\n':
            self.linea += 1
            self.col = 0

        return self

    def copiar(self):
        return Posicion(self.indice, self.linea, self.col, self.fin, self.ftxt)

#######################################
# Aquí se definen los tokens y las listas
# de elementos esperadas para cada una de
# ellas.
#
# Esto está basado en el recuadro de
# analisis sintactico traducido.
#######################################

TOK_PROGRAMA = 'Programa'
TOK_CLASE_PRINCIPAL = 'ClasePrincipal'
TOK_IDENTIFICADOR   = 'Identificador'
TOK_RESERVADA       = 'reservada'
TOK_CLAS_DEF = 'ClasDef'
TOK_DECL_DEF = 'DeclVar'
TOK_DECL_MET = 'DeclMet'
TOK_LISTA_FORMAL = 'ListaFormal'
TOK_RESTO_FORMAL    = 'RestoFormal'
TOK_TIPO = 'Tipo'
TOK_DECLARACION = 'Declaracion'
TOK_EXPRESION    = 'Expresion'
TOK_LISTA_EXP     = 'ListaExp'
TOK_ASIGNACION    = 'asignacion'
TOK_ENT = 'entero'
TOK_COMENT = 'comentario'
TOK_OPERADOR = 'operador'
TOK_PARENIZQ = 'parentizq'
TOK_PARENDER= 'parentder'
TOK_CORIZQ = 'corcheteizq'
TOK_CORDER= 'corcheteder'
TOK_CADENA = 'cadena'
TOK_EOF         = 'EOF'
TOK_MUL = 'OPERADOR MULTIPLICACION'
TOK_DIV = 'OPERADOR DIVISION'
TOK_SUM = 'OPERADOR SUMA'
TOK_RESTA = 'OPERADOR RESTA'
TOK_ASIG =     'ASIGNACION'
TOK_POT = 'Potencia'

tipos = ['ent','ent[]','Cadena[]','Cadena',
    'bool','largo','vacio']

reservadas = [
    'si',
    'clase',
    'mientras',
    'entonces',
    'imprimir',
    'Verdadero',
    'Falso',
    'esto',
    'nuevo',
    'ent',
    'publico',
    'bool',
    'extiende',
    'retornar',
    'largo',
    'estatico',
    'principal',
    'Cadena'
]
clasdecls = [
    'clase',
    'extiende']
exp = [    
    'Verdadero',
    'Falso',
    'esto',
    'nuevo',
    '!']

operadores = [
    '&',
    '|',
    '==',
    '!=',
    '<',
    '>',
    '<=',
    '>=', 
]

ignorar = [';','.',':']


#############################################
# La clase token se encarga de crear la tupla
# con el token identificado y su respectivo
# identificador.
#############################################

class Token:
    # Edite la variable tipo y valor, si no funcionan entonces hay que devolverlo a type y value xD
    def __init__(self, tipo_, valor=None, pos_start=None, pos_end=None):
        self.tipo = tipo_
        self.valor = valor
        
        if pos_start:
            self.pos_start = pos_start.copiar()
            self.pos_end = pos_start.copiar()
            self.pos_end.avanzar()
            
        if pos_end:
            self.pos_end = pos_end.copiar()

    def iguales(self, tipo_, valor):
        return self.tipo == tipo_ and self.valor == valor
         
    
    def __repr__(self):
        if self.valor: return ('{} , {}'.format(self.tipo, self.valor))
        return '{}'.format(self.tipo)

#######################################
# La clase de analisis sintactico es la
# que explicitamente se encarga de clasificar
# cada elemento entrante de la linea en alguna
# de las funciones encargadas de realizar
# el análisis de los valores.
#######################################

class analizadorLexico:
    def __init__(self, fin, texto):
        self.fin = fin
        self.texto = texto
        self.pos = Posicion(-1, 0, -1, fin, texto)
        self.current_char = None
        self.avanzar()
    
    def avanzar(self):
        self.pos.avanzar(self.current_char)
        self.current_char = self.texto[self.pos.indice] if self.pos.indice < len(self.texto) else None

    def crear_tokens(self):
        tokens = []

        # Aquí se toma un caracter de la linea, y dependiendo de su valor, es enviado a la
        # función encargada de continuar con el análisis de la palabra.
        # *Un valor no reconocido será tomado como error*
        
        while self.current_char != None:
           if self.current_char in ' \t':
                self.avanzar()
           elif self.current_char in ignorar:
                self.avanzar()
           elif self.current_char in DIGITOS:
                tokens.append(self.crear_numero())
           elif self.current_char in LETRAS:
                tokens = self.crear_identificador(tokens)
           elif self.current_char == '+':
                tokens.append(Token(TOK_SUM,pos_start=self.pos))
                self.avanzar()
           elif self.current_char == '-':
                tokens.append(Token(TOK_RESTA,pos_start=self.pos))
                self.avanzar()
           elif self.current_char == '/':
                tokens.append(Token(TOK_DIV,pos_start=self.pos))
                self.avanzar()

           elif self.current_char == '^':
                tokens.append(Token(TOK_POT, pos_start=self.pos))
                self.avanzar()
           elif self.current_char == '=':
                tokens.append(self.crear_operador())
                self.avanzar()
           elif self.current_char == '*':
                tokens.append(Token(TOK_MUL,pos_start=self.pos))
                self.avanzar()
           elif self.current_char in operadores:
                tokens.append(self.crear_operador())
                self.avanzar()
           elif self.current_char == '/':
                tokens.append(self.crear_comentario())
                self.avanzar()
           elif self.current_char == '"':
                tokens.append(self.crear_cadena())
                self.avanzar()
           elif self.current_char == '(':
                tokens.append(Token(TOK_PARENIZQ,self.current_char))
                self.avanzar()
           elif self.current_char == ')':
                tokens.append(Token(TOK_PARENDER,self.current_char))
                self.avanzar()
           elif self.current_char == '\n':
                self.avanzar()
           elif self.current_char == '{':
                tokens.append(Token(TOK_CORIZQ,self.current_char))
                self.avanzar()
           elif self.current_char == '}':
                tokens.append(Token(TOK_CORDER,self.current_char))
                self.avanzar()
           elif self.current_char == '\n':
                self.avanzar()
           else:
                pos_start = self.pos.copiar()
                char = self.current_char
                self.avanzar()
                mensaje = Error(pos_start, self.pos, "Reporte de Error", "'" + char + "'")
                return tokens, mensaje
                

        return tokens, None




    ########################################################################
    # un tipo, una expresión o un identificador.
    # solo caracter. Adicionalmente valida si se trata de una declaración,
    # Esta función se encarga de contruir palabras a partir de un
    ########################################################################
    def crear_identificador(self,tokens):
        identi = ''
        inicio = self.pos.copiar()
        bandera = False
        tok_type = ''
        while bandera == False:
            if(self.current_char != None and self.current_char in LETRAS_DIGITOS + '_') or (self.current_char == '[') or (self.current_char == ']'):
                identi += self.current_char
                self.avanzar()

            else:
                bandera = True

        if identi == 'principal':
            tok_type = TOK_CLASE_PRINCIPAL
            tokens.append(Token(tok_type, identi, inicio, self.pos))
        elif identi in clasdecls:
            tok_type = TOK_CLAS_DEF
            tokens.append(Token(tok_type, identi, inicio, self.pos))
        elif identi == 'public':
            tok_type = TOK_DeclMet
            tokens.append(Token(tok_type, identi, inicio, self.pos))    
        elif identi in exp:
            tok_type = TOK_EXPRESION
            tokens.append(Token(tok_type, identi, inicio, self.pos))
        elif identi in tipos:
            tok_type = TOK_TIPO
            tokens.append(Token(tok_type, identi, inicio, self.pos))
        elif identi in reservadas:
            tok_type = TOK_RESERVADA
            tokens.append(Token(tok_type, identi, inicio, self.pos))
        else:
            tok_type = TOK_IDENTIFICADOR
            tokens.append(Token(tok_type, identi, inicio, self.pos))
        return tokens
    

    ##########################################################################
    # Esta función se encarga de crear números, enteros o flotantes, a partir de
    # un valor númerico. Palabras que inicien por valores númericos en combinación
    # de letras serán tomadas como error.
    #############################################################################
    
    def crear_numero(self):
        inicio = self.pos
        num_str = ''
        dot_count = 0
        bandera = False
        pos_start = self.pos.copiar()
        while bandera == False:
            if(self.current_char != None and self.current_char in LETRAS_DIGITOS + '.'):
                if self.current_char == '.':
                    if dot_count == 1: break
                    dot_count += 1
                    num_str += '.'

                elif self.current_char in LETRAS:
                    num_str += self.current_char
                
                else:
                    num_str += self.current_char
                self.avanzar()

            else:
                bandera = True

        try:
            if dot_count == 0:
                return Token(TOK_ENT, int(num_str),pos_start, self.pos)

        except ValueError:
            mensaje = Error(inicio, self.pos, "Reporte de Error", "'" + num_str + "'")
            return mensaje.as_string()


    #########################################################################
    # Esta función se encarga de contruir comentarios. Inicia con el caracter
    # '/', si este es seguido por '*' se empezará a crear un comentario; caso
    # contrario el valor se tomará como un operador.
    ##########################################################################
    
    def crear_comentario(self):

        comentario = self.current_char
        bandera = False
        comentario_final = ''
        posInicio = self.pos.copiar()
        self.avanzar()

        if self.current_char == '*':

            while bandera == False:
                if(comentario_final == '*') and (self.current_char == '/'):
                    comentario += self.current_char
                    self.avanzar()
                    bandera = True

                else:
                    comentario_final = self.current_char
                    comentario += self.current_char
                    self.avanzar()

            return Token(TOK_COMENT, comentario, posInicio, self.pos)

        else:

            return Token(TOK_OPERADOR, comentario, posInicio, self.pos)


    #########################################################################
    # Esta función se encarga de contruir cadenas. Inicia con el caracter
    # '"'.
    ##########################################################################
    def crear_cadena(self):

        cadena = self.current_char
        self.avanzar()
        pos_start = self.pos.copiar()

        while self.current_char != '"':
            cadena += self.current_char
            self.avanzar()


        return Token(TOK_CADENA, cadena,pos_start, self.pos)


    
    ##################################################################################
    # Esta función lleva a cabo el reconocimiento de operadores, además de contruir
    # aquellos formados por dos caracteres, tales como '<=', '==' o '&&'.
    # *Un signo de igual (=) solo, será definido como operador de asiganción*
    ##################################################################################
    def crear_operador(self):
        inicio = self.current_char
        operador = ''
        bandera = False
        pos_start = self.pos.copiar()

        while bandera == False:
            if(self.current_char != None and self.current_char in operadores):

                operador += self.current_char
                self.avanzar()

            else:
                bandera = True

        if inicio == '=':
            return Token(TOK_ASIGNACION, inicio, pos_start,self.pos)
        else:
            return Token(TOK_OPERADOR, operador,pos_start,self.pos)

            

###########################################
# Función que inicia el flujo del programa
###########################################

def run(fin, text, linea):
    
    global NUM_LINEA
    NUM_LINEA = linea
    anlex = analizadorLexico(fin, text)
    tokens, error = anlex.crear_tokens()
    if error: return tokens, error
    
    # Generar AST
    print(tokens)
    ansin = analizadorSintactico(tokens)
    ast =  ansin.enlazar()

    return ast.nodo, ast.error
