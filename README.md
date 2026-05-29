# ⚡ VoltIQ — Energy Intelligence System

Sistema de gestão de consumo de energia elétrica para pequenas empresas.

---

## 👥 Equipe

| Nome | Função |
|------|--------|
| João Vitor | Desenvolvedor — Banco de Dados |
| Clara | Product Owner — Backend Python |
| Guilherme | Scrum Master — Backend Python |
| Kaio | Desenvolvedor — Frontend |

```
## 📁 Estrutura do Projeto

```
voltiq/
│
├── backend/
│   ├── calculo.py          → calcula custo, status e variação
│   ├── conexao.py          → conexão com o banco de dados
│   ├── empresa.py          → operações de empresas
│   ├── leitura.py          → operações de leituras
│   ├── meta.py             → operações de metas
│   ├── main.py             → menu principal do sistema
│   └── servidor.py         → integração entre frontend e backend
│
├── banco/
│   └── banco_de_dados.sql  → script de criação do banco MySQL
│
├── front-end/
│   └── index2.html         → interface visual do sistema
│
├── modelagem/
│   ├── Conceitual_1.brM3   → modelo conceitual
│   └── Lógico_1.brM3       → modelo lógico
│
└── README.md
---

## 💻 Pré-requisitos

Antes de rodar o projeto, você precisa ter instalado:

- [Python 3.13](https://www.python.org/downloads/) — marcar **"Add Python to PATH"** na instalação
- [MySQL](https://dev.mysql.com/downloads/installer/) — anotar a senha criada durante a instalação
- [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) — para criar o banco
- [VS Code](https://code.visualstudio.com/) — para rodar o servidor

---

## 🚀 Como instalar e rodar

### Passo 1 — Baixar os arquivos

Baixe todos os arquivos do repositório e coloque dentro de uma pasta chamada `voltiq` na Área de Trabalho.

---

### Passo 2 — Criar o banco de dados

1. Abra o **MySQL Workbench**
2. Clique na conexão **Local instance** para entrar
3. Digite sua senha do MySQL
4. No menu do topo clique em **File → Open SQL Script**
5. Selecione o arquivo `banco_de_dados.sql`
6. Clique no **raio ⚡** (ou Ctrl+Shift+Enter) para executar
7. Aguarde a mensagem verde de sucesso

---

### Passo 3 — Configurar a senha do MySQL

1. Abra o arquivo `conexao.py` no VS Code
2. Encontre essa linha:

```python
password="",
```

3. Coloque a sua senha do MySQL entre as aspas:

```python
password="suasenha123",
```

> ⚠️ Se você instalou o MySQL sem senha, deixe as aspas vazias: `password=""`

4. Salve o arquivo com **Ctrl+S**

---

### Passo 4 — Instalar a biblioteca do MySQL

1. Abra o VS Code
2. Abra o terminal: **Terminal → New Terminal**
3. Digite e aperte Enter:

```
pip install mysql-connector-python
```

4. Aguarde aparecer **"Successfully installed"**

> Se der erro, tente:
> ```
> python -m pip install mysql-connector-python --user
> ```

---

### Passo 5 — Abrir a pasta no VS Code

1. No VS Code clique em **File → Open Folder**
2. Selecione a pasta `voltiq`
3. Clique em **Selecionar Pasta**

---

### Passo 6 — Rodar o servidor

1. Abra o terminal no VS Code: **Terminal → New Terminal**
2. Digite e aperte Enter:

```
python servidor.py
```

3. Deve aparecer:

```
VoltIQ -- Servidor iniciado!
API rodando em: http://localhost:8000
Abra o index.html no navegador para usar o sistema
Para parar: Ctrl + C
```

> ⚠️ **Deixe essa janela aberta!** Se fechar o terminal, o sistema para de funcionar.

---

### Passo 7 — Abrir o sistema

1. Vá na pasta `voltiq` na Área de Trabalho
2. Dê **dois cliques** no arquivo `index.html`
3. Ele abre no navegador automaticamente
4. Faça o login:
   - **Usuário:** admin
   - **Senha:** 1234

---

## 📖 Como usar o sistema

### Dashboard
Tela inicial com resumo geral — total de empresas, leituras e kWh consumidos.

### Empresas
- Clique em **+ Nova Empresa** para cadastrar
- Preencha: nome, CNPJ, cidade e tarifa (R$/kWh)
- Use os botões **Editar** e **Excluir** para gerenciar
- Clique em **Exportar CSV** para baixar a lista em planilha

### Leituras
- Selecione a empresa no menu
- Clique em **+ Nova Leitura**
- Preencha o mês (formato: 2026-06) e o kWh consumido

### Metas
- Selecione a empresa no menu
- Clique em **+ Nova Meta**
- Preencha o mês e o limite de kWh

### Relatório
- Selecione a empresa e o mês
- Clique em **Gerar Relatório**
- O sistema mostra: consumo, meta, custo, variação e status
- Clique em **Baixar PDF** para salvar o relatório

### Gráficos
- Selecione a empresa
- Visualize o histórico de consumo em barras e o custo em linha

### Comparar
- Ranking automático de todas as empresas por consumo total

---

## 🚦 Status do sistema

| Status | Condição | Cor |
|--------|----------|-----|
| ✅ OK | Consumo abaixo de 80% da meta | Verde |
| ⚠️ ATENÇÃO | Consumo entre 80% e 100% da meta | Laranja |
| 🚨 CRÍTICO | Consumo igual ou acima da meta | Vermelho |

---

## 🔄 Todo dia que for usar

1. Abra o VS Code
2. Abra o terminal (**Terminal → New Terminal**)
3. Digite: `python servidor.py`
4. Abra o `index.html` no navegador
5. Login: **admin** / **1234**

---

## ❓ Problemas comuns

**"pip não é reconhecido"**
→ Reinstale o Python marcando a opção **"Add Python to PATH"**

**"No module named mysql"**
→ Execute: `python -m pip install mysql-connector-python --user`

**"Erro ao carregar empresas"**
→ Verifique se a senha no `conexao.py` está correta e se o servidor está rodando

**"Não conectou ao banco"**
→ Verifique se o MySQL está rodando e se o banco `voltiq` foi criado

---

## 🛠️ Tecnologias

- **Python 3.13** — lógica e backend
- **MySQL** — banco de dados
- **HTML + CSS + JavaScript** — interface visual

---

## 📅 ExpoTech 2026
