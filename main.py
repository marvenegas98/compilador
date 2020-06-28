#Maria Venegas Berrocal
#Alejandro Centeno Chaves
#Hilary González Abarca
# CONSTANTES

import string
import os
import math
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
###################################

class Error:
  def __init__(self, pos_inicio, pos_fin, error_nombre, detalles):
    self.pos_inicio = pos_inicio
    self.pos_fin = pos_fin
    self.error_nombre = error_nombre
    self.detalles = detalles
  
  def as_string(self):
        resultado = 'Línea: {}, Con error sintáctico, cercano al toquen {}'.format(NUM_LINEA, self.error_nombre)
        return resultado


#######################################
# La clase Posición se encarga de llevar
# el control del avance de la lectura de
# la linea.
#######################################

class Posicion:
  def __init__(self, indice, ln, col, fn, ftxt):
    self.indice = indice
    self.ln = ln
    self.col = col
    self.fn = fn
    self.ftxt = ftxt

  def avanzar(self, char_actual=None):
    self.indice += 1
    self.col += 1

    if char_actual == '\n':
      self.ln += 1
      self.col = 0

    return self

  def copiar(self):
    return Posicion(self.indice, self.ln, self.col, self.fn, self.ftxt)

#######################################
# Aquí se definen los tokens y las listas
# de elementos esperadas para cada una de
# ellas.
#
# Esto está basado en el recuadro de
# analisis sintactico traducido.
#######################################
TOK_ENT             = 'ENT'
TOK_CADENA          = 'CADENA'
TOK_IDENTIFICADOR   = 'identificador'
TOK_RESERVADA       = 'reservada'
TOK_SUMA        = 'OPERADOR SUMA'
TOK_RESTA       = 'OPERADOR RESTA'
TOK_MUL         = 'OPERADOR MUL'
TOK_DIV         = 'OPERADOR DIV'
TOK_ELV             = 'ELEVADO'
TOK_ASIG                    = 'OPERADOR ASIGNACION'
TOK_PARENTIZQ       = 'PARENTIZQ'
TOK_PARENTDER   = 'PARENTDER'
TOK_IGUALDAD                    = 'OPERADOR IGUALDAD'
TOK_DESIGUALDAD                 = 'OPERADOR DESIGUALDAD'
TOK_MENORQ                  = 'OPERADOR MENOR QUE'
TOK_MAYORQ                  = 'OPERADOR MAYOR QUE'
TOK_MENORIG             = 'OPERADOR MENOR IGUAL QUE'
TOK_MAYORIG             = 'OPERADOR MAYOR IGUAL QUE'
TOK_COMMA               = ','
TOK_EOF             = 'EOF'
TOK_COMMENT = 'comentario'

reservadas = [
  'clase',
  'ent',
  'cadena',
  '&&',
  '||',
  'si',
  'entonces',
  'mientras',
  'publico',
  'imprimir',
  'esto',
  'nuevo',
]

#############################################
# La clase token se encarga de crear la tupla
# con el token identificado y su respectivo
# identificador.
#############################################

class Token:
  def __init__(self, type_, valor=None, pos_inicio=None, pos_fin=None):
    self.tipo = type_
    self.valor = valor

    if pos_inicio:
      self.pos_inicio = pos_inicio.copiar()
      self.pos_fin = pos_inicio.copiar()
      self.pos_fin.avanzar()

    if pos_fin:
      self.pos_fin = pos_fin.copiar()

  def iguales(self, type_, valor):
    return self.tipo == type_ and self.valor == valor
  
  def __repr__(self):
    if self.valor: return f'{self.tipo}:{self.valor}'
    return f'{self.tipo}'
#######################################
# La clase de analisis Lexico es la
# que explicitamente se encarga de clasificar
# cada elemento entrante de la linea en alguna
# de las funciones encargadas de realizar
# el análisis de los valores.
#######################################

