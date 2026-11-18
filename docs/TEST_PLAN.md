# Plano de testes inicial

## Testes automatizados
- Autenticação: rota protegida sem token deve retornar 401.
- Produto: cadastro deve persistir código, nome e saldo.
- Movimentação: saída válida deve reduzir saldo e gerar histórico.
- Regra de negócio: saída acima do saldo deve retornar 422 sem alterar o estoque.

## Validação com representante externo
Use dados fictícios e protótipo/ambiente de teste:
1. Localizar a função de movimentação no menu.
2. Registrar saída de 5 unidades de Arroz Tipo 1 (AR001), saldo inicial 30.
3. Interpretar o saldo final (25) e os alertas de reposição.

Registre sucesso por tarefa, tempo da tarefa central, necessidade de ajuda, erros, nota de satisfação e comentários. Não registre credenciais ou dados sensíveis.
