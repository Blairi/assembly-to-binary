import tkinter as tk
from tkinter import filedialog

# variable para guardar la ubicación del archivo
INPUT_FILE = "./asm.asm"

# lista con los nombres de los registros
# en orden
REG_CODES = [
    "areg",
    "breg",
    "creg",
    "dreg",
    "ereg",
    "freg",
    "greg",
    "hreg",
    "ireg",
    "jreg",
]

# diccionario para guardar la linea donde
# se encuentra la etiqueta
LABELS = {}

# diccionario para guardar la ultima linea 
# donde se uso el registro
DIR_REG = {
    "areg": -1,
    "breg": -1,
    "creg": -1,
    "dreg": -1,
    "ereg": -1,
    "freg": -1,
    "greg": -1,
    "hreg": -1,
    "ireg": -1,
    "jreg": -1,
}

# lista con las operaciones en orden
OP_CODES = [
    "add",
    "sub",
    "mul",
    "div",
    "cmp",
    "and",
    "or",
    "not",
    "xor",
    "shl",
    "shr",
    "rol",
    "ror",
    "test",
    "read",
    "write",
    "move",
]

# diccionario con las operaciones 
# de salto de linea con la conversion
# a binario
JM_CODES = {
    "jmp": "10001",
    "je": "10010",
    "jne": "10011",
    "ja": "10100",
    "jae": "10101",
    "jb": "10110",
    "jbe": "10111",
    "jcd": "11000",
}


def read_file(name) -> list[str]:

    # recuperar todo el contenido del archivo
    cont = []
    with open(name, "r") as file:
        file.seek(0)
        cont = file.readlines()
    
    # guardar todas las lineas en una lista
    # quitando los saltos de linea
    lines = []
    for line in cont:
        if not line == "\n":
            lines.append(line)
    
    return lines
    

def binary_converter(n:int, bits:int):
    # string para guardar el binario
    binary_representation = ""

    # copiar el numero entero a un aux
    aux = n

    # dividimos el numero entre 2
    # y concatenamos el residuo de / 2
    # mientras sea mayor a 0
    while aux > 0:
        binary_representation += str(aux % 2)
        aux //= 2
    
    # rellenar con 0s el string en caso
    # de que en la conversion se necesiten
    # mas bits
    if len(binary_representation) < bits:
        for _ in range(0, bits - len(binary_representation)):
            binary_representation += "0"

    # retornamos la cadena en binario
    # volteada
    return binary_representation[::-1]


def op_instruction(instruction:str, line:int) -> str:

    # limpiar instrucción
    instruction = instruction.replace("\n", "")

    # separando por espacios la instruccion
    entities = instruction.split(" ")

    # buscar el indice de la operacion
    op = OP_CODES.index(entities[0])

    # convertir el indice de la operacion a
    # binario de 5 bits
    bin = binary_converter(op, 5)

    # iteramos el resto de registros u operaciones
    # quitando la primer operacion
    for entity in entities[1:]:

        # quitando las comas
        entity = entity.replace(",", "")

        # si lo que esta despues de la operacion...

        # es un registro
        if entity in REG_CODES:
            # guardamos la ultima linea donde se uso
            # el archivo
            DIR_REG[entity] = line

            # buscamos el indice del registro
            # para despues convertirlo a binario
            reg = REG_CODES.index(entity)
            bin += " "
            bin += binary_converter(reg, 4)

        # es una operacion de lectura/escritura
        # con un registro
        elif "[" in entity:

            # limpiando el registro
            entity = entity.replace("[", "")
            entity = entity.replace("]", "")

            # guardamos la ultima linea donde 
            # el registro se uso
            DIR_REG[entity] = line

            # recuperamos la ultima linea donde se uso
            # el registro para convertirla a binario
            dir = binary_converter(DIR_REG[entity], 4)
            bin += " "
            bin += dir
        
        # es una asignacion con valor inmediato
        elif entity[0] == "#":
            bin += " "
            # convertimos a binario quitandole 
            # el simbolo "gato"
            bin += binary_converter(int(entity[1:]), 8)

    # retornamos la instruccion convertida a binario
    return bin


