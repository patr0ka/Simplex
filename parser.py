import re

def leTxt(file_path):
    with open(file_path, 'r') as func:
        lines = [line.strip() for line in func if line.strip()]

    #divide a primeira linha em max ou min e a função objetivo
    obj_match = re.match(r'(max|min)\s+z\s*=\s*(.*)', lines[0].lower())
    is_max = obj_match.group(1) == 'max'
    obj_expr = obj_match.group(2)
    
    #regex para ver o padrão das variáveis na função objetivo e nas restrições
    var_pattern = re.compile(r'([+-]?\s*\d*\.?\d*)x(\d+)')
    vars_indices = set()


    #tira espaços e coloca 1 em variaveis unitárias
    def parse_expr(expr):
        parsed = {}
        for coef, var in var_pattern.findall(expr.replace('-', '+-')):
            coef = coef.replace(' ', '')

            coef = coef if coef and coef != '+' and coef != '-' else coef + '1'
            parsed[int(var)] = float(coef)
            vars_indices.add(int(var))

        return parsed

    obj_parsed = parse_expr(obj_expr)
    num_vars = max(vars_indices)

    c = [obj_parsed.get(i+1, 0.0) for i in range(num_vars)]       

    restricoes = []
    for line in lines[1:]:

        if '<=' in line:
            esquerda_igual, direita_igual = line.split('<=')
            op = '<='
        elif '>=' in line or '=>' in line:
            esquerda_igual, direita_igual = re.split(r'>=|=>', line)
            op = '>='
        elif '<' in line:
            esquerda_igual, direita_igual = line.split('<')
            op = '<='
        elif '>' in line:
            esquerda_igual, direita_igual = line.split('>')
            op = '>='
        else:
            esquerda_igual, direita_igual = line.split('=')
            op = '='

        esquerda_parsed = parse_expr(esquerda_igual)

        a_row = [esquerda_parsed.get(i+1, 0.0) for i in range(num_vars)]

        b_val = float(direita_igual.strip())

        restricoes.append((a_row, op, b_val))

    return is_max, c, restricoes
    


#normaliza o problema colocando todas as restrições em <= e adicionando variáveis de folga
def normalizacao(c, constraints):
    A = []
    b = []

    novo_c = c[:]
    coef_varFolga = 0
    num_varFolga = len(constraints)

    for a_row, op, b_val in constraints:
        row = a_row[:]
        folga = [0] * num_varFolga
        if op == '<=':
            folga[coef_varFolga] = 1
            novo_c.append(0)
        elif op == '>=':
            folga[coef_varFolga] = -1
            novo_c.append(0)
        else:  # '='
            novo_c.append(0)
        row.extend(folga)
        A.append(row)
        b.append(b_val)
        coef_varFolga += 1

    return novo_c, A, b