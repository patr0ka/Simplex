from parser import leTxt, normalizacao
from simplex import simplex_fase1, simplex_fase2
from var_artificial import adicionar_variaveis_artificiais

def main():
    is_max, c, restricoes = leTxt('entrada.txt')
    print("<------ Problema de", "Maximização ------>" if is_max else "Minimização ------>")

    print("\n[Pré-processamento] Verificando o vetor b...")
    #se tiver linha negativa ele faz *-1 e troca o sinal
    for i, (a_row, op, termo_indep) in enumerate(restricoes):
        if termo_indep < 0:
            a_row = [-x for x in a_row]
            termo_indep = -termo_indep
            if op == '<=':
                op = '>='
            elif op == '>=':
                op = '<='
            restricoes[i] = (a_row, op, termo_indep)


    precisa_fase1 = any(op in ['>=', '='] for _, op, _ in restricoes)
    c_padrao, A, b = normalizacao(c, restricoes)

    if is_max:
        c_padrao = [-ci for ci in c_padrao]

    m = len(A)
    n_sem_artificiais = len(A[0])
    base_para_fase2 = []

    if precisa_fase1:
        print("\n[Fase 1] Problema requer Fase I. Encontrando base viável...")
        A_art, b_art, c_art, base_inicial_art = adicionar_variaveis_artificiais(A, b, c_padrao)
        
        solucao_fase1, base_fase1, status_f1 = simplex_fase1(c_art, A_art, b_art, base_inicial_art)

        if status_f1 == "infactivel":
            print("Problema infactível! (não há solução viável)")
            return

        base_para_fase2 = [j for j in base_fase1 if j < n_sem_artificiais]
        folgas_disponiveis = [j for j in range(n_sem_artificiais) if j not in base_para_fase2]
        while len(base_para_fase2) < m:
            base_para_fase2.append(folgas_disponiveis.pop(0))
    else:
        print("\nFase I não é necessária. Base inicial de folga é viável.")
        num_vars_originais = len(c)
        base_para_fase2 = list(range(num_vars_originais, n_sem_artificiais))

    print("\n[Fase 2] Resolvendo problema original...")
    x_final, z_final, status_f2 = simplex_fase2(c_padrao, A, b, base_para_fase2)

    if status_f2 == "ilimitado":
        print("\nProblema ilimitado! (não há solução ótima finita)")
        return

    if is_max:
        z_final = -z_final

    print("\nSolução ótima encontrada:")
    print(f"x = {x_final[:len(c)]}")  
    print(f"Z = {z_final}")

if __name__ == '__main__':
    main()