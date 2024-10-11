from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.title} by {self.author}"



class Author(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    age= models.IntegerField(100)

    def __str__(self):
        return (f"name - {self.first_name},\n"
                f"last name - {self.last_name}\n"
                f"age - {self.age}")

