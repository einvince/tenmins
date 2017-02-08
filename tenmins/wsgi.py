

import os, sys


root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, '..', 'site-packages'))


# add the django project path into the sys.path
# sys.path.append('/root/tenmins/')
# add the virtualenv site-packages path to the sys.path
# sys.path.append('<PATH_TO_VIRTUALENV>/Lib/site-packages')

# poiting to the project settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tenmins.settings")


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()





