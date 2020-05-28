#Maria Venegas Berrocal
#Alejandro Centeno Chaves
#Hilary González Abarca
# CONSTANTES

import string
import os
import math

DIGITOS = '0123456789'
LETRAS = string.ascii_letters
LETTERS_DIGITS = LETRAS + DIGITOS
NUM_LINEA = 0

#######################################


#######################################
# POSICION
#######################################

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        result = 'La linea {} contiene un error, el lexema identificado con error es: {}.'.format(NUM_LINEA, self.details)
        return result

class Posicion:
    def __init__(self, indice, linea, col, fin, ftxt):
        self.indice = indice
        self.linea = linea
        self.col = col
        self.fin = fin
        self.ftxt = ftxt

    def avanzar(self, char_actual):
        self.indice += 1
        self.col += 1

        if char_actual == '\n':
            self.linea += 1
            self.col = 0

        return self

    def copiar(self):
        return Posicion(self.indice, self.linea, self.col, self.fin, self.ftxt)

#######################################
# TOKENS
#######################################

TOK_PROGRAMA = 'Programa'
TOK_CLASE_PRINCIPAL = 'ClasePrincipal'
TOK_IDENTIFICADOR	= 'Identificador'
TOK_RESERVADA		= 'reservada'
TOK_ClAS_DEF = 'ClasDef'
TOK_DECL_DEF = 'DeclVar'
TOK_DECL_MET = 'DeclMet'
TOK_LISTA_FORMAL = 'ListaFormal'
TOK_RESTO_FORMAL	= 'RestoFormal'
TOK_TIPO = 'Tipo'
TOK_DECLARACION = 'Declaracion'
TOK_EXPRESION    = 'Expresion'
TOK_LISTA_EXP     = 'ListaExp'
TOK_ASIGNACION    = 'asignacion'
TOK_ENT = 'digitos'
TOK_COMENT = 'comentario'
TOK_OPERADOR = 'operador'

reservadas = [
    'clase',
    'si',
    'mientras',
    'entonces',
]

operadores = [
    '+',
    '*',
    '-',
    '&&',
    '||',
    '==',
    '!=',
    '<',
    '>',
    '<=',
    '>=',
    '=',
]

class Token:
	# Edite la variable tipo y valor, si no funcionan entonces hay que devolverlo a type y value xD
    def __init__(self, tipo_, valor=None, pos_start=None, pos_end=None):
        self.tipo = tipo_
        self.valor = valor
    
    def __repr__(self):
        if self.valor: return ('{} : {}'.format(self.tipo, self.valor))
        return '{}'.format(self.tipo)

#######################################
# ANALIZADOR LEXICO
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

        while self.current_char != None:
            if self.current_char in ' \t':
                self.avanzar()
            elif self.current_char in DIGITOS:
                tokens.append(self.crear_numero())
            elif self.current_char in LETRAS:
                tokens.append(self.crear_identificador())
            elif self.current_char in operadores:
                tokens.append(Token(TOK_OPERADOR, self.current_char))
                self.avanzar()
            elif self.current_char == '/':
                tokens.append(self.crear_comentario())
                self.avanzar()
            elif self.current_char == ')':
                tokens.append(self.crear_comentario)
                self.avanzar()
            elif self.current_char == '\n':
                self.avanzar()
            else:
                pos_start = self.pos.copiar()
                char = self.current_char
                self.avanzar()
                mensaje = Error(pos_start, self.pos, "Reporte de Error", "'" + char + "'")
                return [], mensaje
                

        return tokens, None




    def crear_identificador(self):
        identi = ''
        inicio = self.pos.copiar()
        bandera = False
        while bandera == False:
            if(self.current_char != None and self.current_char in LETTERS_DIGITS + '_'):
                identi += self.current_char
                self.avanzar()

            else:
                bandera = True
                self.avanzar()

        tok_type = TOK_RESERVADA if identi in reservadas else TOK_IDENTIFICADOR
        return Token(tok_type, identi, inicio, self.pos)
    
    
    def crear_numero(self):
        inicio = self.pos
        num_str = ''
        dot_count = 0
        bandera = False

        while bandera == False:
            if(self.current_char != None and self.current_char in LETTERS_DIGITS + '.'):
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
                self.avanzar()

        try:
            if dot_count == 0:
                return Token(TOK_ENT, int(num_str))
            else:
                return Token(TT_FLOAT, float(num_str))
        except ValueError:
            mensaje = Error(inicio, self.pos, "Reporte de Error", "'" + num_str + "'")
            return mensaje

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

            return Token(TOK_COMENT, comentario)

        else:

            return Token(TOK_OPERADOR, comentario)

            

#######################################
# RUN
#######################################

def run(fin, text, linea):
    global NUM_LINEA
    NUM_LINEA = linea
    anlex = analizadorLexico(fin, text)
    tokens, error = anlex.crear_tokens()

    return tokens, error
