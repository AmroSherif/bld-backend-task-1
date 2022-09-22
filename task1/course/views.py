from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import shortuuid
import json


class Course(View):
    def get(self, request, *args, **kwargs):
        json_data = open("db.json")
        j_data = json.load(json_data)

        if "id" in kwargs.keys():
            for i in j_data["courses"]:
                if i["id"] == kwargs["id"]:
                    return JsonResponse(data=i)
            return JsonResponse(data={})
        else:
            return JsonResponse(data=j_data)

    def post(self, request, *args, **kwargs):
        json_data = open("db.json")

        j_data = json.load(json_data)
        json_data.close()

        r_body = json.loads(request.body)

        new_course = {
            "id": shortuuid.uuid(),
            "name": r_body["name"],
            "description": r_body["description"],
        }

        j_data["courses"].append(new_course)

        json_data = open("db.json", "w")
        json_data.write(json.dumps(j_data))

        return JsonResponse(data=j_data)

    def put(self, request, *args, **kwargs):
        json_data = open("db.json")

        j_data = json.load(json_data)
        json_data.close()

        r_body = json.loads(request.body)

        for i in j_data["courses"]:
            if i["id"] == kwargs["id"]:
                i["name"] = r_body["name"]
                i["description"] = r_body["description"]
                selected_course = i
                break

        json_data = open("db.json", "w")
        json_data.write(json.dumps(j_data))

        return JsonResponse(data=selected_course)

    def delete(self, request, *args, **kwargs):
        json_data = open("db.json")

        j_data = json.load(json_data)
        json_data.close()

        for i in j_data["courses"]:
            if i["id"] == kwargs["id"]:
                j_data["courses"].pop(j_data["courses"].index(i))
                break

        json_data = open("db.json", "w")
        json_data.write(json.dumps(j_data))

        return JsonResponse(data={})
