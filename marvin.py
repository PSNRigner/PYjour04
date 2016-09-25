from cnorm.nodes import *


# noinspection PyUnresolvedReferences,PyProtectedMember
def marvin(d: Decl) -> str:
    result = d._name if d._name else "tout seul dans son coin,"
    r = ("", False)
    if d._name:
        result += " est"
    if isinstance(d.ctype, PrimaryType):
        r = variable(d)
        result += r[0]
    elif isinstance(d.ctype, ComposedType):
        # print(">>")
        # print(vars(d))
        r = composed(d)
        result += r[0]
    result = ("je definie! " if d.colon_expr() is None and not r[1] else "je declare! ") + result
    result += "\n"
    # print(vars(d))
    return result


# noinspection PyProtectedMember
def composed(ast=None, ctype=None) -> str:
    if ctype is None:
        ctype = ast.ctype
    result = ""
    if hasattr(ctype, "enums"):
        return result + " un enumere %squi a %d valeurs possibles" % ("" if ctype._identifier == '' else ctype._identifier + " ", len(ctype.enums)), False

    result += {
        1: " une structure",
        2: " une union"
    }[ctype._specifier]

    if ctype._identifier:
        result += " " + ctype._identifier

    if ctype.fields:
        result += " qui contient des champs qui me saoulent"

    return result, (ast is None or ast._name == '')


# noinspection PyProtectedMember
def variable(ast) -> str:
    if hasattr(ast, '_colon_expr') and ast._colon_expr:
        return " un champs de bit", False

    result = ""
    ad = False

    ptype = ast.ctype
    s = ptype._storage
    if s == 2:
        result += " un type sur"
        ad = True
    if s == 4:
        ad = True
    if isinstance(ptype, FuncType):
        result += " une fonction qui retourne"
        if ptype._storage != 5:
            ad = True
    r = rec(ptype._decltype)
    result += r[0]
    c = r[1]

    if ptype._identifier != '':
        result += {
            "int": " un entier",
            "float": " un floattant",
            "double": " un floattant double precision",
            "void": " rien",
            "char": " un caractere"
        }.get(ptype._identifier, " de type utilisateur " + ptype._identifier)
    elif hasattr(ptype, 'fields'):
        r = composed(ctype=ptype)
        result += r[0]

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
        3: " definie localement",
        5: " et dont le code est integrer a l'appelant"
    }.get(ptype._storage, '')

    if hasattr(ast, '_assign_expr'):
        result += " qui est initialise a une certaine valeur mais ca me saoule"

    if isinstance(ptype, FuncType) and hasattr(ptype, '_params') and ptype._params is not None and len(ptype._params) != 0:
        result += " et qui prends des parametres qui me saoulent"

    return result, ad


# noinspection PyProtectedMember,PyUnresolvedReferences
def rec(d, index=0):
    result = ""
    c = -1
    if d and isinstance(d, QualType):
        c = d._qualifier
        d = d._decltype
    if not d:
        return result, c, True
    r = rec(d._decltype, index + 1)
    result += r[0]
    c2 = r[1]
    last = r[2]
    if isinstance(d, ArrayType):
        result += (" de" if not last else " un") + " tableau" + get_const(c)
        if isinstance(d.expr, Func):
            result += " dont la taille depend d'une expression relou a calculer"
        elif isinstance(d.expr, Literal):
            result += " de taille " + d.expr.value
        if index == 0:
            result += " ou chaque case contient"
    elif isinstance(d, PointerType):
        result += " de" if not last else " un"
        result += " pointeur" + get_const(c)
        if index == 0:
            result += " sur"
    return result, c2, False


def get_const(c):
    return {
        1: " constant",
        2: " toujours mis a jour lorsqu'on y accede"
    }.get(c, '')
