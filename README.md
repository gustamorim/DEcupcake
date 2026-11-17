# DEcupcake

Estrutura inicial de uma loja de cupcakes com Python, Flask, SQLite, SQLAlchemy, HTML, CSS e JavaScript. Projeto local em MVC: models cuidam dos dados, controllers recebem as requisições e templates são as views.

## Executar no Windows (PowerShell)

Instale Python 3.10 ou superior pelo instalador oficial de https://www.python.org/downloads/windows/ e habilite **Add Python to PATH**. Abra um novo PowerShell após instalar.

```powershell
cd C:\Users\lgamo\Desktop\cupcake
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app run run --debug
```

Acesse **http://127.0.0.1:5000**. Use `Ctrl+C` para parar. Se `py` não estiver disponível, use `python -m venv .venv` no segundo comando.

Se o Python estiver instalado, mas nem `py` nem `python` funcionarem, use o caminho completo do executável. Nesta máquina foi encontrada a instalação abaixo:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" -m venv .venv
```

Os comandos usam diretamente o Python do ambiente virtual; não é necessário ativá-lo nem alterar a política de execução do PowerShell. Em execuções futuras, basta entrar na pasta e executar o último comando.

O banco `instance/cupcake.db` e cinco produtos de exemplo são criados automaticamente ao iniciar a aplicação. Para inicializar explicitamente:

```powershell
.\.venv\Scripts\python.exe -m flask --app run init-db
```

Esse comando preserva os dados existentes e insere apenas os sabores de exemplo que ainda não existem, usando o slug como identificador. Assim, bancos com os três produtos originais recebem os dois novos sem apagar contas ou alterar produtos existentes. `create_all()` cria tabelas ausentes, mas não migra tabelas existentes; mudanças futuras no schema precisarão de migrações.

## Organização

```text
cupcake/
├── app/
│   ├── __init__.py           # Fábrica da aplicação e configuração inicial
│   ├── extensions.py         # Instância compartilhada do SQLAlchemy
│   ├── seed.py               # Produtos de exemplo
│   ├── models/
│   │   ├── product.py        # Modelo Product; preço decimal
│   │   ├── user.py           # Usuário e hash da senha
│   │   └── order.py          # Pedido e itens com preço da compra
│   ├── services/cart.py      # Quantidades, itens e total do carrinho
│   ├── auth.py               # Sessão, proteção de rotas e CSRF
│   ├── controllers/         # Blueprints e rotas por responsabilidade
│   ├── templates/           # Views Jinja, base e componentes compartilhados
│   │   ├── base.html
│   │   ├── placeholder.html
│   │   ├── components/
│   │   ├── home/
│   │   ├── catalog/
│   │   ├── cart/
│   │   ├── checkout/
│   │   ├── orders/
│   │   └── account/
│   └── static/
│       ├── css/              # style.css e shop.css
│       └── js/main.js
├── instance/                # SQLite gerado em execução (ignorado pelo Git)
├── config.py
├── run.py
├── requirements.txt
└── .gitignore
```

## Telas e estágio atual

| Tela | Rota | Implementação |
| --- | --- | --- |
| Início | `/` | Layout responsivo, destaques consultados no SQLite e menu mobile |
| Catálogo | `/catalogo` | Cinco sabores com detalhes e botão de adicionar |
| Produto | `/produto/<slug>` | Detalhes, quantidade e adicionar ao carrinho |
| Carrinho | `/carrinho` | Itens, edição de quantidades, remoção, total e finalizar compra |
| Checkout | `/checkout` | Redireciona para o carrinho, onde a compra é finalizada |
| Pedidos | `/pedidos` | Histórico do usuário, itens, total e exclusão |
| Conta | `/conta` | Área autenticada com nome, e-mail e logout |

Exemplo de produto: http://127.0.0.1:5000/produto/chocolate-dos-sonhos

As ilustrações SVG são locais e o frontend não depende de CDN. A finalização registra o pedido; pagamento e entrega não estão integrados nesta etapa.

## Catálogo, carrinho e pedidos

O catálogo contém chocolate, morango, baunilha, **pistache (verde)** e **mirtilo (lilás)**. Os três primeiros continuam em destaque na página inicial. É possível adicionar produtos pela página inicial, pelo catálogo ou pelos detalhes do produto.

1. Adicione cupcakes e abra o carrinho.
2. Ajuste a quantidade de cada sabor (1 a 99) usando **Atualizar**, ou use **Remover**.
3. Entre ou crie uma conta para finalizar. O carrinho é preservado durante o login/cadastro e você retorna para ele.
4. Clique em **Finalizar compra**. Um pedido é salvo no SQLite, o carrinho é esvaziado e a página **Meus pedidos** é aberta.
5. Use **Excluir pedido** para removê-lo e remover seus itens. Com JavaScript ativo, há uma confirmação antes da exclusão.

O carrinho fica na sessão do navegador e é limpo ao sair da conta. Pedidos ficam no banco e são visíveis apenas ao próprio usuário. Os valores são calculados no servidor com `Decimal`; nome e preço unitário são copiados para cada item do pedido para preservar o histórico. Um identificador único da compra impede pedidos duplicados em envios repetidos. Todas as alterações usam POST e validação CSRF.

## Cadastro e autenticação

- Cadastro: http://127.0.0.1:5000/conta/registro
- Login: http://127.0.0.1:5000/conta/login (também acessível por **Minha conta** no menu)
- Após o cadastro, o usuário entra automaticamente. A conta e a tela de pedidos exigem login.
- Logout: botão **Sair da conta**, enviado por POST com token CSRF.

O cadastro pede nome, e-mail, senha de 8 a 128 caracteres e confirmação. O e-mail é normalizado para minúsculas e tem restrição única no SQLite. A senha é armazenada como hash scrypt do Werkzeug. Os formulários validam os dados também no servidor e têm proteção CSRF. A tabela `users` é criada automaticamente ao reiniciar a aplicação; os produtos existentes são preservados. Não há confirmação de e-mail nem recuperação de senha nesta etapa.

Configure uma chave secreta estável para manter as sessões após reiniciar o servidor. No PowerShell, gere uma chave uma vez e use o valor obtido na variável de ambiente `SECRET_KEY` antes de executar o Flask. Não compartilhe nem versione esse valor:

```powershell
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
$env:SECRET_KEY = "cole-aqui-a-chave-gerada"
```

Sem `SECRET_KEY`, o projeto usa uma chave aleatória por processo e as sessões são encerradas após reiniciar o servidor. Em uma implantação HTTPS, configure também `SESSION_COOKIE_SECURE = True`.

Para executar os testes de autenticação, catálogo, carrinho e pedidos com banco temporário em memória:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Desenvolvimento

Para adicionar regras de negócio, edite os controllers; para persistência, os models; para apresentação, templates e static. Novos models devem ser importados em `app/models/__init__.py` para serem registrados antes da criação das tabelas.

O servidor com `--debug` é apenas para desenvolvimento local. Ao preparar uma implantação, configure `SECRET_KEY` no ambiente e utilize um servidor de produção.
