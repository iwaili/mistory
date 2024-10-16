from django.shortcuts import render
from django.conf import settings
from .forms import MovieForm
from firebase_admin import firestore
import requests

# Initialize Firestore
db = firestore.client()

# Define the password (for example purposes, this should be more secure in real-world apps)
REQUIRED_PASSWORD = "sexc"  # Replace with your actual password

def scrape_movie_poster(movie_name, movie_year):
    api_key = settings.OMDB_API
    search_url = f"http://www.omdbapi.com/?t={movie_name}&y={movie_year}&apikey={api_key}"

    response = requests.get(search_url, timeout=5)  # Add a timeout to prevent long waits

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
    print("Home view accessed")  # Debug print
    #db = initialize_firestore()  # Initialize Firestore
    if db is None:
        print("Firestore initialization failed")
        return render(request, 'index.html', {'form': MovieForm(), 'movie_list': [], 'error_message': 'Firestore not available.'})

    if request.method == 'POST':
        print("Request method is POST")  # Debug print
        form = MovieForm(request.POST)
        if form.is_valid():
            print("Form is valid")  # Debug print
            
            # Get form data
            name = form.cleaned_data['name']
            year = form.cleaned_data['year']
            rating = float(form.cleaned_data['rating'])
            comments = form.cleaned_data['comments']
            password = form.cleaned_data['password']

            # Check password
            if password == REQUIRED_PASSWORD:
                poster_url = scrape_movie_poster(name, year)

                # Try to add the movie to Firestore
                try:
                    db.collection('movies').add({
                        'name': name,
                        'year': year,
                        'rating': rating,
                        'comments': comments,
                        'poster_url': poster_url
                    })
                    print("Movie added to Firestore")  # Debug print
                except Exception as e:
                    print(f"Failed to add movie to Firestore: {e}")
                    return render(request, 'index.html', {'form': form, 'movie_list': [], 'error_message': 'Failed to add movie.'})
            else:
                return render(request, 'index.html', {'form': form, 'movie_list': [], 'error_message': 'Incorrect password'})

        else:
            print("Form is not valid")  # Debug print
    else:
        print("Request method is GET")  # Debug print
    
    # Attempt to retrieve movies from Firestore
    try:
        movies = db.collection('movies').stream()
        movie_list = [doc.to_dict() for doc in movies]
        print("Movies retrieved from Firestore")  # Debug print
    except Exception as e:
        print(f"Failed to retrieve movies: {e}")
        movie_list = []

    return render(request, 'index.html', {'form': MovieForm(), 'movie_list': movie_list})