class analizadorLexico:
  def __init__(self, fn, text):
    self.fn = fn
    self.text = text
    self.pos = Posicion(-1, 0, -1, fn, text)
    self.char_actual = None
    self.avanzar()
  
  def avanzar(self):
    self.pos.avanzar(self.char_actual)
    self.char_actual = self.text[self.pos.indice] if self.pos.indice < len(self.text) else None

  def crear_tokens(self):
      
        # Aquí se toma un caracter de la linea, y dependiendo de su valor, es enviado a la
        # función encargada de continuar con el análisis de la palabra.
        # *Un valor no reconocido será tomado como error*
        
    tokens = []

    while self.char_actual != None:
      if self.char_actual in ' \t':
        self.avanzar()
      elif self.char_actual in DIGITOS:
        token,error= self.crear_numero()
        if error: return[], error
        tokens.append(token)
      elif self.char_actual in LETRAS:
        tokens.append(self.crear_identificador())
      elif self.char_actual == '"':
        tokens.append(self.crear_cadena())
      elif self.char_actual == '+':
        tokens.append(Token(TOK_SUMA, pos_inicio=self.pos))
        self.avanzar()
      elif self.char_actual == '-':
        tokens.append(Token(TOK_RESTA, pos_inicio=self.pos))
        self.avanzar()
      elif self.char_actual == '*':
        tokens.append(Token(TOK_MUL, pos_inicio=self.pos))
        self.avanzar()
      elif self.char_actual == '/':
        tokens.append(Token(TOK_DIV, pos_inicio=self.pos))
        self.avanzar()
      elif self.char_actual == '^':
        tokens.append(Token(TOK_ELV, pos_inicio=self.pos))
        self.avanzar()
      elif self.char_actual == '(':
        tokens.append(Token(TOK_PARENTIZQ, pos_inicio=self.pos))
        self.avanzar()
      elif self.char_actual == ')':
        tokens.append(Token(TT_RPAREN, pos_inicio=self.pos))
        self.avanzar()
      elif self.char_actual == '!':
        token, error = self.crear_desigualdad()
        if error: return [], error
        tokens.append(token)
      elif self.char_actual == '=':
        tokens.append(self.crear_igualdad())
      elif self.char_actual == '<':
        tokens.append(self.crear_menor_que())
      elif self.char_actual == '>':
        tokens.append(self.crear_mayor_que())
      else:
        pos_inicio = self.pos.copiar()
        char = self.char_actual
        self.avanzar()
        return [], Error(pos_inicio, self.pos, self.char,"'" + char + "'")

    tokens.append(Token(TOK_EOF, pos_inicio=self.pos))
    return tokens, None

  def crear_numero(self):
      
    ##########################################################################
    # Esta función se encarga de crear números, enteros o flotantes, a partir de
    # un valor númerico. Palabras que inicien por valores númericos en combinación
    # de letras serán tomadas como error.
    #############################################################################
    num_str = ''
    dot_count = 0
    pos_inicio = self.pos.copiar()

    while self.char_actual != None and self.char_actual in DIGITOS + '.':
      if self.char_actual == '.':
        if dot_count == 1: break
        dot_count += 1
      num_str += self.char_actual
      self.avanzar()

    if dot_count == 0:
      return Token(TOK_ENT, int(num_str), pos_inicio, self.pos), None
    else:
      return None, Error(pos_inicio, self.pos, num_str, "'" + self.char_actual + "'")
      
      
    #########################################################################
    # Esta función se encarga de contruir comentarios. Inicia con el caracter
    # '/', si este es seguido por '*' se empezará a crear un comentario; caso
    # contrario el valor se tomará como un operador.
    ##########################################################################
    
    def crear_comentario(self):

        comentario = self.char_actual
        bandera = False
        comentario_final = ''
        posInicio = self.pos.copiar()
        self.avanzar()

        if self.char_actual == '*':

            while bandera == False:
                if(comentario_final == '*') and (self.char_actual == '/'):
                    comentario += self.char_actual
                    self.avanzar()
                    bandera = True

                else:
                    comentario_final = self.char_actual
                    comentario += self.char_actual
                    self.avanzar()

            return Token(TOK_COMMENT, comentario, posInicio, self.pos)

        else:

            return Token(TOK_MUL, comentario, posInicio, self.pos)


    #########################################################################
    # Esta función se encarga de contruir cadenas. Inicia con el caracter
    # '"'.
    ##########################################################################

  def crear_cadena(self):
    string = ''
    pos_inicio = self.pos.copiar()
    escape = False
    self.avanzar()

    escapes = {
      'n': '\n',
      't': '\t'
    }

    while self.char_actual != None and (self.char_actual != '"' or escape):
      if escape:
        string += escapes.get(self.char_actual, self.char_actual)
      else:
        if self.char_actual == '\\':
          escape = True
        else:
          string += self.char_actual
      self.avanzar()
      escape = False
    
    self.avanzar()
    return Token(TOK_CADENA, string, pos_inicio, self.pos)

  def crear_identificador(self):
      
    ########################################################################
    # un tipo, una expresión o un identificador.
    # solo caracter. Adicionalmente valida si se trata de una declaración,
    # Esta función se encarga de contruir palabras a partir de un
    ########################################################################
    id_str = ''
    pos_inicio = self.pos.copiar()

    while self.char_actual != None and self.char_actual in LETRAS_DIGITOS + '_':
      id_str += self.char_actual
      self.avanzar()

    tok_type = TOK_RESERVADA if id_str in reservadas else TOK_IDENTIFICADOR
    return Token(tok_type, id_str, pos_inicio, self.pos)
    
    ##################################################################################
    # Estas funciones llevan a cabo el reconocimiento de operadores, además de contruir
    # aquellos formados por dos caracteres, tales como '<=', '==' o '&&'.
    # *Un signo de igual (=) solo, será definido como operador de asiganción*
    ##################################################################################

  def crear_desigualdad(self):
    pos_inicio = self.pos.copiar()
    self.avanzar()

    if self.char_actual == '=':
      self.avanzar()
      print("hola")
      return Token(TOK_DESIGUALDAD, pos_inicio=pos_inicio, pos_fin=self.pos), None

    self.avanzar()
    return None, Error(pos_inicio, self.pos, self.char_actual, "Error")
  
  def crear_igualdad(self):
    tok_type = TOK_ASIG
    pos_inicio = self.pos.copiar()
    self.avanzar()

    if self.char_actual == '=':
      self.avanzar()
      tok_type = TOK_IGUALDAD

    return Token(tok_type, pos_inicio=pos_inicio, pos_fin=self.pos)

  def crear_menor_que(self):
    tok_type = TOK_MENORQ
    pos_inicio = self.pos.copiar()
    self.avanzar()

    if self.char_actual == '=':
      self.avanzar()
      tok_type = TOK_MENORIG

    return Token(tok_type, pos_inicio=pos_inicio, pos_fin=self.pos)

  def crear_mayor_que(self):
    tok_type = TOK_MAYORQ
    pos_inicio = self.pos.copiar()
    self.avanzar()

    if self.char_actual == '=':
      self.avanzar()
      tok_type = TOK_MAYORIG

    return Token(tok_type, pos_inicio=pos_inicio, pos_fin=self.pos)

