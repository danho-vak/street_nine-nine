from django.contrib import admin

# Register your models here.
from productapp.models import Product, ProductThumbnailImages, ProductOptionParent, ProductOptionChild, \
                                ProductDetailImages

admin.site.register(Product)
admin.site.register(ProductThumbnailImages)
admin.site.register(ProductDetailImages)
admin.site.register(ProductOptionParent)
admin.site.register(ProductOptionChild)
