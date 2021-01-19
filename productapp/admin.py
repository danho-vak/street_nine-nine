from django.contrib import admin

# Register your models here.
from productapp.models import Product, ProductThumbnailImage, ProductOption, \
    ProductDetailImage, ProductCategory

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductThumbnailImage)
admin.site.register(ProductDetailImage)
admin.site.register(ProductOption)
