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
import random
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

    # =========================
    # CACHE AQUI 🔥
    # =========================
    date_api = selected_date.strftime('%Y-%m-%d')
    cache_key = f"apod-{date_api}"

    data = cache.get(cache_key)

    if not data:
        url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&date={date_api}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            cache.set(cache_key, data, 60 * 60 * 24)  # 24h
        else:
            data = None

    # ✅ CONTEXT PADRÃO (sempre existe, evita crash)
    context = {
        'history': None,
        'total_favorites': Favorite.objects.count(),
        'total_history': History.objects.count(),
    }

    # =========================
    # AGORA USA data (não response)
    # =========================
    if data:

        media_type = data.get("media_type")

        image_url = None
        video_url = None

        if media_type == "image":
            image_url = data.get("hdurl") or data.get("url")

        elif media_type == "video":
            video_url = data.get("url")

        translator = GoogleTranslator(source='en', target='pt')
        title_pt = translator.translate(data['title'])
        explanation_pt = translator.translate(data['explanation'])

        download_name = f"{slugify(title_pt)}.jpg"

        hist, _ = History.objects.get_or_create(
            title=title_pt,
            url=image_url or video_url,
            apod_date=selected_date
        )

        context.update({
            'title': title_pt,
            'image_url': image_url,
            'video_url': video_url,
            'explanation': explanation_pt,
            'date': selected_date.strftime('%d/%m/%Y'),
            'date_input_format': selected_date.strftime('%Y-%m-%d'),
            'prev_date': prev_date,
            'next_date': next_date,
            'error': '',
            'download_name': download_name,
            'history': hist,
        })

    else:
        context['error'] = 'Erro ao carregar a APOD.'

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

        # ⭐ contador atualizado
        total_favorites = Favorite.objects.count()

        # ⭐ resposta AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                "id": fav.id,
                "title": fav.title,
                "url": fav.url,
                "date": fav.date.strftime("%d/%m/%Y"),
                "created": created,
                "total_favorites": total_favorites
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

# =========================
# APOD ALEATÓRIA (RANDOM + CACHE)
# =========================
def random_apod(request):
    start_date = date(1995, 6, 16)
    end_date = date.today()
    delta_days = (end_date - start_date).days
    random_days = random.randint(0, delta_days)
    random_date = start_date + timedelta(days=random_days)

    # =========================
    # CACHE 🔥
    # =========================
    date_api = random_date.strftime('%Y-%m-%d')
    cache_key = f"apod-{date_api}"

    data = cache.get(cache_key)

    if not data:
        url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&date={date_api}"
        response = requests.get(url)

        if response.status_code != 200:
            return JsonResponse({"error": "Erro ao carregar APOD"}, status=500)

        data = response.json()
        cache.set(cache_key, data, 60 * 60 * 24)  # 24h

    # =========================
    # resto igual ao seu código
    # =========================
    media_type = data.get("media_type")

    image_url = None
    video_url = None

    if media_type == "image":
        image_url = data.get("hdurl") or data.get("url")
    elif media_type == "video":
        video_url = data.get("url")

    translator = GoogleTranslator(source='en', target='pt')
    title_pt = translator.translate(data['title'])
    explanation_pt = translator.translate(data.get('explanation', ''))

    hist, created = History.objects.get_or_create(
        title=title_pt,
        url=image_url or video_url,
        apod_date=random_date
    )

    if request.GET.get("ajax"):
        prev_date = (random_date - timedelta(days=1)).strftime("%Y-%m-%d")
        next_date = (random_date + timedelta(days=1)).strftime("%Y-%m-%d")

        return JsonResponse({
            "title": title_pt,
            "image_url": image_url,
            "video_url": video_url,
            "explanation": explanation_pt,
            "date": random_date.strftime("%d/%m/%Y"),
            "date_iso": random_date.strftime("%Y-%m-%d"),
            "history_id": hist.id,
            "prev_date": prev_date,
            "next_date": next_date,
        })

    return redirect(f"/?date={date_api}")

# =========================
# CURTIDAS
# =========================

def liked_list(request):
    order = request.GET.get("order", "likes")  # padrão = ranking

    liked_qs = History.objects.filter(likes__gt=0)

    if order == "recent":
        liked_qs = liked_qs.order_by('-visited_at')
    else:
        liked_qs = liked_qs.order_by('-likes')

    paginator = Paginator(liked_qs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "explorer/liked.html", {
        "histories": page_obj,
        "order": order
    })