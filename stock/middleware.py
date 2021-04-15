try:
    import jwt
    import json
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
    from django.contrib.auth.hashers import check_password
    from django.shortcuts import HttpResponseRedirect
    from django.http import HttpResponse
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x


class SimpleMiddleware(MiddlewareMixin):
    def checkToken(self,token):
        salt = "asgfdgerher"
        try:
            info = jwt.decode(token, salt, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            print('token out date')
            print(info)
            return False
        except jwt.InvalidTokenError:
            print('token error')
            return False
        return True

    def process_request(self, request):
        print(request.META)
        if request.META.get("PATH_INFO") == "/login":
            pass
        else:
            token = request.META.get("HTTP_AUTHORIZATION")
            # tokencheck = check_password(ip + c_time + users_names + "laodiggn", token)
            print(token)
            if token is not None:
                if self.checkToken(token):
                    print("success")
                    pass
                else:
                    dic = {'state': 300, 'message': "Please login"}
                    return HttpResponse(json.dumps(dic, ensure_ascii=False))
            else:
                print("fail")
                dic = {'state': 300, 'message': "Please login"}
                return HttpResponse(json.dumps(dic, ensure_ascii=False))

    def process_response(self, request, response):
        return response
