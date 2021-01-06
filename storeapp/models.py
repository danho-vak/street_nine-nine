from django.db import models


class Product(models.Model):
    #category = models.ForeignKey('', on_delete='')
    product_title = models.CharField(max_length=100, null=False, blank=False)
    product_origin_price = models.IntegerField(null=False, blank=False)
    product_sale_price = models.IntegerField(null=False, blank=False)
    #product_image_thumbnail = models.
    #product_description = models.
    #product_description_image = models.
    #product_option_1 = models.

    
class ProductImages(models.Model):
    pass