#######################################
# NODES
#######################################

class NodoNum:
  def __init__(self, tok):
    self.tok = tok

    self.pos_inicio = self.tok.pos_inicio
    self.pos_fin = self.tok.pos_fin

  def __repr__(self):
    return f'{self.tok}'

class NodoString:
  def __init__(self, tok):
    self.tok = tok

    self.pos_inicio = self.tok.pos_inicio
    self.pos_fin = self.tok.pos_fin

  def __repr__(self):
    return f'{self.tok}'

class NodoLista:
  def __init__(self, element_nodes, pos_inicio, pos_fin):
    self.element_nodes = element_nodes

    self.pos_inicio = pos_inicio
    self.pos_fin = pos_fin

class NodoVar:
  def __init__(self, nombre_var_tok):
    self.nombre_var_tok = nombre_var_tok

    self.pos_inicio = self.nombre_var_tok.pos_inicio
    self.pos_fin = self.nombre_var_tok.pos_fin

class NodoAsig:
  def __init__(self, nombre_var_tok, value_node):
    self.nombre_var_tok = nombre_var_tok
    self.value_node = value_node

    self.pos_inicio = self.nombre_var_tok.pos_inicio
    self.pos_fin = self.value_node.pos_fin

class NodoOpBin:
  def __init__(self, nodo_izq, op_tok, nodo_der):
    self.nodo_izq = nodo_izq
    self.op_tok = op_tok
    self.nodo_der = nodo_der

    self.pos_inicio = self.nodo_izq.pos_inicio
    self.pos_fin = self.nodo_der.pos_fin

  def __repr__(self):
    return f'({self.nodo_izq}, {self.op_tok}, {self.nodo_der})'

