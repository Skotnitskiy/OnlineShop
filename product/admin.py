from django.contrib import admin

from product.models import (Category,
                            Subcategory,
                            Product,
                            ExchangeRate,
                            Producer)

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(ExchangeRate)
admin.site.register(Producer)
