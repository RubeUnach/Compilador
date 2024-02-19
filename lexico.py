import ply.lex as lex

class Lexico():
    
    linea = 1
    resultadoLexema = []
    valor = " "
    tipo = " "
    
    reservados = (
        'FOR','DO','WHILE',
        'IF','ELSE','SWITCH',
        'CASE','BREAK','RETURN',
        'STATIC','PRINT'
        'PUBLIC','PRIVATE',
    )
    tipoDato = (
        'STRING','INT',
        'FLOAT','VOID','CHAR',
    )
    operadoresAritmeticos = ('MAS','MENOS','MULT','DIV','ASIG','MODULO')
    operadoresID = ('INCREMENTO','DECREMENTO')
    operadoresLogicos = ('IGUALACION','DIFERENCIA','MAYOR','MENOR','MAYOROIGUAL','MENOROIGUAL','AND','OR') 
    delimitadores = ('IPAREN','RPAREN','ICORCH','RCORCH','ILLAVE','RLLAVE',)
    tokens = ('IDENTIFICADOR','ENTERO','DECIMAL','CADENA','FIN','PUNTO',) 
    tokens = tokens + reservados + tipoDato+ operadoresAritmeticos + operadoresID + operadoresLogicos + delimitadores
    #OPERADORES ARITMETICOS
    t_MAS =r'\+'
    t_MENOS=r'-'
    t_MULT=r'\*'
    t_DIV=r'/'
    t_ASIG=r'='
    t_MODULO=r'%'
    #ARITMETICOS DE INCREMENTO Y DECREMENTO 
    t_INCREMENTO=r'\+\+'
    t_DECREMENTO=r'--'
    #ARITMETICOS LOGICOS
    t_IGUALACION=r'=='
    t_DIFERENCIA=r'!='
    t_MAYOR=r'>'
    t_MENOR=r'<'
    t_MAYOROIGUAL=r'>='
    t_MENOROIGUAL=r'<='
    t_AND=r'&&'
    t_OR=r'\|\|'   
    #OPERADOR DE ACCESO
    t_PUNTO=r'\.' 
    #DELIMITADORES
    t_IPAREN=r'\('
    t_RPAREN=r'\)'
    t_ICORCH=r'\['
    t_RCORCH=r'\]'
    t_ILLAVE=r'\{'
    t_RLLAVE=r'\}'

        
    def t_FIN(self,t):
        r';'
        self.valor = "PUNTO Y COMA"
        self.tipo = "TERMINO DE EXPRESION"
        return t

    def t_IDENTIFICADOR(self,t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        if t.value.upper() in self.reservados:
            self.tipo = "RESERVADA"
            self.valor = t.value.upper()
        elif t.value.upper() in self.tipoDato:
            self.tipo = "TIPO DE DATO"
            self.valor = t.value
        else:
            self.tipo = "IDENTIFICADOR"
            self.valor = t.value
        return t
    
    def t_DECIMAL(self,t):
        r'\d+\.\d+'
        try: 
            t.value = float(t.value)
            self.valor = "DECIMAL"
            self.tipo = "VALOR"
        except ValueError:
            self.valor = "INVALIDO"
        return t

    def t_ENTERO(self,t):
        r'\d+'
        try: 
            t.value = int(t.value)
            self.valor = "ENTERO"
            self.tipo = "VALOR"
        except ValueError:
            self.valor = "VALOR NO VALIDO"
        return t

    def t_CADENA(self,t):
        r'(\".*?\")'
        t.value = t.value[1:-1] #removemos comillas
        #Agregar todas las acciones como tap,saltos y mas
        t.value = t.value.replace('\\t','\t')
        t.value = t.value.replace('\\n','\n')
        t.value = t.value.replace('\\"','\"')
        t.value = t.value.replace("\\'","\'")
        t.value = t.value.replace('\\\\','\\')
        self.valor = "CADENA"
        self.tipo = "VALOR"
        return t
    
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_ignore  = ' \t'

    def t_error(self,t):
        estado = {
            "identificador": "INVALIDO",
            "lexema": str(t.value),
            "linea": str(self.linea)
        }
        cadena = str(t.value)
        valor = len(cadena)
        t.lexer.skip(valor)
        self.resultadoLexema.append(estado)

    def test(self,data):
        self.lexer = lex.lex(self)
        datosAux =  data.split("\n")
        for aux1 in datosAux:
            aux2 =  aux1.split(" ")
            for dato in aux2:
                self.lexer.input(dato)
                while True:
                    tok = self.lexer.token()
                    if not tok:
                        break
                    if self.valor == " ": 
                        self.identificarToken(str(tok.value))
                    estado = {
                        "identificador": self.valor,
                        "token": str(tok.value),
                        "tipo": self.tipo,
                        "linea": str(self.linea)
                    }
                    self.resultadoLexema.append(estado)
                    self.valor=" "
            self.linea += 1
        return self.resultadoLexema
        
    def identificarToken(self, token):
        if token == "(":
            self.valor = "PARERNTICIS DE APERTURA"
            self.tipo = "DELIMITADOR"
        elif token == ")":
            self.valor = "PARENTECIS DE CIERRE"
            self.tipo = "DELIMITADOR"
        elif token == "{":
            self.valor = "CORCHETE DE APERTURA"
            self.tipo = "DELIMITADOR"
        elif token == "}":
            self.valor = "CORCHETE DE CIERRE"
            self.tipo = "DELIMITADOR"
        elif token == "[":
            self.valor = "LLAVE DE APERTURA"
            self.tipo = "DELIMITADOR"
        elif token == "]":
            self.valor = "LLAVE DE CIERRE"
            self.tipo = "DELIMITADOR"
        elif token == "+":
            self.valor = "MAS"
            self.tipo = "OPERADOR ARITMETICO"
        elif token == "-":
            self.valor = "MENOS"
            self.tipo = "OPERADOR ARITMETICO"
        elif token == "*":
            self.valor = "MULTIPLICACION"
            self.tipo = "OPERADOR ARITMETICO"
        elif token == "/":
            self.valor = "DIVICION"
            self.tipo = "OPERADOR ARITMETICO"
        elif token == "=":
            self.valor = "IGUAL"
            self.tipo = "OPERADOR DE ASIGNACION"
        elif token == "++":
            self.valor = "MAS MAS"
            self.tipo = "OPERADOR INCREMENTAL"
        elif token == "--":
            self.valor = "MENOS MENOS"
            self.tipo = "OPERADOR DECREMENTAL"
        elif token == "==":
            self.valor = "IGUALACION"
            self.tipo = "OPERADOR LOGICO"
        elif token == "!=":
            self.valor = "NEGACION"
            self.tipo = "OPERADOR LOGICO"
        elif token == ">":
            self.valor = "MAYOR"
            self.tipo = "OPERADOR LOGICO"
        elif token == "<":
            self.valor = "MENOR"
            self.tipo = "OPERADOR LOGICO"
        elif token == ">=":
            self.valor = "MAYOR O IGUAL"
            self.tipo = "OPERADOR LOGICO"
        elif token == "<=":
            self.valor = "MENOR O IGUAL"
            self.tipo = "OPERADOR LOGICO"
        elif token == "||":
            self.valor = "OR"
            self.tipo = "OPERADOR LOGICO"
        elif token == "&&":
            self.valor = "AND"
            self.tipo = "OPERADOR LOGICO"
        elif token == ".":
            self.valor = "PUNTO"
            self.tipo = "OPERADOR DE ACCESO"
        
        
    def borrar(self):
        self.resultadoLexema.clear()