from flask import Flask, request, jsonify
from shazamio import Shazam
import asyncio

app = Flask(__name__)
shazam = Shazam()

async def search_track(query, limit):
    result = await shazam.search_track(query=query)
    tracks = result.get('tracks', {}).get('hits', [])
    return tracks[:limit]

async def search_artist(query, limit):
    result = await shazam.search_artist(query=query)
    artists = result.get('artists', {}).get('hits', [])
    return artists[:limit]

async def recognize_song(audio_data):
    return await shazam.recognize_song(audio_data)

async def top_world_tracks(country_code, limit):
    result = await shazam.top_world_tracks(country_code=country_code)
    tracks = result.get('tracks', [])
    return tracks[:limit]

async def city_top_tracks(country_code, city_name, limit):
    result = await shazam.city_top_tracks(country_code=country_code, city_name=city_name)
    tracks = result.get('tracks', [])
    return tracks[:limit]

async def genre_world_tracks(genre_code, limit):
    result = await shazam.genre_world_tracks(genre_code=genre_code)
    tracks = result.get('tracks', [])
    return tracks[:limit]

async def related_tracks(track_id, limit):
    result = await shazam.related_tracks(track_id=track_id)
    tracks = result.get('tracks', [])
    return tracks[:limit]

@app.route('/search/track', methods=['POST'])
def search_track_route():
    data = request.get_json()
    query = data.get('query', '')
    limit = data.get('limit', 10)

    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    try:
        limit = int(limit)
    except ValueError:
        return jsonify({'error': 'Invalid limit value'}), 400

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tracks = loop.run_until_complete(search_track(query, limit))
    
    return jsonify(tracks)

@app.route('/search/artist', methods=['POST'])
def search_artist_route():
    data = request.get_json()
    query = data.get('query', '')
    limit = data.get('limit', 10)

    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    try:
        limit = int(limit)
    except ValueError:
        return jsonify({'error': 'Invalid limit value'}), 400

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    artists = loop.run_until_complete(search_artist(query, limit))
    
    return jsonify(artists)

@app.route('/recognize-song', methods=['POST'])
def recognize_song_route():
    audio_data = request.files.get('audio')

    if not audio_data:
        return jsonify({'error': 'Audio file is required'}), 400

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        song_data = loop.run_until_complete(recognize_song(audio_data))
        return jsonify(song_data)
    except Exception as e:
        return jsonify({'error': f'Error recognizing song: {str(e)}'}), 500

@app.route('/top_world_tracks', methods=['POST'])
def get_top_world_tracks_route():
    data = request.get_json()
    country_code = data.get('country_code', '')
    limit = data.get('limit', 10)
    
    if not country_code:
        return jsonify({'error': 'Country code is required'}), 400

    try:
        limit = int(limit)
    except ValueError:
        return jsonify({'error': 'Invalid limit value'}), 400

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    top_tracks = loop.run_until_complete(top_world_tracks(country_code.upper(), limit))
    return jsonify(top_tracks)

@app.route('/city_top_tracks', methods=['POST'])
def get_city_top_tracks_route():
    data = request.get_json()
    country_code = data.get('country_code', '')
    city_name = data.get('city_name', '')
    limit = data.get('limit', 10)
    
    if not country_code or not city_name:
        return jsonify({'error': 'Country code and city name are required'}), 400

    try:
        limit = int(limit)
    except ValueError:
        return jsonify({'error': 'Invalid limit value'}), 400

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    top_tracks = loop.run_until_complete(city_top_tracks(country_code.upper(), city_name.replace(" ", ""), limit))
    return jsonify(top_tracks)

@app.route('/genre_world_tracks', methods=['POST'])
def get_genre_world_tracks_route():
    data = request.get_json()
    genre_code = data.get('genre_code', '')
    limit = data.get('limit', 10)
    
    if not genre_code:
        return jsonify({'error': 'Genre code is required'}), 400

    try:
        limit = int(limit)
    except ValueError:
        return jsonify({'error': 'Invalid limit value'}), 400

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    top_tracks = loop.run_until_complete(genre_world_tracks(genre_code, limit))
    return jsonify(top_tracks)

@app.route('/related_tracks', methods=['POST'])
def related_tracks_route():
    data = request.get_json()
    track_id = data.get('track_id', '')
    limit = data.get('limit', 10)

    if not track_id:
        return jsonify({'error': 'Track ID is required'}), 400

    try:
        limit = int(limit)
    except ValueError:
        return jsonify({'error': 'Invalid limit value'}), 400

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    related_tracks = loop.run_until_complete(related_tracks(track_id, limit))
    return jsonify(related_tracks)

def run_flask_app():
    app.run(debug=True, use_reloader=False)

if __name__ == '__main__':
    run_flask_app()
