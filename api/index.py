from quart import Quart, request, jsonify
from shazamio import Shazam
import asyncio

app = Quart(__name__)
shazam = Shazam()

async def _search_and_limit(search_function, query, limit):
    """Helper function to perform search and apply limit."""
    result = await search_function(query=query)
    items = result.get(list(result.keys())[1], {}).get('hits', [])  # Dynamically access hits key
    return items[:limit]

@app.route('/search/track', methods=['POST'])
async def search_track_route():
    data = await request.get_json()
    query = data.get('query', '')
    limit = data.get('limit', 10)

    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    try:
        limit = int(limit)
    except ValueError:
        return jsonify({'error': 'Invalid limit value'}), 400

    tracks = await _search_and_limit(shazam.search_track, query, limit)
    return jsonify(tracks)

@app.route('/search/artist', methods=['POST'])
async def search_artist_route():
    data = await request.get_json()
    query = data.get('query', '')
    limit = data.get('limit', 10)

    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    try:
        limit = int(limit)
    except ValueError:
        return jsonify({'error': 'Invalid limit value'}), 400

    artists = await _search_and_limit(shazam.search_artist, query, limit)
    return jsonify(artists)

@app.route('/recognize-song', methods=['POST'])
async def recognize_song_route():
    audio_data = request.files.get('audio')

    if not audio_data:
        return jsonify({'error': 'Audio file is required'}), 400

    try:
        song_data = await shazam.recognize_song(audio_data)
        return jsonify(song_data)
    except Exception as e:
        return jsonify({'error': f'Error recognizing song: {str(e)}'}), 500

@app.route('/top_world_tracks/<country_code>', methods=['GET'])
async def get_top_world_tracks_route(country_code):
    limit = request.args.get('limit', 10)
    try:
        limit = int(limit)
    except ValueError:
        return jsonify({'error': 'Invalid limit value'}), 400
    top_tracks = await _search_and_limit(shazam.top_world_tracks, country_code.upper(), limit)
    return jsonify(top_tracks)

@app.route('/city_top_tracks/<country_code>/<city_name>', methods=['GET'])
async def get_city_top_tracks_route(country_code, city_name):
    limit = request.args.get('limit', 10)
    try:
        limit = int(limit)
    except ValueError:
        return jsonify({'error': 'Invalid limit value'}), 400
    top_tracks = await _search_and_limit(shazam.city_top_tracks, f'{city_name.replace(" ", "")},{country_code.upper()}', limit)
    return jsonify(top_tracks)

@app.route('/genre_world_tracks/<genre_code>', methods=['GET'])
async def get_genre_world_tracks_route(genre_code):
    limit = request.args.get('limit', 10)
    try:
        limit = int(limit)
    except ValueError:
        return jsonify({'error': 'Invalid limit value'}), 400
    top_tracks = await _search_and_limit(shazam.genre_world_tracks, genre_code, limit)
    return jsonify(top_tracks)

@app.route('/related_tracks/<track_id>', methods=['GET'])
async def related_tracks_route(track_id):
    limit = request.args.get('limit', 10)
    try:
        limit = int(limit)
        track_id = int(track_id)
    except ValueError:
        return jsonify({'error': 'Invalid limit or track_id value'}), 400
    related_tracks = await _search_and_limit(shazam.related_tracks, track_id, limit)
    return jsonify(related_tracks)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