class NodoOpUn:
  def __init__(self, op_tok, node):
    self.op_tok = op_tok
    self.node = node

    self.pos_inicio = self.op_tok.pos_inicio
    self.pos_fin = node.pos_fin

  def __repr__(self):
    return f'({self.op_tok}, {self.node})'

class NodoSi:
  def __init__(self, casos, caso_mientras):
    self.casos = casos
    self.caso_mientras = caso_mientras

    self.pos_inicio = self.casos[0][0].pos_inicio
    self.pos_fin = (self.caso_mientras or self.casos[len(self.casos) - 1][0]).pos_fin

class NodoMientras:
  def __init__(self, nodo_condicion, nodo_cuerpo):
    self.nodo_condicion = nodo_condicion
    self.nodo_cuerpo = nodo_cuerpo

    self.pos_inicio = self.nodo_condicion.pos_inicio
    self.pos_fin = self.nodo_cuerpo.pos_fin

class NodoFuncion:
  def __init__(self, nombre_var_tok, nombres_tokens, nodo_cuerpo):
    self.nombre_var_tok = nombre_var_tok
    self.nombres_tokens = nombres_tokens
    self.nodo_cuerpo = nodo_cuerpo

    if self.nombre_var_tok:
      self.pos_inicio = self.nombre_var_tok.pos_inicio
    elif len(self.nombres_tokens) > 0:
      self.pos_inicio = self.nombres_tokens[0].pos_inicio
    else:
      self.pos_inicio = self.nodo_cuerpo.pos_inicio

    self.pos_fin = self.nodo_cuerpo.pos_fin

class NodoLlamada:
  def __init__(self, nodo_llamar, nodos):
    self.nodo_llamar = nodo_llamar
    self.nodos = nodos

    self.pos_inicio = self.nodo_llamar.pos_inicio

    if len(self.nodos) > 0:
      self.pos_fin = self.nodos[len(self.nodos) - 1].pos_fin
    else:
      self.pos_fin = self.nodo_llamar.pos_fin

#######################################
# PARSE RESULT
#######################################

class Resultado:
  def __init__(self):
    self.error = None
    self.node = None
    self.ult_avance_reg = 0
    self.avance = 0

  def registrar_avance(self):
    self.ult_avance_reg = 1
    self.avance += 1

  def registrar(self, res):
    self.ult_avance_reg = res.avance
    self.avance += res.avance
    if res.error: self.error = res.error
    return res.node

  def exito(self, node):
    self.node = node
    return self

  def fallo(self, error):
    if not self.error or self.ult_avance_reg == 0:
      self.error = error
    return self

#######################################
# La clase de analisis sintactico es la
# que explicitamente se encarga de clasificar
# cada elemento entrante de la linea en alguna
# de las funciones encargadas de realizar
# el análisis de los valores.
#######################################

