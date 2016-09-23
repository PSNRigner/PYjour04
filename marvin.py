from cnorm.nodes import *


# noinspection PyUnresolvedReferences,PyProtectedMember
def marvin(ast: Decl) -> str:
    result = ""
    for d in ast.body:
        result += "je definie! " if not d.colon_expr() else "je declare! "
        result += d._name
        if isinstance(d.ctype, PrimaryType):
            result += variable(d)
        result += "\n"
        #print(vars(d))
    return result


# noinspection PyProtectedMember
def variable(ast) -> str:
    result = " est"

    if ast._colon_expr:
        return " est un champs de bit"

    ptype = ast.ctype
    d = array_rec(ptype)
    result += d[0]
    d = d[1]
    e = 0
    while d and isinstance(d, PointerType):
        result += " un" if e == 0 else " de"
        if d._decltype and isinstance(d._decltype, PointerType):
            result += " pointeur"
        else:
            result += " pointeur sur"
        d = d._decltype
        e += 1

    if ptype._identifier != '':
        result += {
            "int": " un entier",
            "float": " un floattant",
            "double": " un floattant double precision",
            "void": " rien",
            "char": "",
            "GG": ""
        }[ptype._identifier]

    if ptype._specifier != 0:
        result += {
            4: " a la jack",
            5: " a la super-jack",
            6: " court"
        }.get(ptype._specifier, '')

    if ptype._decltype and hasattr(ptype._decltype, '_qualifier'):
        result += {
            1: " constant"
        }.get(ptype._decltype._qualifier, '')

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


# noinspection PyProtectedMember
def array_rec(ptype):
    result = ""
    val = []
    m = 0
    d = ptype._decltype
    while d and isinstance(d, ArrayType):
        if isinstance(d.expr, Literal):
            val.append(d.expr.value)
        else:
            val.append(0)
        d = d._decltype
        m += 1

    d = ptype._decltype
    i = 0

    while d and isinstance(d, ArrayType):
        result += (" de" if i != 0 else " un") + " tableau"
        if isinstance(d.expr, Binary):
            result += " dont la taille depend d'une expression relou a calculer"
        elif isinstance(d.expr, Literal):
            result += " de taille " + val[m - 1 - i]
        d = d._decltype
        i += 1
        if not d:
            result += " ou chaque case contient"
    return result, d
