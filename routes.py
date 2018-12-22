PAGES_FOLDER = 'pages'


def not_found():
    return read_content('not_found.html')


def index():
    return read_content('index.html')


def about():
    return read_content('about.html')


def read_content(filename):
    f = open(PAGES_FOLDER + '/' + filename)
    content = f.read()
    f.close()
    return content


handlers = {
    '/not_found': not_found,
    '/': index,
    '/about': about
}
