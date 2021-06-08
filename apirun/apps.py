from django.apps import AppConfig
from . views import fetchVideo
import sys

class ApirunConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apirun'
    
    # Runs The Thread To Get You Tube Search Query Data
    def ready(self):
        RUNNING_DEVSERVER = (len(sys.argv) > 1 and sys.argv[1] == 'runserver')
        print(RUNNING_DEVSERVER)
        if(RUNNING_DEVSERVER):
            fetchVideo()