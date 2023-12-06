import tkinter as tk
from tkinter import filedialog

INPUT_FILE = "./asm.asm"

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

LABELS = {}

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

    cont = []
    with open(name, "r") as file:
        file.seek(0)
        cont = file.readlines()
    
    lines = []
    for line in cont:
        if not line == "\n":
            lines.append(line)
    
    return lines
    

def binary_converter(n:int, bits:int):
    binary_representation = ""
    aux = n
    while aux > 0:
        binary_representation += str(aux % 2)
        aux //= 2
    
    if len(binary_representation) < bits:
        for _ in range(0, bits - len(binary_representation)):
            binary_representation += "0"

    return binary_representation[::-1]


def op_instruction(instruction:str, line:int) -> str:
    instruction = instruction.replace("\n", "")

    # split instruction by " "
    entities = instruction.split(" ")

    # search index of operation
    op = OP_CODES.index(entities[0])

    # convert operation index in binary (5 bits)
    bin = binary_converter(op, 5)

    # iterate rest of entities in the instruction
    for entity in entities[1:]:
        entity = entity.replace(",", "")

        if entity in REG_CODES:
            # save last line where the register was used
            DIR_REG[entity] = line

            reg = REG_CODES.index(entity)
            bin += " "
            bin += binary_converter(reg, 4)

        elif "[" in entity:
            entity = entity.replace("[", "")
            entity = entity.replace("]", "")

            # save last line where the register was used
            DIR_REG[entity] = line

            dir = binary_converter(DIR_REG[entity], 4)
            bin += " "
            bin += dir
        
        elif entity[0] == "#":
            bin += " "
            bin += binary_converter(int(entity[1:]), 8)

    return bin


def jm_instruction(instruction:str) -> str:
    instruction = instruction.replace("\n", "")

    # split instruction by " "
    entities = instruction.split(" ")

    # convert the jump operation index in binary (5 bits)
    bin = JM_CODES[entities[0]]

    # 
    if len(entities) > 2:

        bin += " "
        label = entities[1].replace("," ,"")
        bin += binary_converter(LABELS[label], 8)

        bin += " "
        reg = REG_CODES.index(entities[2])
        bin += binary_converter(reg, 8)
    
    else:
        bin += " "
        label = entities[1]
        bin += binary_converter(LABELS[label], 8)
    
    return bin
        

def search_labels(file) -> None:
    lines = read_file(file)

    i = 1
    for line in lines:

        entity = line.split(" ")[0]
        entity = entity.replace("\n", "")

        if entity[-1] == ":":
            # print(f"{i}: {entity}")
            LABELS[entity[:-1]] = i
        
        i+=1


def conversor(file) -> list[str]:
    
    ans = []

    search_labels(file)

    lines = read_file(file)

    out = ""

    i = 1
    for line in lines:

        entity = line.split(" ")[0]

        entity = entity.replace("\n", "")
    
        # print(entity)

        # operation instruction
        ins = ""
        if entity in OP_CODES:
            ins = op_instruction(line, i)
            # print(f"{i}: {ins}")
            out += ins
        
        elif entity in JM_CODES:
            ins = jm_instruction(line)
            # print(f"{i}: {ins}")
            out += ins

        i += 1

        ins = ins.replace(" ", "")
        padding = ""
        if len(ins) < 24 and not entity[-1] == ":":
            for _ in range(0, 24 - len(ins) ):
                padding += "0"

            padding += ins
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