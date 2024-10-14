from django.shortcuts import render
from django.conf import settings
from .forms import MovieForm
from firebase_admin import firestore
import requests
# Initialize Firestore
db = firestore.client()

import requests

def scrape_movie_poster(movie_name, movie_year):
    api_key = settings.OMDB_API
    search_url = f"http://www.omdbapi.com/?t={movie_name}&y={movie_year}&apikey={api_key}"

    response = requests.get(search_url)

    if response.status_code != 200:
        print("Error fetching data from OMDb API")
        return None
    
    data = response.json()

    if data['Response'] == 'True':
        poster_url = data['Poster']  # Get the poster URL
        return poster_url
    else:
        print("Movie not found")
        return None

def home(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            year = form.cleaned_data['year']
            rating = float(form.cleaned_data['rating'])  # Convert Decimal to float
            comments = form.cleaned_data['comments']

            # Scrape movie poster from Wikipedia
            poster_url = scrape_movie_poster(name, year)

            # Store movie details in Firestore
            db.collection('movies').add({
                'name': name,
                'year': year,
                'rating': rating,  # Firestore expects float
                'comments': comments,
                'poster_url': poster_url  # Store the poster URL in Firestore
            })

    form = MovieForm()  # Empty form for display
    # Retrieve all movies from Firestore
    movies = db.collection('movies').stream()
    movie_list = [doc.to_dict() for doc in movies]

    return render(request, 'index.html', {'form': form, 'movie_list': movie_list})
