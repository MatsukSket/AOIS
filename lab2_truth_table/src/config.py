OP_NOT = '!'
OP_AND = '&'
OP_OR = '|'
OP_IMP= '>'
OP_IMP1 = '->'
OP_EQ = '~'

PRIORITY = {
    OP_NOT: 4,
    OP_AND: 3,
    OP_OR: 2,
    OP_IMP: 1,
    OP_EQ: 1,
    '(': 0
}

VARS = {'a', 'b', 'c', 'd', 'e'}