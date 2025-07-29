# desafio_transacoes_bancaria
Projeto Final curso ADA - GRUPO 3
Projeto em Python


Descrição do Projeto
# Projeto Transações Bancárias -- logica de programacao II

Esse programa é um sistema de gestao de transacoes de uma conta bancária pessoal no qual os dados são de transações e possuem seu valor, a categoria do gasto e seu ID.
 
Teu objetivo é completar esse sistema CRUD (Create-Read-Update-Delete) simples para ver dados de transacao da tua conta pessoal, criar, editar e excluir transações.

Também deve fazer com que o programa NUNCA pare, ou seja, caso ocorra um possível erro, deve validar as entradas, detectar erros e avisar o usuário, mas o programa não deve parar.


## Notas importantes: 
1. As funções que geram os dados e criam a interface do sistema já estão prontas. Por favor não as altere.

2. Depois das funções do sistema estão as funções do programa no qual podem alterar à vontade, exceto o nome das funções. Ou seja, podem criar funções, adicionar ou remover parâmetros, mas não alterar o nome das funções existentes.

3. Coloque opções de navegabilidade em cada janela que o usuário estiver. Por exemplo, se ele escolher a opcao "alterar transacao" sem querer, tem que ter a opcao de voltar para a tela anterior ou inicial.

4. Caso por qualquer motivo queira os dados originais novamente, apage o json `transactions` na pasta `data` e inicie o programa novamente para gerar os dados. Os valores serão os mesmos, porém os UUID NÃO serão os mesmos!!

5. A exibição do relatório deve conter:
    - O valor total de transações da conta (calcular_total_transacoes)
    - Todas as m5 transações realizadas
    - Deve ter a opção de salvar o relatório em um arquivo
    - Deve ter a opção de visualizar na tela
