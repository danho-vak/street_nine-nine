from django.contrib import admin

# Register your models here.
from productapp.models import Product, ProductThumbnailImage, ProductOptionParent, ProductOptionChild, \
                                ProductDetailImage

admin.site.register(Product)
admin.site.register(ProductThumbnailImage)
admin.site.register(ProductDetailImage)
admin.site.register(ProductOptionParent)
admin.site.register(ProductOptionChild)
