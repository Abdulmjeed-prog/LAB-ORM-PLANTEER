from django.db import models

# Create your models here.

class Plant(models.Model):
    class CategoryChoices(models.TextChoices):
        cat_1 = 'herb', 'Herb'
        cat_2 = 'flowering', 'Flowering'
        cat_3 = 'succulent', 'Succulent'
        cat_4 = 'houseplant', 'Houseplant'
        cat_5 = 'medicinal', 'Medicinal'
        cat_6 = 'vegetable', 'Vegetable'
        cat_7 = 'fruit', 'Fruit'
        cat_8 = 'tree', 'Tree'
        cat_9 = 'indoor', 'Indoor'


    name = models.CharField(1024)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField()
    category = models.CharField(1024,choices=CategoryChoices.choices)
    is_edible = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)