def jm_instruction(instruction:str) -> str:
    # limpiamos la instruccion
    instruction = instruction.replace("\n", "")

    # separamos por espacios
    entities = instruction.split(" ")

    # recuperamos el binario de la operacion
    # de salto del diccionario
    bin = JM_CODES[entities[0]]

    # si la instruccion tiene mas de 2
    # "entidades", ej: jbe 10111, hreg
    if len(entities) > 2:

        bin += " "
        # quitando comas
        label = entities[1].replace("," ,"")

        # recuperamos la linea donde se encuentra
        # declarada la etiqueta y la convertimos
        # a binario
        bin += binary_converter(LABELS[label], 8)

        bin += " "

        # recuperamos el indice del registro que
        # se usa para convertirlo a binario
        reg = REG_CODES.index(entities[2])
        bin += binary_converter(reg, 8)

    # si la instruccion tiene solo 2
    # "entidades", ej: jbe 10111
    else:
        bin += " "
        # solo recuperamos la linea de la etiqueta
        # para convertirla a binario
        label = entities[1]
        bin += binary_converter(LABELS[label], 8)
    
    return bin
        

def search_labels(file) -> None:
    lines = read_file(file)

    # indice de la linea
    i = 1

    # recorremos cada linea buscando una 
    # etiqueta
    for line in lines:

        entity = line.split(" ")[0]
        entity = entity.replace("\n", "")

        # si ej -> etiq:
        if entity[-1] == ":":
            # print(f"{i}: {entity}")

            # guardamos la linea en donde
            # esta la etiqueta
            LABELS[entity[:-1]] = i
        
        # aumentamos el numero de linea
        i+=1


def conversor(file) -> list[str]:
    
    # declaramos una lista que es donde se van
    # a guardar todas las instrucciones en binario
    ans = []

    # buscamos las etiquetas
    search_labels(file)

    # leemos de nuevo el archivo
    lines = read_file(file)

    # string para guardar el binario
    out = ""

    # indice de la linea actual
    i = 1

    # leemos cada linea del archivo
    for line in lines:

        # separamos la instruccion por espacios
        # para recuperar la primer "entidad"
        entity = line.split(" ")[0]

        # quitando saltos de linea
        entity = entity.replace("\n", "")
    
        # print(entity)

        # string para guardar la 
        # instruccion
        ins = ""

        # si la operacion no es una de
        # salto de linea
        if entity in OP_CODES:

            # convertimos la operacion a binario
            # y la concatenamos
            ins = op_instruction(line, i)
            # print(f"{i}: {ins}")
            out += ins
        
        # si la operacion es de salto de linea
        elif entity in JM_CODES:
            # convertimos a binario y concatenamos
            ins = jm_instruction(line)
            # print(f"{i}: {ins}")
            out += ins

        # vamos aumentando el indice de la linea actual
        i += 1

        # quitamos espacios en blanco
        ins = ins.replace(" ", "")

        # declaramos un string auxiliar para
        # rellenarlo con 0
        padding = ""

        # rellenamos con n 0s si la instruccion 
        # aún no es de 24 bits
        if len(ins) < 24 and not entity[-1] == ":":
            for _ in range(0, 24 - len(ins) ):
                padding += "0"

            # contatenamos a los 0s nuestra instruccion
            padding += ins

            # guardamos la isntruccion completa
            # en la lista a retornar
            ans.append(padding)

    return ans


win = tk.Tk()
txt_orig = tk.Text(win, wrap=tk.WORD, width=40, height=10)
txt_out = tk.Text(win, wrap=tk.WORD, width=40, height=10)
def open_file():
    INPUT_FILE = filedialog.askopenfilename()
    if INPUT_FILE:
        cont = read_file(INPUT_FILE)
        for line in cont:
            txt_orig.insert(tk.END, line)


def conv_file():
    out = conversor(INPUT_FILE)
    for line in out:
        txt_out.insert(tk.END, "\n")
        txt_out.insert(tk.END, line)


def window() -> None:
    
    win.title("Assembly to binary")

    btn_open = tk.Button(win, text="open file", command=open_file)
    btn_open.pack(pady=10)

    txt_orig.pack(side=tk.LEFT, padx=10, pady=10)
    
    btn_conv = tk.Button(win, text="convert file", command=conv_file)
    btn_conv.pack(pady=10)

    txt_out.pack(side=tk.RIGHT, padx=10, pady=10)

    win.mainloop()


def main() -> None:
    
    window()

        

if __name__ == "__main__":
    main()