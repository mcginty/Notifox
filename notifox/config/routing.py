"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.explicit = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # Page section
    map.connect('/', controller='index', action='index')
    map.connect('/add', controller='page', action='add')
    map.connect('/selected', controller='page', action='selected')
    map.connect('/selected/', controller='page', action='selected')

    # Auth section
    map.connect('/register', controller='auth', action='register_post', conditions=dict(method=['POST']))
    map.connect('/register', controller='auth', action='register')
    map.connect('/register/', controller='auth', action='register')

    map.connect('/login', controller='auth', action='login_post', conditions=dict(method=['POST']))
    map.connect('/login', controller='auth', action='login')
    map.connect('/login/', controller='auth', action='login')
    map.connect('/logout', controller='auth', action='logout')

    #map.connect('/{controller}', action='index')
    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')

    return map
