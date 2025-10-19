from django.shortcuts import render, get_object_or_404
from .models import Movie, Series, Episode
from django.http import FileResponse
import os, zipfile
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after registration
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    movies = Movie.objects.all()
    series = Series.objects.all()
    return render(request, 'core/home.html', {'movies': movies, 'series': series})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'core/movie_detail.html', {'movie': movie})

def series_detail(request, pk):
    series = get_object_or_404(Series, pk=pk)
    episodes = Episode.objects.filter(series=series)
    return render(request, 'core/series_detail.html', {'series': series, 'episodes': episodes})

def download_series_zip(request, series_id):
    series = get_object_or_404(Series, pk=series_id)
    episodes = Episode.objects.filter(series=series)

    zip_filename = f"{series.title.replace(' ', '_')}.zip"
    zip_path = os.path.join(settings.MEDIA_ROOT, 'zips', zip_filename)
    os.makedirs(os.path.dirname(zip_path), exist_ok=True)

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for ep in episodes:
            file_path = ep.episode_file.path
            arcname = os.path.basename(file_path)
            zipf.write(file_path, arcname)

    return FileResponse(open(zip_path, 'rb'), as_attachment=True, filename=zip_filename)
