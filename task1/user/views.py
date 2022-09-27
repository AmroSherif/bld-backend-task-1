from copy import deepcopy
from django.http import JsonResponse, HttpResponse
from django.views import View
import json
from .forms import UserForms
from user.models import UserDb
from datetime import date


class User(View):
    def get(self, request, *args, **kwargs):
        user_qr = UserDb.objects
        age = request.GET.get("age")
        if age != None:
            user_qr = user_qr.filter(
                birth_date__lte=date(
                    date.today().year - int(age), date.today().month, date.today().day
                )
            )
        # ok
        users = {"users_list": list(user_qr.values())}
        return JsonResponse(data=users, status=200)

    def post(self, request, *args, **kwargs):
        r_body = json.loads(request.body)
        f = UserForms(
            {
                "first_name": r_body["first_name"],
                "last_name": r_body["last_name"],
                "birth_date": r_body["birth_date"],
                "email": r_body["email"],
                "password": r_body["password"],
            }
        )
        if f.is_valid():
            UserDb.objects.create(
                first_name=r_body["first_name"],
                last_name=r_body["last_name"],
                birth_date=r_body["birth_date"],
                email=r_body["email"],
                password=r_body["password"],
            )
            # created
            return HttpResponse(status=201)
        else:
            # unprocessable Entity
            return JsonResponse(data=json.loads(f.errors.as_json()), status=422)


class SingleUser(View):
    def get(self, request, *args, **kwargs):
        user_qr = UserDb.objects.filter(pk=kwargs["id"])
        if len(user_qr):
            # found
            return JsonResponse(data=user_qr.values()[0], status=302)
        # not found
        return HttpResponse(status=404)

    def update_user(self, user_qr, first_name, last_name, birth_date, email, password):
        user_qr.first_name = first_name
        user_qr.last_name = last_name
        user_qr.birth_date = birth_date
        user_qr.email = email
        user_qr.password = password
        user_qr.save()

    def put(self, request, *args, **kwargs):
        r_body = json.loads(request.body)
        user_qr = UserDb.objects.filter(pk=kwargs["id"])
        if len(user_qr):
            # ok
            status_code = 200
            f = UserForms(
                {
                    "first_name": r_body["first_name"],
                    "last_name": r_body["last_name"],
                    "birth_date": r_body["birth_date"],
                    "email": r_body["email"],
                    "password": r_body["password"],
                }
            )
            if f.is_valid():
                self.update_user(
                    user_qr[0],
                    r_body["first_name"],
                    r_body["last_name"],
                    r_body["birth_date"],
                    r_body["email"],
                    r_body["password"],
                )
            else:
                # unprocessable Entity
                return JsonResponse(data=json.loads(f.errors.as_json()), status=422)
        else:
            # not found
            status_code = 404
        return HttpResponse(status=status_code)

    def delete(self, request, *args, **kwargs):
        status_code = 404
        user_qr = UserDb.objects.filter(pk=kwargs["id"])
        if len(user_qr):
            user_qr[0].delete()
            # found
            status_code = 200
        # not found
        return HttpResponse(status=status_code)
