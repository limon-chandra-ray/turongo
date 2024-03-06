from django.contrib import admin
from .models import Product,ProductImage,ProductSize,RootCategory,RootCategoryTwo,RootCategoryThree,Category
# Register your models here.
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductSize)

admin.site.register(RootCategory)
admin.site.register(RootCategoryTwo)
admin.site.register(RootCategoryThree)
admin.site.register(Category)