from django.db import models


class CourseDb(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "course_db"
