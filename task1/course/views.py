from django.http import JsonResponse, HttpResponse
from django.views import View
import json
from .forms import CourseForms
from course.models import CourseDb


class Course(View):
    def get(self, request, *args, **kwargs):
        # ok
        courses = {"courses_list": list(CourseDb.objects.values())}
        return JsonResponse(data=courses, status=200)

    def post(self, request, *args, **kwargs):
        r_body = json.loads(request.body)
        f = CourseForms({"name": r_body["name"], "description": r_body["description"]})
        if f.is_valid():
            CourseDb.objects.create(
                name=r_body["name"], description=r_body["description"]
            )
            # created
            return HttpResponse(status=201)
        else:
            # unprocessable Entity
            return JsonResponse(data=json.loads(f.errors.as_json()), status=422)


class SingleCourse(View):
    def get(self, request, *args, **kwargs):
        course_qr = CourseDb.objects.filter(pk=kwargs["id"])
        if len(course_qr):
            # found
            return JsonResponse(data=course_qr.values()[0], status=302)
        # not found
        return HttpResponse(status=404)

    def update_course(self, course_qr, name, description):
        course_qr.name = name
        course_qr.description = description
        course_qr.save()

    def put(self, request, *args, **kwargs):
        r_body = json.loads(request.body)
        course_qr = CourseDb.objects.filter(pk=kwargs["id"])
        if len(course_qr):
            # ok
            status_code = 200
            f = CourseForms(
                {"name": r_body["name"], "description": r_body["description"]}
            )
            if f.is_valid():
                self.update_course(course_qr[0], r_body["name"], r_body["description"])
            else:
                # unprocessable Entity
                return JsonResponse(data=json.loads(f.errors.as_json()), status=422)
        else:
            # not found
            status_code = 404
        return HttpResponse(status=status_code)

    def delete(self, request, *args, **kwargs):
        status_code = 404
        course_qr = CourseDb.objects.filter(pk=kwargs["id"])
        if len(course_qr):
            course_qr[0].delete()
            # found
            status_code = 200
        # not found
        return HttpResponse(status=status_code)
