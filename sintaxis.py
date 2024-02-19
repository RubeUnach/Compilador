from lexico import *
import ply.yacc as yacc


lex = Lexico()
t = lex.rlexema 
    
precedence = (
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO'),
    ('right','UMENOS'),
    )

def p_expresion_declarar():
    'expresion : expresion MAS expresion'
    #   ^            ^      ^    ^
    #  t[0]         t[1]   t[2] t[3]
    print("t[0] => ",t[0])
    print("t[1] => ",t[0])
    print("t[3] => ",t[0])
    t[0] = t[1] + t[3]
    