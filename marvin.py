from cnorm.nodes import *


# noinspection PyUnresolvedReferences,PyProtectedMember
def marvin(d: Decl) -> str:
    result = "je definie! " if not d.colon_expr() else "je declare! "
    result += d._name
    if isinstance(d.ctype, PrimaryType):
        result += variable(d)
    # result += "\n"
    # print(vars(d))
    return result


# noinspection PyProtectedMember
def variable(ast) -> str:
    result = " est"

    if ast._colon_expr:
        return " est un champs de bit"

    ptype = ast.ctype
    r = rec(ptype._decltype)
    result += r[0]
    c = r[1]

    if ptype._identifier != '':
        result += {
            "int": " un entier",
            "float": " un floattant",
            "double": " un floattant double precision",
            "void": " rien",
            "char": " un caractere",
            "GG": ""
        }[ptype._identifier]

    if ptype._specifier != 0:
        result += {
            4: " a la jack",
            5: " a la super-jack",
            6: " court"
        }.get(ptype._specifier, '')

    result += get_const(c)

    if hasattr(ptype, '_sign'):
        result += {
            2: " positif ou nul"
        }.get(ptype._sign, '')

    result += {
        1: " stocker dans un registre",
        3: " definie localement"
    }.get(ptype._storage, '')

    if hasattr(ast, '_assign_expr'):
        result += " qui est initialise a une certaine valeur mais ca me saoule"

    return result


# noinspection PyProtectedMember,PyUnresolvedReferences
def rec(d, index=0):
    result = ""
    c = -1
    if d and isinstance(d, QualType):
        c = d._qualifier
        d = d._decltype
    if not d:
        return result, c
    r = rec(d._decltype, index + 1)
    result += r[0]
    c2 = r[1]
    if isinstance(d, ArrayType):
        result += (" de" if d._decltype else " un") + " tableau" + get_const(c)
        if isinstance(d.expr, Binary):
            result += " dont la taille depend d'une expression relou a calculer"
        elif isinstance(d.expr, Literal):
            result += " de taille " + d.expr.value
        if index == 0:
            result += " ou chaque case contient"
    elif isinstance(d, PointerType):
        result += " de" if d._decltype else " un"
        result += " pointeur" + get_const(c)
        if index == 0:
            result += " sur"
    return result, c2


def get_const(c):
    return {
        1: " constant",
        2: " toujours mis a jour lorsqu'on y accede"
    }.get(c, '')
