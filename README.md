🚀 NASA Explorer

Aplicação web feita com Django que consome a API Astronomy Picture of the Day (APOD) da NASA para exibir imagens e vídeos astronômicos diariamente.

O usuário pode visualizar, curtir, favoritar, baixar imagens e acompanhar o histórico de navegação — tudo com uma interface moderna e interações AJAX (sem recarregar a página).

🌐 Demonstração

Principais telas da aplicação:

📸 Screenshots
Tela inicial




Tela de favoritos




Tela de histórico




🎯 Objetivos do projeto

Este projeto foi criado para praticar conceitos importantes de desenvolvimento web:

Consumo de API externa

Estrutura de aplicações com Django

Models, Views e Templates

Banco de dados SQLite

Requisições assíncronas com AJAX / Fetch API

Paginação de dados

Interface dinâmica sem reload

Organização de projetos reais

Versionamento com Git e GitHub

🛠 Tecnologias

Python

Django

SQLite

HTML5

CSS3

JavaScript

Fetch API / AJAX

Bootstrap

✨ Funcionalidades
📸 APOD

Exibição da Astronomy Picture of the Day

Navegação por datas

Imagem aleatória do espaço

Download da imagem

Caso o conteúdo seja um vídeo do YouTube, ele é exibido no player embutido.
Alguns vídeos podem apresentar Erro 153 devido a restrições do YouTube — nesses casos é exibido um botão "Assistir no YouTube".

⭐ Favoritos

Adicionar e remover imagens favoritas

Atualização dinâmica via AJAX

Página dedicada com paginação

Busca por título

👍 Curtidas

Sistema de likes por imagem

Atualização sem recarregar a página

Página de ranking com imagens mais curtidas

Layout em grid responsivo

📜 Histórico

Registro automático de visitas

Filtro por data

Busca por título

Opção para limpar histórico

🎨 Interface

Tema espacial inspirado em galáxias

Cards com hover effects

Transições suaves

Layout responsivo

📂 Estrutura do projeto
nasa-explorer/
│
├── config/          # Configurações do Django
├── explorer/        # App principal (models, views, templates)
├── screenshots/     # Imagens usadas no README
├── staticfiles/     # Arquivos estáticos coletados
│
├── manage.py
├── requirements.txt
├── README.md
└── .env
▶ Como rodar o projeto localmente
1. Clonar o repositório
git clone https://github.com/gabrielbastosg/Nasa-Explorer.git
cd Nasa-Explorer
2. Criar ambiente virtual
python -m venv .venv

Linux / Mac

source .venv/bin/activate

Windows

.venv\Scripts\activate
3. Instalar dependências
pip install -r requirements.txt
4. Criar arquivo .env

Crie um arquivo .env na raiz do projeto:

API_KEY=SUA_CHAVE_DA_NASA

Você pode obter uma chave gratuita em:

https://api.nasa.gov

5. Rodar o projeto
python manage.py migrate
python manage.py runserver

Depois acesse:

http://127.0.0.1:8000
📌 Aprendizados

Durante o desenvolvimento deste projeto, pratiquei conceitos importantes como:

consumo de APIs externas

cache de requisições

manipulação de dados em Django

comunicação entre backend e frontend com AJAX

organização de um projeto web completo

👨‍💻 Autor

Projeto desenvolvido por Gabriel Bastos como parte dos estudos em desenvolvimento web com Python e Django.
