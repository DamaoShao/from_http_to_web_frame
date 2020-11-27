from models import User

import uuid

# set_cookies example
session = {}


def template(name):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def current_user(request):
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, 'visitor')
    return username


def response_with_headers(headers, code=200):
    header = 'HTTP/1.1 {} VERY OK\r\n'.format(code)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                       for k, v in headers.items()])
    return header


def redirect(url):
    headers = {
        'Location': url,
    }
    # no body
    r = response_with_headers(headers, 302) + '\r\n'
    return r.encode('utf-8')


def login_required(route_function):
    def decorator(request):
        username = current_user(request)
        u = User.find_by(username=username)
        if u is None:
            return redirect('/login')
        return route_function(request)
    return decorator


def route_static(request):
    filename = request.query.get('file', 'image.jpeg')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img


def route_index(request):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(headers)
    body = template('index.html')
    username = current_user(request)
    body = body.replace('{{username}}', username)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_login(request):
    headers = {
        'Content-Type': 'text/html',
    }
    username = current_user(request)
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            session_id = str(uuid.uuid4())
            session[session_id] = u.username
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            result = 'Login successfully'
        else:
            result = 'Incorrect username or password'
    else:
        result = ''
    body = template('login.html')
    body = body.replace('{{result}}', result)
    body = body.replace('{{username}}', username)
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_register(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        u.save()
        result = 'registered successfully<br><br><br> <h3>{}</h3>'.format(u)
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
}
