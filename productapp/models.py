from django.db import models

from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill


class Product(models.Model):
    #category = models.ForeignKey('', on_delete='')
    product_id = models.CharField(max_length=10, null=False, blank=False)                       # 판매자가 부여한 제품의 ID
    product_code = models.CharField(max_length=10, null=False, blank=False, unique=True)        # 제품의 옵션에 따른 판매자가 부여한 제품의 고유 CODE
    product_sale_id = models.CharField(max_length=10, null=False, blank=False, unique=True)     # 제품의 ID + CODE로 조합된 판매코드(파생 컬럼으로 사용 예정)
    product_title = models.CharField(max_length=100, null=False, blank=False)                   # 제품 명
    product_origin_price = models.IntegerField(null=False, blank=False)                         # 제품 원가
    product_sale_price = models.IntegerField(null=False, blank=False)                           # 제품 실제 판매 가격(파생 컬럼으로 사용 예정)
    product_description = models.CharField(max_length=200, null=False, blank=False)             # 제품 설명
    product_is_display = models.BooleanField(default=True)                                      # 제품 전시 여부

    # product_thumbnails = models.ForeignKey('ProductThumbnailImages', on_delete=models.CASCADE)  # 제품 썸네일
    # product_detail_images = models.ForeignKey('ProductDetailImages', on_delete=models.CASCADE)  # 제품 상세 이미지

    def __str__(self):
        return self.product_title


'''
    제품의 썸네일을 저장할 model
        Product와 1:N관계로 설정()
'''
class ProductThumbnailImages(models.Model):
    p_target_product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_thumbnails')
    p_thumbnail = ProcessedImageField(upload_to='product_thumbnails',
                                      processors=[ResizeToFill(300, 300)],
                                      format='JPEG',
                                      options={'quality': 60})


'''
    제품의 상세이미지를 저장할 model
        product와 1:N관계로 설정
'''
class ProductDetailImages(models.Model):
    p_target_product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_detail_images')
    p_detail_image = models.ImageField(upload_to='ProductDetailImages', blank=False, null=False)


'''
    제품의 상위 옵션을 저장할 model
    product와 1:N관계로 설정
'''
class ProductOptionParent(models.Model):
    p_target_product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_options')
    p_option_parent_title = models.CharField(max_length=20, null=False, blank=False)


'''
    제품의 하위 옵션을 저장할 model
        ProductOptionParent와 1:N관계로 설정
'''
class ProductOptionChild(models.Model):
    p_option_parent = models.ForeignKey('ProductOptionParent', on_delete=models.CASCADE, related_name='product_child')
    p_option_child_title = models.CharField(max_length=20, null=False, blank=False)