🚀 NASA Explorer
Projeto Django consumindo a API APOD da NASA.

## Funcionalidades
- Foto astronômica do dia
- Histórico de visitas
- Favoritos
- Curtidas
- Download da imagem
- Botão de imagem aleatória com efeito fade suave (atualização dinâmica da APOD sem recarregar a página)

## Como rodar
1. Instalar dependências:

pip install -r requirements.txt


2. Criar arquivo `.env` com sua chave da NASA:

API_KEY=sua_chave_aqui


3. Rodar o servidor:

python manage.py runserver
