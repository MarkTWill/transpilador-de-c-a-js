import jsbeautifier
import re
import tkinter as tk
from tkinter import scrolledtext

root = tk.Tk()
root.title("Resultados del Analizador")

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=30, bg='black', fg='white')
text_area.pack()

def mostrar_resultados(resultados):
    text_area.delete(1.0, tk.END)  # Limpiar el contenido actual
    text_area.insert(tk.INSERT, resultados)


from ply import lex, yacc

tokens = (
    'SUMA', 'RESTA', 'MULTIPLICACION', 'DIVISION','INT', 'FLOAT', 'CHAR', 'DOUBLE', 'BOOLEAN', 'LONG',
    'STRING', 'IF', 'ELSE', 'WHILE', 'DO', 'FOR', 'RETURN', 'COMA', 'PRINT', 'MAIN', 'VOID',
    'PARENTESIS_IZQ', 'PARENTESIS_DER', 'CORCHETE_IZQ', 'CORCHETE_DER',
    'ASIGNACION', 'MENOR_IGUAL', 'MAYOR_IGUAL', 'IGUAL', 'DISTINTO','MENOR', 'MAYOR',
    'AND', 'OR', 'NOT',
    'ID', 'NUMERO', 'CADENA', 'COUT',
    'PUNTO_Y_COMA', 'LLAVE_IZQ', 'LLAVE_DER', 'DEST', 
)

tokens += (
    'CLASS', 'PUBLIC', 'PRIVATE', 'PROTECTED', 'COLON', 'USING', 'NAMESPACE', 'INCLUDE', 'NUMERAL', 
)

reservado ={'if': 'IF' ,'public': 'PUBLIC' ,'private': 'PRIVATE' ,'protected': 'PROTECTED','class': 'CLASS','else': 'ELSE', 'while': 'WHILE','main':'MAIN',
           'do': 'DO','for': 'FOR', 'return': 'RETURN','break':'BREAK', 'void':'VOID', 'cout': 'COUT', 
           'using': 'USING' ,'namespace': 'NAMESPACE','include': 'INCLUDE'}

t_NAMESPACE = r'NAMESPACE'
t_INCLUDE = r'INCLUDE'
t_CLASS = r'class'
t_PUBLIC = r'public'
t_PRIVATE = r'private'
t_PROTECTED = r'protected'
t_COLON = r':'
t_DEST = r'~'
t_USING = r'using'
t_NUMERAL= r'\#'

t_COUT = r'cout'
t_PRINT= r'<<'
t_COMA = r','
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'
t_ASIGNACION = r'='
t_MENOR = r'<'
t_MAYOR = r'>'
t_MENOR_IGUAL = r'<='
t_MAYOR_IGUAL = r'>='
t_IGUAL = r'=='
t_DISTINTO = r'!='
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_NUMERO = r'\d+'
t_CADENA = r'\"([^\\\n]|(\\.))*?\"'
t_PUNTO_Y_COMA = r';'

t_ignore = ' \t\n'

def t_MAIN(t):
    r'main'
    return t

def t_VOID(t):
    r'void'
    return t

def t_INT(t):
    r'int'
    return t

def t_FLOAT(t):
    r'float'
    return t

def t_CHAR(t):
    r'char'
    return t

def t_DOUBLE(t):
    r'double'
    return t

def t_BOOLEAN(t):
    r'boolean'
    return t

def t_STRING(t):
    r'string'
    return t

def t_LONG(t):
    r'long'
    return t

def t_IF(t):
    r'if'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_DO(t):
    r'do'
    return t

def t_FOR(t):
    r'for'
    return t

def t_RETURN(t):
    r'return'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservado.get(t.value, 'ID')  
    return t

def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

precedence = (
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULTIPLICACION', 'DIVISION'),
)

js_code = ""
def p_program(p):
    '''program : class_declaration program
               | function_declaration program
               | main_function program
               | vacio
    '''
    global js_code
    js_code += ""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + p[2]
    js_code=p[0]

def p_class_declaration(p):
    '''class_declaration : CLASS ID LLAVE_IZQ class_body LLAVE_DER PUNTO_Y_COMA'''
    p[0] = f'class {p[2]}' + ' {\n' + p[4] + '}\n'

