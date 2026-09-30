import copy


def adicionar_variaveis_artificiais(A, b, c):

    num_linhas = len(A)  
    num_colunas = len(A[0])  

    copia_A = copy.deepcopy(A)
    vetor_c = [0] * num_colunas
    
    # gruda a identidade com a matriz A
    for i in range(num_linhas):
        nova_coluna = [1 if j == i else 0 for j in range(num_linhas)]
        
        for j in range(num_linhas):
            copia_A[j].append(nova_coluna[j])
        
        vetor_c.append(1)
    
    
    #gera a primeira base da fI
    base_inicial = list(range(num_colunas, num_colunas + num_linhas))
    
    return copia_A, b[:], vetor_c, base_inicial

def verificar_variaveis_artificiais_na_base(base, n_original, n_artificiais):
    return any(j >= n_original for j in base)