import webbrowser

url = 'http://www.python.org/'
url = 'https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=37.5072,-122.2605'

# Open URL in a new tab, if a browser window is already open.
webbrowser.open_new_tab(url + 'doc/')

# Open URL in new window, raising the window if possible.
webbrowser.open_new(url)