def determinante(matriz):
    if len(matriz) == 1:
        return matriz[0][0]
    if len(matriz) == 2:
        return matriz[0][0]*matriz[1][1] - matriz[0][1]*matriz[1][0]

    #se for > 2x2 faz laplace
    #vai fazendo submatriz de cada elemento de uma linha e vai calculando o determinante dela, multiplicando por ij e somando em det
    det = 0
    for c in range(len(matriz)):
        submat = []
        for row in matriz[1:]:
            nova_linha = row[:c] + row[c+1:]
            submat.append(nova_linha)
        sign = (-1) ** c
        det += sign * matriz[0][c] * determinante(submat)
    return det

def inversa(matriz):
    tamanho_matriz = len(matriz)
    identidade = []
    #cria matriz identidade
    for j in range(tamanho_matriz):
        linha = []
        for i in range(tamanho_matriz):
            linha.append(float(i == j))
        identidade.append(linha)
    
    #junta a matriz A com a identidade
    matriz_aumentada = []
    for i, linha in enumerate(matriz):
        matriz_aumentada.append(linha[:] + identidade[i])

    for i in range(tamanho_matriz):
        #se for 0 ele troca o pivô
        if matriz_aumentada[i][i] == 0:
            for j in range(i+1, tamanho_matriz):
                if matriz_aumentada[j][i] != 0:
                    #troca as linha se for 0
                    matriz_aumentada[i], matriz_aumentada[j] = matriz_aumentada[j], matriz_aumentada[i]
                    break
        div = matriz_aumentada[i][i]
        nova_linha = []
        #divide a linha pelo pivô
        for m in matriz_aumentada[i]:
            nova_linha.append(m / div)
        matriz_aumentada[i] = nova_linha
        #percorre todas as linhas menos do pivo e vai zerando com gauss p transformas A em A-1
        for j in range(tamanho_matriz):
            if j != i:
                fator = matriz_aumentada[j][i]
                nova_linha = []
                for k in range(2*tamanho_matriz):
                    nova_linha.append(matriz_aumentada[j][k] - fator * matriz_aumentada[i][k])
                matriz_aumentada[j] = nova_linha

    #pega só a inversa
    resultado = []
    for linha in matriz_aumentada:
        resultado.append(linha[tamanho_matriz:])
    return resultado

def multiplicacao(matrizA, matrizB):
    linhas_A = len(matrizA)
    colunas_B = len(matrizB[0])
    colunas_A = len(matrizA[0])

    resultado = []
    for i in range(linhas_A):
        linha = []
        for j in range(colunas_B):
            linha.append(0)
        resultado.append(linha)
    for i in range(linhas_A):
        for j in range(colunas_B):
            for k in range(colunas_A):
                resultado[i][j] += matrizA[i][k] * matrizB[k][j]
    return resultado