from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
import os
import requests
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
from django.core.cache import cache
from datetime import datetime, timedelta, date
from django.conf import settings
from explorer.models import Favorite, History  
from django.core.paginator import Paginator
import unicodedata
from django.utils.text import slugify 
from django.views.decorators.csrf import csrf_exempt
# =========================
# Carregando .env
# =========================
load_dotenv()
API_KEY = os.getenv('API_KEY')


# =========================
# HOME
# =========================
def home(request):
    return HttpResponse("🚀 Nasa Explorer online!")


# =========================
# APOD normal
# =========================
def apod_view(request):
    date_str = request.GET.get('date')

    if date_str:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        selected_date = datetime.today()

    prev_date = (selected_date - timedelta(days=1)).strftime("%Y-%m-%d")
    next_date = (selected_date + timedelta(days=1)).strftime("%Y-%m-%d")

    url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&date={selected_date.strftime('%Y-%m-%d')}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        translator = GoogleTranslator(source='en', target='pt')
        title_pt = translator.translate(data['title'])
        explanation_pt = translator.translate(data['explanation'])

        # ✅ gerar nome do arquivo para download
        download_name = f"{slugify(title_pt)}.jpg"

        context = {
            'title': title_pt,
            'image_url': data.get('url'),
            'explanation': explanation_pt,
            'date': selected_date.strftime('%d/%m/%Y'),
            'date_input_format': selected_date.strftime('%Y-%m-%d'),
            'prev_date': prev_date,
            'next_date': next_date,
            'error': '',
            'download_name': download_name  # adiciona aqui
        }

        # salvar histórico
        hist, created = History.objects.get_or_create(
            title=title_pt,
            url=data.get('url'),
            apod_date=selected_date
        )

        context['history'] = hist

        # estatísticas
        context.update({
            'total_favorites': Favorite.objects.count(),
            'total_history': History.objects.count(),
            'latest_favorite': Favorite.objects.order_by('-id').first(),
        })

    else:
        context = {'error': 'Erro ao carregar a APOD.'}

    return render(request, 'explorer/apod.html', context)

# =========================
# ADICIONAR FAVORITO (AJAX READY)
# =========================
def add_favorite(request):
    if request.method == "POST":
        title = request.POST.get("title")
        url = request.POST.get("url")

        fav, created = Favorite.objects.get_or_create(
            title=title,
            url=url,
            defaults={'date': date.today()}
        )

        # Se for AJAX, retorna JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                "id": fav.id,
                "title": fav.title,
                "url": fav.url,
                "date": fav.date.strftime("%d/%m/%Y"),
                "created": created
            })

    return redirect(request.META.get("HTTP_REFERER", '/'))


# =========================
# LISTAR FAVORITOS
# =========================
def favorites_list(request):
    query = request.GET.get("q")

    favorites_qs = Favorite.objects.all().order_by('-id')

    # 🔥 busca sem acento
    if query:
        normalized_query = normalize(query)

        favorites_qs = [
            fav for fav in favorites_qs
            if normalized_query in normalize(fav.title)
        ]

    paginator = Paginator(favorites_qs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "explorer/favorites.html", {
        "favorites": page_obj,
        "query": query
    })
# =========================
# REMOVER FAVORITO
# =========================
def remove_favorite(request, fav_id):
    if request.method == "POST":
        fav = get_object_or_404(Favorite, id=fav_id)
        fav.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))


# =========================
# LISTAR HISTÓRICO
# =========================
def history_list(request):
    query = request.GET.get('q') or ''
    start_date = request.GET.get('start_date') or ''
    end_date = request.GET.get('end_date') or ''

    histories = History.objects.all().order_by('-visited_at')

    # 🔎 busca ignorando acento
    if query:
        normalized_query = normalize(query)

        histories = [
            h for h in histories
            if normalized_query in normalize(h.title)
        ]

    # 📅 filtros de data (só aplica se existir valor válido)
    if start_date:
        histories = [h for h in histories if str(h.apod_date) >= start_date]

    if end_date:
        histories = [h for h in histories if str(h.apod_date) <= end_date]

    # paginação
    paginator = Paginator(histories, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "explorer/history.html", {
        "histories": page_obj,
        "query": query,
        "start_date": start_date,
        "end_date": end_date,
    })

def normalize(text):
    if not text:
        return ""
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ).lower()

def limpar_historico(request):
    """
    Limpa todo o historico de APODs
    """
    if request.method == "POST":
        History.objects.all().delete()

        # Se for AJAX, retorna JSON com sucesso
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True})

        # Se não for AJAX, redireciona
        return redirect("history_list")
    return redirect("history_list")

def like_apod(request, history_id):
    if request.method == "POST":

        session_key = f"liked_{history_id}"

        # já curtiu nesta sessão → não soma
        if request.session.get(session_key):
            hist = get_object_or_404(History, id=history_id)
            return JsonResponse({"likes": hist.likes})

        hist = get_object_or_404(History, id=history_id)
        hist.likes += 1
        hist.save()

        # marca como curtido
        request.session[session_key] = True

        return JsonResponse({"likes": hist.likes})