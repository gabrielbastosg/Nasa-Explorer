# 🚀 NASA Explorer

Aplicação web feita com Django que consome a API APOD da NASA para exibir a **Astronomy Picture of the Day**.

O usuário pode visualizar, curtir, favoritar, baixar imagens e acompanhar o histórico de navegação — tudo com uma interface moderna e interações AJAX (sem recarregar a página).

---

## 🌌 Demonstração

Principais telas:
- Página principal (APOD diária)
- Favoritos
- Histórico
- Ranking de curtidas

---

## 🎯 Objetivos do projeto

Este projeto foi criado para praticar:

- Consumo de API externa
- Django (Models, Views, Templates)
- Banco de dados SQLite
- AJAX com JavaScript (fetch API)
- Paginação
- UX sem reload
- Organização de projeto real
- Versionamento com Git/GitHub

---

## 🛠 Tecnologias

- Python
- Django
- SQLite
- HTML5
- CSS3
- JavaScript (Fetch/AJAX)
- Bootstrap

---

## ✨ Funcionalidades

### 📸 APOD
- Foto astronômica do dia
- Navegação por datas
- Imagem aleatória
- Download da imagem

### ⭐ Favoritos
- Adicionar/remover favoritos
- Atualização via AJAX (sem reload)
- Página dedicada com paginação
- Busca por título

### 👍 Curtidas
- Sistema de likes por imagem
- Atualização via AJAX
- Página de ranking (mais curtidas primeiro)
- Layout em grid responsivo

### 📜 Histórico
- Registro automático de visitas
- Filtro por data
- Busca por título
- Limpar histórico

### 🎨 Interface
- Tema espacial (galáxia)
- Cards com hover effects
- Transições suaves
- Layout responsivo

---

## ▶ Como rodar localmente

### 1. Clonar o repositório
```bash
git clone https://github.com/gabrielbastosg/Nasa-Explorer.git
cd Nasa-Explorer
2. Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

3. Instalar dependências
pip install -r requirements.txt

4. Criar arquivo .env

Crie um arquivo .env na raiz:

API_KEY=SUA_CHAVE_DA_NASA

Pegue sua chave gratuita em:
https://api.nasa.gov

5. Rodar o projeto
python manage.py migrate
python manage.py runserver

📚 Estrutura do projeto
explorer/
 ├─ models.py
 ├─ views.py
 ├─ urls.py
 ├─ templates/
 ├─ static/

