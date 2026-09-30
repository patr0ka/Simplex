# 📊 Método Simplex - Duas Fases (Python)

Implementação em Python puro do algoritmo **Simplex de Duas Fases** (*Two-Phase Simplex Method*) para resolução de problemas de **Programação Linear (PL)**, desenvolvido para a disciplina de **Pesquisa Operacional** (5º Semestre - Ciência da Computação / UNICENTRO).

---

## 🚀 Funcionalidades

- **Maximização e Minimização**: Suporte nativo tanto para problemas de `max` quanto de `min`.
- **Restrições Diversificadas**: Aceita desigualdades (`<=`, `>=`) e igualdades (`=`).
- **Pré-processamento Automático**:
  - Ajuste automático de restrições com termos independentes negativos ($b_i < 0$), multiplicando a linha por $-1$ e invertendo o operador.
- **Método das Duas Fases**:
  - **Fase I**: Adiciona variáveis artificiais e busca uma solução básica viável inicial, detectando problemas **infactíveis**.
  - **Fase II**: Otimiza a função objetivo a partir da base viável gerada pela Fase I (ou diretamente pela base de folgas, se aplicável), detectando problemas **ilimitados**.
- **Álgebra Linear Pura (Zero Dependências Externas)**:
  - Toda a matemática matricial foi desenvolvida do zero (sem NumPy/SciPy):
    - Inversão de matriz por eliminação de Gauss-Jordan.
    - Determinante via expansão de Laplace.
    - Multiplicação de matrizes.
- **Parser com Expressões Regulares**:
  - Leitura intuitiva de equações lineares diretamente de um arquivo de texto formatado (`entrada.txt`).

---

## 📁 Estrutura do Projeto

```text
Simplex/
├── main.py             # Ponto de entrada da aplicação e orquestração das fases
├── simplex.py          # Implementação das iterações da Fase I e Fase II do Simplex
├── parser.py           # Parser regex para leitura e normalização das restrições
├── op_matrizes.py      # Operações de álgebra linear (inversa, determinante, multiplicação)
├── var_artificial.py   # Criação e tratamento das variáveis artificiais para a Fase I
├── entrada.txt         # Arquivo com o problema atual a ser resolvido
├── lista_testes.txt    # Bateria de testes práticos com gabaritos (ótimos, ilimitados e infactíveis)
└── .gitignore          # Arquivos e pastas ignorados pelo Git
```

---

## 🛠️ Como Usar

### Pré-requisitos
- **Python 3.8+** instalado.
- Não requer instalação de pacotes externos (`pip`), utilizando apenas a biblioteca padrão do Python.

### 1. Definindo o Problema (`entrada.txt`)
Crie ou edite o arquivo `entrada.txt` na raiz do projeto com o modelo linear. 

- A primeira linha define o tipo (`max` ou `min`) e a função objetivo $z$.
- As linhas seguintes contêm as restrições lineares.
- As variáveis devem seguir o padrão $x_1, x_2, x_3, \dots, x_n$.

#### Exemplo de `entrada.txt`:
```text
max z = 3x1 + 3x2 + 13x3
-3x1 + 6x2 + 7x3 <= 8
6x1 - 3x2 + 7x3 >= 8
x1 <= 2
x3 <= 0
```

### 2. Executando o Simplex
Execute o script principal via terminal:

```bash
python main.py
```

### 3. Exemplo de Saída no Terminal
```text
<------ Problema de Maximização ------>

[Pré-processamento] Verificando o vetor b...

[Fase 1] Problema requer Fase I. Encontrando base viável...

----------> Fase I
Ainda há variáveis artificiais na base: [7, 8, 9]
Ainda há variáveis artificiais na base: [7, 9]
Ainda há variáveis artificiais na base: [7]
Não há mais variáveis artificiais na base - podemos prosseguir para a Fase II
Fase I concluída com sucesso

[Fase 2] Resolvendo problema original...

----------> Fase II

Solução ótima encontrada:
x = [2.0, 1.3333333333333335, 0.0]
Z = 10.0
```

---

## 🧪 Casos de Teste

O arquivo [`lista_testes.txt`](lista_testes.txt) reúne dezenas de problemas com seus respectivos resultados esperados:
- Problemas com solução ótima única;
- Problemas **ilimitados**;
- Problemas **infactíveis**;
- Problemas que exigem ou dispensam a Fase I.

Basta copiar qualquer um dos blocos para o arquivo `entrada.txt` e rodar `python main.py` para conferir a resolução.

---

## 👨‍💻 Autor

Desenvolvido por **Patrick** ([@patr0ka](https://github.com/patr0ka)).
