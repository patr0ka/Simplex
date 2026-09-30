from op_matrizes import inversa, multiplicacao
TOLERANCIA = 1e-9

def simplex_fase1(c, A, b, base_inicial):
    
    num_linhas = len(A)
    num_colunas = len(A[0])
    num_varArtificial = num_colunas - len(c) + len(base_inicial)
    iteracao = 1
    
    # encontra base e não base
    base = base_inicial.copy()
    nao_base = [j for j in range(num_colunas) if j not in base]
    
    print("\n----------> Fase I")
    
    while True:
        # 1 - calcula a solução básica

        # pega as colunas da base e calcula a inversa
        B = [[A[i][j] for j in base] for i in range(num_linhas)]
        B_inv = inversa(B)
        solucao_basica = multiplicacao(B_inv, [[b[i]] for i in range(num_linhas)])

        # coloca o valor da solucao basica num vetor com 0 nas nao base
        x = [0] * num_colunas
        for i, j in enumerate(base):
            x[j] = solucao_basica[i][0]
        
        # 2 - calcula custo relativo 

        # 2.1 - vetor multiplicador simplex
        custo_basicas = [c[j] for j in base]
        lambda_ = multiplicacao([custo_basicas], B_inv)[0]
        
        # 2.2 - calcula custo relativo de cada var não base 
        custos_relativos = {}
        for j in nao_base:
            a_j = [A[i][j] for i in range(num_linhas)]
            custo_padrão = c[j]
            custos_relativos[j] = custo_padrão - sum(lambda_[i] * a_j[i] for i in range(num_linhas))

        # 2.3 - vê qual variável entra na base
        if all(cr >= -1e-10 for cr in custos_relativos.values()):

            # vê se tem alguma variável artificial na base com valor > 0
            variaveis_artificiais_na_base = []
            for j in base:
                if j >= len(c) - num_varArtificial:
                    variaveis_artificiais_na_base.append(j)
            
            if variaveis_artificiais_na_base:
                # Verificar se o valor das variáveis artificiais é próximo de zero
                tem_artificial_positiva = False
                for j in variaveis_artificiais_na_base:
                    if x[j] > 1e-6:
                        tem_artificial_positiva = True
                        break
                
                if tem_artificial_positiva:
                    print("Problema infactível")
                    return x, base, "infactivel"
            
            print("Fase I concluída com sucesso")
            return x, base, "factivel"
        
        # se não for ótimo (tiver negativo), pega a não base com custo relativo mais negativo, põe na base e segue
        j_entra = min(custos_relativos.items(), key=lambda item: item[1])[0]
                
        # 4 - vê o comportamento da base ao colocar a nova varivael
        a_j = [[A[i][j_entra]] for i in range(num_linhas)]
        y = multiplicacao(B_inv, a_j)  
        
        # 5 -  vai incrementando a nova variavel, a que base que zerar primeiro sai
        razoes = {}
        for i in range(num_linhas):
        # y tem q ser > 0 para que as varaiveis estejam diminuindo
            if y[i][0] > TOLERANCIA:
                razoes[i] = solucao_basica[i][0] / y[i][0]

        #se nenhuma diminui é pq é ilimitado, pq pode crescer p sempre
        if not razoes:
            print("Não há razões válidas - Problema ilimitado")
            return x, base, "ilimitado"  
    
        # encontrar índice com razão mínima
        indice_sai = min(razoes.items(), key=lambda item: item[1])[0]
                
        # Passo 6: Atualização da partição básica
        base[indice_sai] = j_entra
        nao_base = [j for j in range(num_colunas) if j not in base]
        
        # Verificar se ainda há variáveis artificiais na base
        variaveis_artificiais_na_base = [j for j in base if j >= len(c) - num_varArtificial]
        if not variaveis_artificiais_na_base:
            print("Não há mais variáveis artificiais na base - podemos prosseguir para a Fase II")
        else:
            print(f"Ainda há variáveis artificiais na base: {variaveis_artificiais_na_base}")
        
        iteracao += 1


def simplex_fase2(c, A, b, base_inicial):
    
    num_linhas = len(A)
    num_colunas = len(A[0])
    iteracao = 1
    
    # encontra base e não base
    base = base_inicial.copy()
    nao_base = [j for j in range(num_colunas) if j not in base]
    
    print("\n----------> Fase II")
    
    while True:
        # 1 - calcula a solução básica

        # pega as colunas da base e calcula a inversa
        B = [[A[i][j] for j in base] for i in range(num_linhas)]
        B_inv = inversa(B)
        solucao_basica = multiplicacao(B_inv, [[b[i]] for i in range(num_linhas)])

        # coloca o valor da solucao basica num vetor com 0 nas nao base
        x = [0] * num_colunas
        for i, j in enumerate(base):
            x[j] = solucao_basica[i][0]
           
        # 2 - calcula custo relativo 

        # 2.1 - vetor multiplicador simplex
        custo_basicas = [c[j] for j in base]
        lambda_ = multiplicacao([custo_basicas], B_inv)[0]
        
        # 2.2 - calcula custo relativo de cada var não base 
        custos_relativos = {}
        for j in nao_base:
            a_j = [A[i][j] for i in range(num_linhas)]
            custo_padrão = c[j]
            custos_relativos[j] = custo_padrão - sum(lambda_[i] * a_j[i] for i in range(num_linhas))
        
        # 2.3 - vê qual variável entra na base
        # se for tudo >=0 é pq já é ótimo
        if all(cr >= -1e-10 for cr in custos_relativos.values()):
            z = sum(c[j] * x[j] for j in range(num_colunas))
            return x, z, "otimo"
        
        # se não for ótimo (tiver negativo), pega a não base com custo relativo mais negativo, põe na base e segue
        j_entra = min(custos_relativos.items(), key=lambda item: item[1])[0]
                
        # 4 - vê o comportamento da base ao colocar a nova varivael
        a_j = [[A[i][j_entra]] for i in range(num_linhas)]
        y = multiplicacao(B_inv, a_j) 
        
        # 5 -  vai incrementando a nova variavel, a que base que zerar primeiro sai
        razoes = {}
        for i in range(num_linhas):
            # y tem q ser > 0 para que as varaiveis estejam diminuindo
            if y[i][0] > TOLERANCIA:
                razoes[i] = solucao_basica[i][0] / y[i][0]

        #se nenhuma diminui é pq é ilimitado, pq pode crescer p sempre
        if not razoes:
            print("Não há razões válidas, problema ilimitado")
            return x, 0, "ilimitado"   # na fase 2

        # encontra o indice que zera primeiro (ele sai da base)
        indice_sai = min(razoes.items(), key=lambda item: item[1])[0]
                
        # 6 - só atualiza a base e não base, e repete tudo
        base[indice_sai] = j_entra
        nao_base = [j for j in range(num_colunas) if j not in base]
        iteracao += 1