# Arquitetura

Aplicação monolítica em camadas:
- Apresentação: Angular standalone components.
- API/regras de negócio: FastAPI e Pydantic.
- Persistência: SQLAlchemy e PostgreSQL.

A movimentação atualiza o saldo e insere o histórico na mesma sessão/transação do banco. As entradas são validadas no servidor; a interface não é considerada uma barreira de segurança.