def p_class_body(p):
    '''class_body : class_member
                  | class_body class_member'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + p[2]
    temp=p[0]
    nuev = re.sub(r'^.*?constructor\(\)\s*{', 'constructor() {', p[0], flags=re.DOTALL)
    nuevof = re.sub(r'\bfunction\b', '', nuev)
    p[0]=nuevof

def p_class_member(p):
    '''class_member : access_specifier COLON class_member
                    | assignment_statement class_member
                    | function_declaration class_member
                    | constructor_declaration class_member
                    | destructor_declaration class_member
                    | vacio
    '''
    if len(p) == 4 and p[1] is not None:
        p[0] = "" + p[3]
    elif len(p) == 3 and p[2] is not None:
        if p[1] == "function_declaration" or p[1] == "constructor_declaration":
            p[0] = p[2] + p[3]
        else:
            p[0] = p[1] + p[2]
    else:
        p[0] = ''


def p_access_specifier(p):
    '''access_specifier : PUBLIC
                       | PRIVATE
                       | PROTECTED'''
    p[0]=''

def p_constructor_declaration(p):
    '''constructor_declaration : ID PARENTESIS_IZQ argument_list PARENTESIS_DER  LLAVE_IZQ statement_list LLAVE_DER'''
    variables = ', '.join([f'this.{var.strip()}' if not var.strip().startswith('this.') else var.strip() for var in p[6].split(',')])
    p[0] = f'constructor({p[3]})' + ' {\n' + f'  {variables}\n' + '}\n'


def p_destructor_declaration(p):
    '''destructor_declaration : DEST ID PARENTESIS_IZQ argument_list PARENTESIS_DER PUNTO_Y_COMA'''
    p[0] = ''
  
def p_main_function(p):
    '''main_function : INT MAIN PARENTESIS_IZQ PARENTESIS_DER LLAVE_IZQ statement_list LLAVE_DER'''
    p[0]= 'function main() {\n' + p[6] + '}\nmain();\n'
    
def p_function_declaration(p):
    '''function_declaration : variable ID PARENTESIS_IZQ argument_list PARENTESIS_DER LLAVE_IZQ statement_list LLAVE_DER
                            | NUMERAL INCLUDE MENOR ID MAYOR
                            | USING NAMESPACE ID PUNTO_Y_COMA'''
    if len(p) == 6 or len(p) == 5:
        p[0] = ' '
    else:
        p[0]= f'function {p[2]}({p[4]})' + ' {\n' + p[7] + '}\n'

def p_statement_list(p):
    '''statement_list : statement
        | statement_list statement
    '''
    if len(p) == 2:
        p[0] = p[1] if p[1] is not None else ""
    elif len(p) == 3:
        p[0] = p[1] + (p[2] if p[2] is not None else "")
    else:
        p[0] = ""

def p_statement(p):
    '''statement : assignment_statement 
        | expression_statement
        | if
        | while
        | do_while
        | for
        | return
        | function_call PUNTO_Y_COMA
    '''
    p[0] = p[1] if len(p) == 2 else p[1]+p[2]


def p_if_statement(p):
    '''if : IF PARENTESIS_IZQ expression PARENTESIS_DER LLAVE_IZQ statement_list LLAVE_DER
        | IF PARENTESIS_IZQ expression PARENTESIS_DER LLAVE_IZQ statement_list LLAVE_DER ELSE LLAVE_IZQ statement_list LLAVE_DER
    '''
    if len(p) == 8:
        p[0] = f'if ({p[3]})' + ' {\n' + p[6] + '}\n'
    elif len(p) == 11:
        p[0] = f'if ({p[3]})' + ' {\n' + p[6] + '} else {\n' + p[9] + '}\n'

def p_while_statement(p):
    '''while : WHILE PARENTESIS_IZQ expression PARENTESIS_DER LLAVE_IZQ statement_list LLAVE_DER'''
    p[0] = f'while ({p[3]})' + ' {\n' + p[6] + '}\n'

def p_do_while_statement(p):
    '''do_while : DO LLAVE_IZQ statement_list LLAVE_DER WHILE PARENTESIS_IZQ expression PARENTESIS_DER PUNTO_Y_COMA'''
    p[0] = f'do {{\n{p[3]}\n}} while ({p[8]});\n'

def p_for_statement(p):
    '''for : FOR PARENTESIS_IZQ variable ID ASIGNACION expression PUNTO_Y_COMA expression PUNTO_Y_COMA expression PARENTESIS_DER LLAVE_IZQ statement_list LLAVE_DER'''
    
    p[0] = f'for ({p[3]} {p[4]} {p[5]} {p[6]}; {p[8]}; {p[10]})' + ' {\n' + p[13] + '}\n'

def p_return_statement(p):
    '''return : RETURN expression PUNTO_Y_COMA'''
    p[0] = f'return {p[2]};\n'


def p_function_call(p):
    '''function_call : ID PARENTESIS_IZQ argument_list PARENTESIS_DER'''
    p[0] = f'{p[1]}({p[3]})'

def p_argument_fun(p):
    '''argument_fun : NUMERO COMA argument_fun
                    | ID COMA argument_fun
                    | vacio
                    '''
    p[0] = f'{p[1]}, {p[3]}'

def p_argument_list(p):
    '''argument_list : expression
        | expression COMA argument_list
        | variable expression
        | variable expression COMA argument_list
        | vacio 
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = f'{p[2]}'
    elif len(p) == 4:
        p[0] = f'{p[1]}, {p[3]}'
    elif len(p) == 5:
        p[0] = f'{p[2]}, {p[4]}'

