from fileinput import close
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View
import shortuuid
import json


def read_db():
    j_file = open("db.json")
    j_data = json.load(j_file)
    j_file.close()
    return j_data


def write_db(j_data):
    j_file = open("db.json", "w")
    j_file.write(json.dumps(j_data))
    j_file.close()


class Course(View):
    def get(self, request, *args, **kwargs):
        j_data = read_db()
        # ok
        return JsonResponse(data=j_data, status=200)

    def create_course(self, course_name, course_description):
        new_course = {
            "id": shortuuid.uuid(),
            "name": course_name,
            "description": course_description,
        }
        return new_course

    def post(self, request, *args, **kwargs):
        j_data = read_db()
        r_body = json.loads(request.body)
        new_course = self.create_course(r_body["name"], r_body["description"])

        j_data["courses"].append(new_course)

        write_db(j_data)
        # created
        return HttpResponse(status=201)


class SingleCourse(View):
    def find_course(self, course_id, j_data):
        for i in range(len(j_data["courses"])):
            if j_data["courses"][i]["id"] == course_id:
                return i
        return -1

    def get(self, request, *args, **kwargs):
        j_data = read_db()
        course_index = self.find_course(kwargs["id"], j_data)
        single_course = j_data["courses"][course_index] if course_index != -1 else {}
        # found / not found
        status_code = 302 if course_index != -1 else 404
        return JsonResponse(data=single_course, status=status_code)

    def update_course(self, course_index, course_name, course_description, j_data):
        j_data["courses"][course_index]["name"] = course_name
        j_data["courses"][course_index]["description"] = course_description

    def put(self, request, *args, **kwargs):
        j_data = read_db()
        r_body = json.loads(request.body)
        course_index = self.find_course(kwargs["id"], j_data)
        if course_index != -1:
            self.update_course(
                course_index, r_body["name"], r_body["description"], j_data
            )
        # ok / not found
        status_code = 200 if course_index != -1 else 404
        write_db(j_data)
        return HttpResponse(status=status_code)

    def delete(self, request, *args, **kwargs):
        j_data = read_db()
        course_index = self.find_course(kwargs["id"], j_data)
        if course_index != -1:
            j_data["courses"].pop(course_index)
        # ok / not found
        status_code = 200 if course_index != -1 else 404
        write_db(j_data)
        return HttpResponse(status=status_code)
