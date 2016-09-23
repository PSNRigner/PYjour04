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
        print(vars(d))
    return result


# noinspection PyProtectedMember
def variable(ast) -> str:
    result = ""
    if ast._colon_expr:
        return " est un champs de bit"
    ptype = ast.ctype
    if ptype._identifier != '':
        result += {
            "int": " est un entier",
            "float": " est un floattant",
            "double": " est un floattant double precision",
            "void": "",
            "char": "",
            "GG": ""
        }[ptype._identifier]
    if ptype._specifier != 0:
        result += {
            6: " court"
        }.get(ptype._specifier, '')
    if ptype._decltype and hasattr(ptype._decltype, '_qualifier'):
        result += {
            1: " constant"
        }.get(ptype._decltype._qualifier, '')
    result += {
        1: " stocker dans un registre"
    }.get(ptype._storage, '')
    if hasattr(ast, '_assign_expr'):
        result += " qui est initialise a une certaine valeur mais ca me saoule"
    return result
