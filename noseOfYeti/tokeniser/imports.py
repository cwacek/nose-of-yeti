from tokenize import OP, NEWLINE
from tokens import tokensIn

def determineImports(with_default_imports=True, without_should_dsl=False, extra_imports=None):
    default = []

    if extra_imports:
        if type(extra_imports) in (str, unicode):
            default.extend(tokensIn(extra_imports))
        else:
            for d in extra_imports:
                if d[0] == NEWLINE:
                    # I want to make sure the extra imports don't 
                    # Take up extra lines in the code than the "# coding: spec"
                    default.append((OP, ';'))
                else:
                    default.append(d)

    if with_default_imports:
        if default and tuple(default[-1]) != (OP, ';'):
            default.append((OP, ';'))

        should_dsl = "from should_dsl import *;"
        if without_should_dsl:
            should_dsl = ""
        
        default.extend(
            tokensIn('import nose; from nose.tools import *; %s from noseOfYeti.noy_helper import *;' % should_dsl)
        )

    return default