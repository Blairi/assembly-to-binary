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
    # "jmp",
    # "je",
    # "jne",
    # "ja",
    # "jae",
    # "jb",
    # "jbe",
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


def read_file() -> list[str]:

    cont = []
    with open(INPUT_FILE, "r") as file:
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

def jm_instruction(instruction:str, line:int) -> str:
    instruction = instruction.replace("\n", "")

    # split instruction by " "
    entities = instruction.split(" ")

    # convert the jump operation index in binary (5 bits)
    bin = JM_CODES[entities[0]]

    # 
    if len(entities) > 2:
        bin += " "
        bin += entities[1].replace("," ,"")
        
        bin += " "
        reg = REG_CODES.index(entities[2])
        bin += binary_converter(reg, 8)
    
    return bin
        


def main() -> None:

    lines = read_file()

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
            ins = jm_instruction(line, i)
            # print(f"{i}: {ins}")
            out += ins

        i += 1

        ins = ins.replace(" ", "")
        padding = ""
        if len(ins) < 24:
            for _ in range(0, 24 - len(ins) ):
                padding += "0"
            padding += ins
    
        print(padding)

        

if __name__ == "__main__":
    main()