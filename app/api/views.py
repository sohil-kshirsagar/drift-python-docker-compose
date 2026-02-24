import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def health(request):
    return Response({'status': 'ok', 'service': 'drift-python-docker-compose'})


@api_view(['GET'])
def weather(request):
    """Get weather for a location using open-meteo API."""
    lat = request.query_params.get('lat', '37.7749')
    lon = request.query_params.get('lon', '-122.4194')

    resp = requests.get(
        'https://api.open-meteo.com/v1/forecast',
        params={
            'latitude': lat,
            'longitude': lon,
            'current_weather': 'true',
        },
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()

    current = data.get('current_weather', {})
    return Response({
        'latitude': lat,
        'longitude': lon,
        'temperature_c': current.get('temperature'),
        'windspeed_kmh': current.get('windspeed'),
        'weather_code': current.get('weathercode'),
    })


@api_view(['GET'])
def get_user(request, user_id):
    """Fetch a random user seeded by user_id."""
    resp = requests.get(
        'https://randomuser.me/api/',
        params={'seed': str(user_id)},
        timeout=10,
    )
    resp.raise_for_status()
    results = resp.json().get('results', [])
    if not results:
        return Response({'error': 'User not found'}, status=404)

    user = results[0]
    return Response({
        'id': user_id,
        'name': f"{user['name']['first']} {user['name']['last']}",
        'email': user['email'],
        'city': user['location']['city'],
        'country': user['location']['country'],
    })


@api_view(['POST'])
def create_user(request):
    """Create a random user."""
    resp = requests.get('https://randomuser.me/api/', timeout=10)
    resp.raise_for_status()
    results = resp.json().get('results', [])
    if not results:
        return Response({'error': 'Failed to generate user'}, status=500)

    user = results[0]
    return Response({
        'name': f"{user['name']['first']} {user['name']['last']}",
        'email': user['email'],
        'city': user['location']['city'],
        'country': user['location']['country'],
    }, status=201)


@api_view(['GET'])
def get_post(request, post_id):
    """Fetch a post with its comments from jsonplaceholder."""
    post_resp = requests.get(
        f'https://jsonplaceholder.typicode.com/posts/{post_id}',
        timeout=10,
    )
    post_resp.raise_for_status()
    post = post_resp.json()

    comments_resp = requests.get(
        f'https://jsonplaceholder.typicode.com/posts/{post_id}/comments',
        timeout=10,
    )
    comments_resp.raise_for_status()
    comments = comments_resp.json()

    return Response({
        'id': post['id'],
        'title': post['title'],
        'body': post['body'],
        'num_comments': len(comments),
        'comments': [
            {'name': c['name'], 'email': c['email'], 'body': c['body']}
            for c in comments
        ],
    })


@api_view(['POST'])
def create_post(request):
    """Create a new post on jsonplaceholder."""
    resp = requests.post(
        'https://jsonplaceholder.typicode.com/posts',
        json={
            'title': request.data.get('title', 'Untitled'),
            'body': request.data.get('body', ''),
            'userId': request.data.get('user_id', 1),
        },
        timeout=10,
    )
    resp.raise_for_status()
    return Response(resp.json(), status=201)
