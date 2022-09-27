from django.db import models


class CourseDb(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()

    class Meta:
        db_table = "course_db"