def p_assignment_statement(p):
    '''assignment_statement : variable ID PUNTO_Y_COMA
        | variable ID ASIGNACION expression PUNTO_Y_COMA
        | variable ID CORCHETE_IZQ expression CORCHETE_DER ASIGNACION LLAVE_IZQ argument_list LLAVE_DER PUNTO_Y_COMA
        | ID ASIGNACION expression PUNTO_Y_COMA
    '''
    if len(p) == 4:
        p[0] = f'{p[1]} {p[2]};'
    elif len(p) == 6:
        p[0] = f'{p[1]} {p[2]} = {p[4]};'
    elif len(p) == 11:
        p[0] = f'{p[1]} {p[2]} = [{p[8]}];'
    elif len(p) == 5:
        p[0] = f'{p[1]} = {p[3]};'

def p_variable(p):
    '''variable : INT
        | FLOAT 
        | CHAR 
        | DOUBLE 
        | BOOLEAN 
        | LONG 
        | STRING 
        | VOID
    '''
    p[0] = 'let'

def p_expression_statement(p):
    '''expression_statement : expression PUNTO_Y_COMA
                            | COUT PRINT expression PUNTO_Y_COMA'''
    if len(p) == 3:
        p[0] = f'{p[1]};'
    elif len(p) == 5:
        p[0]= f'console.log({p[3]});'

def p_expression(p):
    '''expression : expression SUMA expression
        | expression RESTA expression
        | expression MULTIPLICACION expression
        | expression DIVISION expression
        | expression MENOR_IGUAL expression
        | expression MAYOR_IGUAL expression
        | expression IGUAL expression
        | expression DISTINTO expression
        | expression AND expression
        | expression OR expression
        | NOT expression
        | PARENTESIS_IZQ expression PARENTESIS_DER
        | LLAVE_IZQ expression LLAVE_DER  
        | NUMERO 
        | CADENA
        | expression PRINT expression 
        | COUT PRINT expression 
        | expression MENOR expression 
        | expression MAYOR expression
        | expression SUMA SUMA
        | ID
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        if p[1] == 'COUT':
            p[0] = f'console.log({p[1]}, {p[3]})'
        else:
            p[0] = f'{p[1]}{p[2]}{p[3]}'
    elif len(p) == 5 and p[1] == 'expression' and p[2] == 'PARENTESIS_IZQ':
        p[0] = f'({p[2]})'
    elif len(p) == 4 and p[1] == 'expression' and p[2] == 'LLAVE_IZQ':
        p[0] = f'{{{p[3]}}}'
    elif len(p) == 2 and p[1].isdigit():
        p[0] = f'{p[1]}'
    elif len(p) == 2 and p[1][0] == '"' and p[1][-1] == '"':
        p[0] = p[1]  # Literal de cadena
    elif len(p) == 4 and p[1] == 'expression' and p[2] == 'PRINT':
        p[0] = f'console.log({p[3]})'
    elif len(p) == 4:
        p[0] = f'{p[1]}{p[3]}'  # Expresiones binarias
    elif len(p) == 3:
        p[0] = f'{p[1]}{p[2]}'

def p_vacio(p):
    '''vacio : '''
    p[0] = ""

def p_error(p):
    cad="ENTRADA:\n\n",entrada_aux, " \n\nError de sintaxis (La sintaxis no es valida)\n", p
    mostrar_resultados(cad)
    global accion
    accion = True 
    print('La sintaxis no es valida: ', p)

def traducir_argument_list(p):
    resultado = ""
    for item in p:
        resultado += traducir(item)
    return resultado

def traducir_variable(p):
    if isinstance(p, tuple) and len(p) > 0:
        tipo_variable = p[0]
        # Cambiar a "let" o "var" según el tipo de variable en Mark
        return "let" if tipo_variable != "VOID" else ""
    else:
        return ""

def traducir(p):
    if isinstance(p, tuple):
        return traducir(p[0])
    elif isinstance(p, list):
        return ''.join([traducir(item) for item in p])
    elif isinstance(p, str):
        return p
    else:
        return ""

def analizador(entrada):
    global entrada_aux
    entrada_aux = entrada 
    parser.parse(entrada, lexer=lexer)
    if not accion:
        cad="ENTRADA:\n\n",entrada, " \n\nLa entrada es sintácticamente válida"
        mostrar_resultados(cad)
        #js_code = jsbeautifier.beautify(js_code)  # Formatear el código JS
        #with open("salida.js", "w") as file:
        #    file.write(js_code)
        #root.mainloop()


parser = yacc.yacc()
accion=False

def leer(codigo_fuente):
    with open(codigo_fuente, 'r') as file:
        entrada = file.read()
    analizador(entrada)

codigo = 'ejemplo2.cpp'
leer(codigo)
if not accion:
    js_code = jsbeautifier.beautify(js_code)
    print(js_code)
    with open("salida.js", "w") as file:
                file.write(js_code)

root.mainloop()