class analizadorSintactico:
  def __init__(self, tokens):
    self.tokens = tokens
    self.tok_indice = -1
    self.avanzar()

  def avanzar(self, ):
    self.tok_indice += 1
    if self.tok_indice < len(self.tokens):
      self.tok_actual = self.tokens[self.tok_indice]
    return self.tok_actual

  def enlazar(self):
    res = self.expr()
    if not res.error and self.tok_actual.tipo != TOK_EOF:
      return res.fallo(Error(
        self.tok_actual.pos_inicio, self.tok_actual.pos_fin, self.tok_actual.tipo,
        "Error"
      ))
    return res

  ###################################

  def expr(self):
    res = Resultado()

    if self.tok_actual.iguales(TOK_RESERVADA, 'ent') or self.tok_actual.iguales(TOK_RESERVADA, 'cadena'):
      res.registrar_avance()
      self.avanzar()

      if self.tok_actual.tipo != TOK_IDENTIFICADOR:
        return res.fallo(Error(
          self.tok_actual.pos_inicio, self.tok_actual.pos_fin,
          "Error"
        ))

      var_name = self.tok_actual
      res.registrar_avance()
      self.avanzar()

      if self.tok_actual.tipo != TOK_ASIG:
        return res.fallo(Error(
          self.tok_actual.pos_inicio, self.tok_actual.pos_fin,self.tok_actual.tipo,
          "Esperaba '='"
        ))

      res.registrar_avance()
      self.avanzar()
      expr = res.registrar(self.expr())
      if res.error: return res
      return res.exito(NodoAsig(var_name, expr))

    node = res.registrar(self.op_bin(self.expr_comp, ((TOK_RESERVADA, '&&'), (TOK_RESERVADA, '||'))))

    if res.error:
      return res.fallo(Error(
        self.tok_actual.pos_inicio, self.tok_actual.pos_fin,self.tok_actual.tipo,
        "Error"
      ))

    return res.exito(node)

  def expr_comp(self):
    res = Resultado() 
    node = res.registrar(self.op_bin(self.expr_arit, (TOK_IGUALDAD, TOK_DESIGUALDAD, TOK_MENORQ, TOK_MAYORQ, TOK_MENORIG, TOK_MAYORIG)))
    
    if res.error:
      return res.fallo(Error(
        self.tok_actual.pos_inicio, self.tok_actual.pos_fin,self.tok_actual.tipo,
        "Error"
      ))

    return res.exito(node)

  def expr_arit(self):
    return self.op_bin(self.term, (TOK_SUMA, TOK_RESTA))

  def term(self):
    return self.op_bin(self.factor, (TOK_MUL, TOK_DIV))

  def factor(self):
    res = Resultado()
    tok = self.tok_actual

    if tok.tipo in (TOK_SUMA, TOK_RESTA):
      res.registrar_avance()
      self.avanzar()
      factor = res.registrar(self.factor())
      if res.error: return res
      return res.exito(NodoOpUn(tok, factor))

    return self.elv()

  def elv(self):
    return self.op_bin(self.llamada, (TOK_ELV, ), self.factor)

  def llamada(self):
    res = Resultado()
    atom = res.registrar(self.atom())
    if res.error: return res

    if self.tok_actual.tipo == TOK_PARENTIZQ:
      res.registrar_avance()
      self.avanzar()
      nodos = []

      if self.tok_actual.tipo == TOK_PARENTDER:
        res.registrar_avance()
        self.avanzar()
      else:
        nodos.append(res.registrar(self.expr()))
        if res.error:
          return res.fallo(Error(
            self.tok_actual.pos_inicio, self.tok_actual.pos_fin,self.tok_actual.tipo,
            "Error"
          ))

        while self.tok_actual.tipo == TOK_COMMA:
          res.registrar_avance()
          self.avanzar()

          nodos.append(res.registrar(self.expr()))
          if res.error: return res

        if self.tok_actual.tipo != TOK_PARENTDER:
          return res.fallo(Error(
            self.tok_actual.pos_inicio, self.tok_actual.pos_fin,self.tok_actual.tipo,
            "Error"
          ))

        res.registrar_avance()
        self.avanzar()
      return res.exito(NodoLlamada(atom, nodos))
    return res.exito(atom)

  def atom(self):
    res = Resultado()
    tok = self.tok_actual

    if tok.tipo in (TOK_ENT):
      res.registrar_avance()
      self.avanzar()
      return res.exito(NodoNum(tok))

    elif tok.tipo == TOK_CADENA:
      res.registrar_avance()
      self.avanzar()
      return res.exito(NodoString(tok))

    elif tok.tipo == TOK_IDENTIFICADOR:
      res.registrar_avance()
      self.avanzar()
      return res.exito(NodoVar(tok))

    elif tok.tipo == TOK_PARENTIZQ:
      res.registrar_avance()
      self.avanzar()
      expr = res.registrar(self.expr())
      if res.error: return res
      if self.tok_actual.tipo == TOK_PARENTDER:
        res.registrar_avance()
        self.avanzar()
        return res.exito(expr)
      else:
        return res.fallo(Error(
          self.tok_actual.pos_inicio, self.tok_actual.pos_fin,self.tok_actual.tipo,
          "Error"
        ))
    
    elif tok.iguales(TOK_RESERVADA, 'si'):
      expr_si = res.registrar(self.expr_si())
      if res.error: return res
      return res.exito(expr_si)

    elif tok.iguales(TOK_RESERVADA, 'mientras'):
      expr_mientras = res.registrar(self.expr_mientras())
      if res.error: return res
      return res.exito(expr_mientras)

    elif tok.iguales(TOK_RESERVADA, 'clase') or tok.iguales(TOK_RESERVADA, 'publico'):
      func_def = res.registrar(self.func_def())
      if res.error: return res
      return res.exito(func_def)

    return res.fallo(Error(
      tok.pos_inicio, tok.pos_fin, tok.tipo,
      "Error"
    ))

  def expr_lista(self):
    res = Resultado()
    element_nodes = []
    pos_inicio = self.tok_actual.pos_inicio.copiar()

    if self.tok_actual.tipo != TT_LSQUARE:
      return res.fallo(Error(
        self.tok_actual.pos_inicio, self.tok_actual.pos_fin,self.tok_actual.tipo,
        "Error"
      ))

    res.registrar_avance()
    self.avanzar()

    if self.tok_actual.tipo == TT_RSQUARE:
      res.registrar_avance()
      self.avanzar()
    else:
      element_nodes.append(res.registrar(self.expr()))
      if res.error:
        return res.fallo(Error(
          self.tok_actual.pos_inicio, self.tok_actual.pos_fin,self.tok_actual.tipo,
          "Error"
        ))

      while self.tok_actual.tipo == TOK_COMMA:
        res.registrar_avance()
        self.avanzar()

        element_nodes.append(res.registrar(self.expr()))
        if res.error: return res

      if self.tok_actual.tipo != TT_RSQUARE:
        return res.fallo(InvalidSyntaxError(
          self.tok_actual.pos_inicio, self.tok_actual.pos_fin,tok.tipo,
          "Error"
        ))

      res.registrar_avance()
      self.avanzar()

    return res.exito(NodoLista(
      element_nodes,
      pos_inicio,
      self.tok_actual.pos_fin.copiar()
    ))

  def expr_si(self):
    res = Resultado()
    casos = []
    caso_mientras = None

    if not self.tok_actual.iguales(TOK_RESERVADA, 'si'):
      return res.fallo(Error(
        self.tok_actual.pos_inicio, self.tok_actual.pos_fin,
        "Error"
      ))

    res.registrar_avance()
    self.avanzar()
    
    condicion = res.registrar(self.expr())
    if res.error: return res

    expr = res.registrar(self.expr())
    if res.error: return res
    casos.append((condicion, expr))



    if self.tok_actual.iguales(TOK_RESERVADA, 'entonces'):
      res.registrar_avance()
      self.avanzar()

      caso_mientras = res.registrar(self.expr())
      if res.error: return res

    return res.exito(NodoSi(casos, caso_mientras))


  def expr_mientras(self):
    res = Resultado()

    if not self.tok_actual.iguales(TOK_RESERVADA, 'mientras'):
      return res.fallo(Error(
        self.tok_actual.pos_inicio, self.tok_actual.pos_fin,
        "Error"
      ))

    res.registrar_avance()
    self.avanzar()
    condicion = res.registrar(self.expr())
    if res.error: return res
    res.registrar_avance()
    self.avanzar()
    cuerpo = res.registrar(self.expr())
    if res.error: return res

    return res.exito(NodoMientras(condicion, cuerpo))

  def func_def(self):
    res = Resultado()

    if not (self.tok_actual.iguales(TOK_RESERVADA, 'clase') or self.tok_actual.iguales(TOK_RESERVADA, 'publico')) :
      return res.fallo(Error(
        self.tok_actual.pos_inicio, self.tok_actual.pos_fin,
        "Error"
      ))

    res.registrar_avance()
    self.avanzar()

    if self.tok_actual.tipo == TOK_IDENTIFICADOR:
      nombre_var_tok = self.tok_actual
      res.registrar_avance()
      self.avanzar()
      if self.tok_actual.tipo != TOK_PARENTIZQ:
        return res.fallo(Error(
          self.tok_actual.pos_inicio, self.tok_actual.pos_fin,
          "Error"
        ))
    else:
      nombre_var_tok = None
      if self.tok_actual.tipo != TOK_PARENTIZQ:
        return res.fallo(Error(
          self.tok_actual.pos_inicio, self.tok_actual.pos_fin,
          "Error"
        ))
    
    res.registrar_avance()
    self.avanzar()
    nombres_tokens = []

    if self.tok_actual.tipo == TOK_IDENTIFICADOR:
      nombres_tokens.append(self.tok_actual)
      res.registrar_avance()
      self.avanzar()
      
      while self.tok_actual.tipo == TOK_COMMA:
        res.registrar_avance()
        self.avanzar()

        if self.tok_actual.tipo != TOK_IDENTIFICADOR:
          return res.fallo(Error(
            self.tok_actual.pos_inicio, self.tok_actual.pos_fin,
            "Error"
          ))

        nombres_tokens.append(self.tok_actual)
        res.registrar_avance()
        self.avanzar()
      
      if self.tok_actual.tipo != TOK_PARENTDER:
        return res.fallo(Error(
          self.tok_actual.pos_inicio, self.tok_actual.pos_fin,
          "Error"
        ))
    else:
      if self.tok_actual.tipo != TOK_PARENTDER:
        return res.fallo(Error(
          self.tok_actual.pos_inicio, self.tok_actual.pos_fin,
          "Error"
        ))

    res.registrar_avance()
    self.avanzar()

    nodo_a_retornar = res.registrar(self.expr())
    if res.error: return res

    return res.exito(NodoFuncion(
      nombre_var_tok,
      nombres_tokens,
      nodo_a_retornar
    ))

  ###################################

  def op_bin(self, func_a, ops, func_b=None):
    if func_b == None:
      func_b = func_a
    
    res = Resultado()
    izq = res.registrar(func_a())
    if res.error: return res

    while self.tok_actual.tipo in ops or (self.tok_actual.tipo, self.tok_actual.valor) in ops:
      op_tok = self.tok_actual
      res.registrar_avance()
      self.avanzar()
      der = res.registrar(func_b())
      if res.error: return res
      izq = NodoOpBin(izq, op_tok, der)

    return res.exito(izq)
    
    
###########################################
# Función que inicia el flujo del programa
###########################################
    
def run(fn, texto,linea):
  global NUM_LINEA
  NUM_LINEA = linea
  # Generar lostokens
  lexer = analizadorLexico(fn, texto)
  tokens, error = lexer.crear_tokens()
  if error: return None, error
  
  # Generar el AST
  parser = analizadorSintactico(tokens)
  ast = parser.enlazar()
  if ast.error: return None, ast.error

  return ast.node, ast.error

