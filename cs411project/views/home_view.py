from flask.views import View

class HomeView(View):

    def dispatch_request(self):
        return "Flask is up! Now to get templates figured out"
