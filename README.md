
## 🏸 ** Badminton e Parabadminton** - README

### 📌 **Descrição**
Este sistema é uma plataforma para gerenciar torneios de **Badminton e Parabadminton**, permitindo que usuários acompanhem partidas, classificação, galeria de fotos e vídeos, além de um painel administrativo para gerenciar competições.

---

## 🚀 **Instalação e Configuração**
### **1️⃣ Pré-requisitos**
Antes de rodar o projeto, você precisa ter instalado:
- **Python 3.8+**
- **MySQL**
- **Flask**
- **Virtual Environment**
- **Dependências listadas no `requirements.txt`**

### **2️⃣ Criar e Ativar o Ambiente Virtual**
No terminal, execute os comandos:

```bash
python -m venv env
```

Ative o ambiente virtual:

- **Windows (PowerShell)**:
  ```powershell
  .\env\Scripts\activate
  ```

- **Mac/Linux**:
  ```bash
  source env/bin/activate
  ```

### **3️⃣ Instalar Dependências**
Instale todas as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

---

## 📂 **Estrutura do Projeto**
```
torneio_badminton/
│
├── templates/             # Arquivos HTML
│   ├── base.html          # Layout geral
│   ├── index.html         # Página inicial
│   ├── partidas.html      # Lista de partidas
│   ├── classificacao.html # Ranking de jogadores
│   ├── galeria.html       # Fotos e vídeos
│   ├── historia.html      # História do Badminton e Parabadminton
│   ├── dashboard.html     # Painel administrativo
│   ├── login.html         # Página de login
│   ├── registro.html      # Cadastro de usuários
│
├── static/                # Arquivos CSS e JS
│   ├── styles.css         # Estilos gerais
│   ├── scripts.js         # JavaScript interativo
│
├── app.py                 # Código principal do Flask
├── config.py              # Configurações gerais
├── setup.sql              # Script do banco de dados
├── requirements.txt       # Dependências do Python
├── README.md              # Documentação do projeto
```

---

## ⚙️ **Configuração do Banco de Dados**
1. **Crie o banco de dados e tabelas**:
```sql
CREATE DATABASE torneio_badminton;
USE torneio_badminton;
```

2. **Execute `setup.sql`** para criar todas as tabelas:
```bash
mysql -u root -p < setup.sql
```

---

## 🏆 **Funcionalidades**
✅ **Gerenciamento de Partidas** - Cadastro e exibição de partidas por categoria.  
✅ **Classificação Dinâmica** - Ranking atualizado dos jogadores.  
✅ **Galeria de Fotos e Vídeos** - Destaques dos melhores do ano.  
✅ **História do Badminton** - Informação sobre a origem do esporte.  
✅ **Painel Administrativo** - Controle total para administradores.  
✅ **Gráficos Interativos** - Estatísticas visuais sobre partidas.  
✅ **Notificações sobre torneios** - Alertas de eventos futuros.  
✅ **Gestão de Usuários** - Controle de permissões e edição de jogadores.  
✅ **Compartilhamento Social** - Divulgação de resultados nas redes sociais.  

---

## 🏃‍♂️ **Rodando o Sistema**
1. **Inicie o servidor Flask**:
```bash
python app.py
```

2. **Acesse o sistema no navegador**:
```bash
http://127.0.0.1:5000/
```

---

## 🔐 **Administração**
- Apenas **administradores** podem acessar o **Dashboard** (`/dashboard`).
- Para transformar um usuário em **administrador**, use:
```sql
UPDATE usuarios SET tipo='administrador' WHERE usuario='nome_do_usuario';
```

---

## 🌍 **Expansões Futuras**
- 📊 **Sistema de votação para melhores jogadores**  
- 🎭 **Tema personalizado para usuários**  
- 🎮 **Integração com APIs de pontuação**  
- 🏅 **Ranking internacional de jogadores**

---

## 📧 **Contato**
Caso tenha dúvidas ou sugestões, entre em contato! 🚀🏸  

