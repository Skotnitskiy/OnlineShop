from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Subcategory(models.Model):
    category = models.ManyToManyField(Category,
                                      related_name='subcategories')
    title = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Subcategories'

    def __str__(self):
        return self.title


class Product(models.Model):
    subcategory = models.ManyToManyField(Subcategory)

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField(default=0.0)
    on_the_main = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Order(models.Model):
    product_id = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=1)

    @property
    def cost(self):
        return self.price * int(self.quantity)

    def __str__(self):
        return self.title

    def __radd__(self, other):
        return other + self.cost
