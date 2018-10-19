from flask.views import MethodView

# A simple test View to make sure the pipes fit with cPanel
class TestAPIView(MethodView):

    def get(self, user_id):
        return "Nice to meet you, User {0}".format(user_id)
