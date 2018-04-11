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
    meta_kw = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Subcategories'

    def __str__(self):
        return self.title


class Producer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    subcategory = models.ManyToManyField(Subcategory)
    producer = models.ForeignKey(Producer, null=True, on_delete=models.SET_NULL)

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField(default=0.0)
    on_the_main = models.BooleanField(default=False)
    img_url = models.URLField()
    rating = models.IntegerField(default=0)
    meta_kw = models.CharField(max_length=200)

    class Meta:
        ordering = ['-rating']

    def __str__(self):
        return self.title


class OrderDetails(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)


class Order(models.Model):
    order_details = models.ForeignKey(OrderDetails, default=None)

    product_id = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=1)
    img_url = models.URLField()

    @property
    def cost(self):
        return self.price * int(self.quantity)

    def __str__(self):
        return self.title

    def __radd__(self, other):
        return other + self.cost


class ExchangeRate(models.Model):
    currency = models.FloatField()
    currency_name = models.CharField(max_length=5)

    def __str__(self):
        return self.currency_name

