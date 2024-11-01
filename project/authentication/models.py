from django.db import models

# Create a model to store the form data
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp

    def __str__(self):
        return self.name  # Return the name when referencing the object
