# 🚀 NASA Explorer

Aplicação web desenvolvida com Django que consome a API APOD da NASA para exibir a foto astronômica do dia.

O usuário pode curtir, favoritar, baixar imagens e manter um histórico de navegação.

## 🌌 Sobre o projeto

Este projeto foi criado para praticar:
- Consumo de API externa
- Django MVC (models, views, templates)
- Banco de dados
- Sistema de likes/favoritos
- Manipulação dinâmica com JavaScript
- Versionamento com Git

API utilizada: NASA APOD (Astronomy Picture of the Day)

## 🛠 Tecnologias
- Python
- Django
- SQLite
- HTML/CSS/JS
- Bootstrap

## ✨ Funcionalidades
- 📅 Foto astronômica do dia
- 🔀 Imagem aleatória
- ❤️ Curtidas (likes)
- ⭐ Favoritos
- 🕘 Histórico de visitas
- ⭐ Favoritar (AJAX)
- 👍 Curtir imagens (AJAX)
- 📜 Histórico automático de visitas
- 🎲 APOD aleatória com transição suave
- 📊 Página de ranking de curtidas
- 🔍 Busca nos favoritos e histórico
- 📱 Layout responsivo em grid
- ⬇ Download da imagem

## ▶ Como rodar localmente

```bash
git clone https://github.com/gabrielbastosg/Nasa-Explorer.git
cd Nasa-Explorer

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
