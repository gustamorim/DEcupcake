# Publicar DEcupcake na Vercel

O projeto está preparado para Flask na Vercel, com PostgreSQL externo. Em seu computador, sem `DATABASE_URL`, continua usando `instance/cupcake.db`. Os registros do SQLite não são transferidos automaticamente para PostgreSQL.

## Neon já configurado nesta pasta

Projeto **cupcake**, na organização `org-morning-sound-40245926`, região AWS Ohio. Console: https://console.neon.tech/app/projects/silent-sky-09152151/

As tabelas e os cinco sabores já foram inicializados e o catálogo foi verificado usando PostgreSQL. `DATABASE_URL`, `DATABASE_URL_UNPOOLED` e uma `SECRET_KEY` estável estão em `.env.local`, ignorado pelo Git. `run.py` carrega esse arquivo automaticamente; variáveis já definidas no terminal ou na Vercel continuam tendo prioridade.

Nesta pasta, pule os passos 1 e 2 e prossiga para o envio ao GitHub e a configuração da Vercel. Copie os valores de `DATABASE_URL` e `SECRET_KEY` do arquivo local para as variáveis do projeto Vercel; esse envio não é feito pelo Git. O SQLite anterior permanece como arquivo local, sem transferência dos usuários/pedidos para o Neon.

As skills e o MCP do Neon foram configurados para Codex. Reinicie o agente para carregar o MCP. As instruções abaixo também servem para configurar outra instalação do projeto.

## 1. Criar PostgreSQL no Neon

1. Crie sua conta em https://neon.com e selecione o plano Free.
2. Crie um projeto chamado `decupcake`.
3. Abra **Connect** e copie a URL de conexão. Para o site, use **Connection pooling** habilitado. Mantenha os parâmetros de SSL da URL.
4. Guarde a URL como um segredo: ela inclui usuário e senha. Não cole no código ou no GitHub.

O aplicativo aceita `postgresql://...`, `postgres://...` e `postgresql+psycopg://...`; seleciona automaticamente o driver instalado. Cole apenas a URL, sem o comando `psql` ou aspas externas.

## 2. Inicializar o banco remoto uma vez

No PowerShell da pasta do projeto:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:DATABASE_URL = "cole-a-url-direta-do-Neon-aqui"
.\.venv\Scripts\python.exe -m flask --app run init-db
Remove-Item Env:DATABASE_URL
```

Para este passo, copie a URL com **Connection pooling** desabilitado no Neon (conexão direta). O comando cria as tabelas e os cinco sabores, sem apagar dados existentes. Ao remover a variável, o desenvolvimento local volta para SQLite.

O comando não migra tabelas existentes caso você altere seus campos no futuro. Nessa situação, será necessário usar migrações. Se existir `.env.local`, remover a variável do terminal faz o aplicativo voltar a usar a conexão desse arquivo; para forçar SQLite, use `$env:DATABASE_URL = "sqlite:///cupcake.db"`.

## 3. Enviar as alterações ao GitHub

```powershell
git add .
git commit -m "Prepara Flask e PostgreSQL para Vercel"
git push
```

## 4. Importar na Vercel

1. Entre em https://vercel.com com sua conta do GitHub e selecione o plano Hobby para o trabalho acadêmico.
2. Abra **Add New → Project** e importe `gustamorim/DEcupcake`. Se necessário, autorize acesso a esse repositório.
3. Selecione **Flask** como Framework Preset, caso não seja detectado.
4. Mantenha a raiz do repositório como Root Directory. O `vercel.json` já define o Build Command: `python build.py`. Não configure um comando `flask run`.
5. Cadastre as variáveis abaixo antes de clicar em **Deploy**. Se configurar depois, faça um novo deploy para aplicar.

| Variável | Valor |
| --- | --- |
| `DATABASE_URL` | URL PostgreSQL do Neon, com pooling e SSL habilitados |
| `SECRET_KEY` | Chave aleatória fixa, gerada pelo comando abaixo |

Para gerar `SECRET_KEY` no computador:

```powershell
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
```

Copie o resultado para a variável da Vercel. Use a mesma chave em todas as instâncias da aplicação para o login funcionar. Cadastre as variáveis em **Production** e, se for usar links de preview, também em **Preview**.

6. Clique em **Deploy** e abra o endereço HTTPS fornecido pela Vercel.

## 5. Conferir a publicação

- Abra o catálogo e verifique os cinco sabores e as ilustrações.
- Crie uma conta, adicione um cupcake ao carrinho e finalize.
- Confira o pedido, saia e entre novamente: ele deve permanecer no histórico.
- Teste a exclusão do pedido.

## Arquivos da hospedagem

- `wsgi.py`: exporta a aplicação Flask reconhecida pela Vercel.
- `.python-version`: seleciona Python 3.13.
- `config.py`: lê a conexão e a chave do ambiente; exige PostgreSQL e chave na Vercel.
- `public/static/`: contém os arquivos CSS/JS do site e deve ser enviado ao GitHub. A Vercel os publica pelo CDN; no desenvolvimento local, o Flask serve esses mesmos arquivos.
- `build.py`: verifica a presença dos arquivos públicos antes da publicação.
- `vercel.json`: framework, comando de build e configuração da função.

O build não conecta ao banco. A aplicação na Vercel não cria tabelas durante sua inicialização; por isso o passo 2 é necessário. Os cookies usam HTTPS na Vercel.

Se a publicação falhar, consulte os logs do build. Se o site mostrar erro ao abrir catálogo ou pedidos, consulte **Runtime Logs** e confira a inicialização do banco e as variáveis. Nunca publique a URL com a senha junto com uma mensagem de erro.

## Referências

- Flask na Vercel: https://vercel.com/docs/frameworks/backend/flask
- Conexão Neon: https://neon.com/docs/connect/connect-from-any-app
- Conexões com pooling: https://neon.com/docs/connect/connection-pooling
