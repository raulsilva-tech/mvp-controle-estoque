# MVP de Controle de Estoque — Mercadinho Boa Compra

MVP acadêmico para cadastro de produtos, consulta de estoque e registro de entradas/saídas.
Projeto organizado em frontend Angular 20+, API Python/FastAPI e banco PostgreSQL.

> Os dados de demonstração são fictícios. Este projeto é uma base inicial para desenvolvimento e validação acadêmica, não um sistema pronto para produção.

## Funcionalidades

- Login com token JWT (usuário administrador inicial configurável por variáveis de ambiente).
- Cadastro e consulta de produtos pela interface e API.
- Registro de entradas e saídas com validação de saldo.
- Atualização do saldo e gravação do histórico na mesma transação.
- Listagem de produtos abaixo ou no estoque mínimo.
- Interface responsiva com rótulos, mensagens textuais e alertas que não dependem apenas de cores.

## Tecnologias

- Angular 20+ / TypeScript
- Python 3.12 / FastAPI / Pydantic
- SQLAlchemy 2
- PostgreSQL
- Pytest
- Docker Compose
- GitHub Actions (CI)

## Estrutura

```text
mvp-controle-estoque/
├── backend/
│   ├── app/
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   ├── angular.json
│   └── package.json
├── .github/workflows/ci.yml
├── docker-compose.yml
├── .env.example
└── README.md
```

## Executar com Docker

1. Instale Docker e Docker Compose.
2. Copie `.env.example` para `.env` e altere os valores.
3. Na raiz do projeto, execute:

```bash
docker compose up --build
```

- Frontend: http://localhost:4200
- API: http://localhost:8000
- Documentação OpenAPI: http://localhost:8000/docs

O banco cria as tabelas automaticamente na inicialização para facilitar o MVP. Para uma evolução de projeto, recomenda-se adicionar Alembic e migrações versionadas.

## Executar a API localmente

Requer Python 3.12+ e PostgreSQL disponível.

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

Configure `DATABASE_URL`, `JWT_SECRET`, `ADMIN_USERNAME` e `ADMIN_PASSWORD` conforme `.env.example`, depois:

```bash
uvicorn app.main:app --reload
```

## Executar testes

```bash
cd backend
pytest -q
```

Os testes usam SQLite em memória para não depender do PostgreSQL. Os testes exercitam autenticação, cadastro, consulta e regras de movimentação por meio da API.

## Executar o frontend localmente

```bash
cd frontend
npm install
npm start
```

O frontend espera a API em `http://localhost:8000`. Para outro endereço, ajuste `src/environments/environment.ts`.

## Primeiro acesso

O usuário e a senha iniciais são definidos por `ADMIN_USERNAME` e `ADMIN_PASSWORD`. O valor de exemplo do `.env.example` serve somente para desenvolvimento. Troque-o antes de compartilhar o sistema.

## API principal

- `POST /api/auth/login`
- `GET /api/products`
- `POST /api/products`
- `GET /api/products/{product_id}/movements`
- `POST /api/movements`
- `GET /api/dashboard/summary`

As rotas de produtos e movimentações exigem `Authorization: Bearer <token>`.

## Fluxo principal

1. Entrar no sistema.
2. Abrir **Movimentar estoque**.
3. Selecionar produto, tipo e quantidade.
4. Confirmar a operação.
5. Conferir saldo atualizado, histórico e alertas de estoque mínimo.

## Git: sugestão de histórico semântico

```bash
git init
git add .
git commit -m "chore: estrutura inicial do MVP"
git add .
git commit -m "feat: implementa cadastro e consulta de produtos"
git add .
git commit -m "feat: registra entradas e saídas de estoque"
git add .
git commit -m "test: adiciona testes de API e regras de estoque"
```

Para praticar Pull Request, crie uma branch (`feat/movimentacao-estoque`), implemente uma mudança, abra um PR para `main` e registre no PR a revisão realizada, os testes executados e eventuais ajustes.

## Limitações conhecidas

- Cadastro de usuários e gestão de perfis completos não estão implementados; existe apenas autenticação para o administrador inicial.
- Não há emissão fiscal, PDV, compras, fornecedores, controle de validade ou aplicativo nativo.
- Não configure este projeto diretamente em produção sem revisão de segurança, migrações, logs, backup, HTTPS, gestão de segredos e testes adicionais.
