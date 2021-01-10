from django.db import models

from imagekit.models import ProcessedImageField
from pilkit.processors import Thumbnail


class Product(models.Model):
    product_category = models.ForeignKey('ProductCategory',
                                         related_name='product_category',    # 제품의 카테고리
                                         on_delete=models.SET_NULL,
                                         null=True,
                                         verbose_name='product_category')
    product_id = models.CharField(max_length=10, null=False, blank=False)                       # 판매자가 부여한 제품의 ID
    product_code = models.CharField(max_length=10, null=False, blank=False, unique=True)        # 제품의 옵션에 따른 판매자가 부여한 제품의 고유 CODE
    product_sale_id = models.CharField(max_length=10, null=False, blank=False, unique=True)     # 제품의 ID + CODE로 조합된 판매코드(파생 컬럼으로 사용 예정)
    product_title = models.CharField(max_length=100, null=False, blank=False)                   # 제품 명
    product_origin_price = models.IntegerField(null=False, blank=False)                         # 제품 원가
    product_sale_price = models.IntegerField(null=False, blank=False)                           # 제품 실제 판매 가격(파생 컬럼으로 사용 예정)
    product_description = models.CharField(max_length=200, null=False, blank=False)             # 제품 설명
    product_is_display = models.BooleanField(default=True)                                      # 제품 전시 여부

    def __str__(self):
        return self.product_title


'''
    제품의 썸네일을 저장할 model
        Product와 1:N관계로 설정()
'''
class ProductThumbnailImage(models.Model):
    p_target_product_id = models.ForeignKey(Product,
                                            on_delete=models.CASCADE,
                                            related_name='product_thumbnails',
                                            verbose_name='p_target_product_id')
    p_thumbnail = ProcessedImageField(upload_to='product_thumbnails',
                                      processors=[Thumbnail(300, 300)],
                                      format='JPEG',
                                      options={'quality': 60}, null=True, blank=True)

    def __str__(self):
        return str(self.p_target_product_id)

'''
    제품의 상세이미지를 저장할 model
        product와 1:N관계로 설정
'''
class ProductDetailImage(models.Model):
    p_target_product_id = models.ForeignKey(Product,
                                            on_delete=models.CASCADE,
                                            related_name='product_detail_images',
                                            verbose_name='p_target_product_id')
    p_detail_image = models.ImageField(upload_to='ProductDetailImages', blank=False, null=False)


'''
    제품의 상위 옵션을 저장할 model
        product와 1:N관계로 설정
'''
class ProductOptionParent(models.Model):
    p_target_product_id = models.ForeignKey(Product,
                                            on_delete=models.CASCADE,
                                            related_name='product_options',
                                            verbose_name='p_target_product_id')

'''
    제품의 하위 옵션을 저장할 model
        ProductOptionParent와 1:N관계로 설정
'''
class ProductOptionChild(models.Model):
    p_option_parent_id = models.ForeignKey('ProductOptionParent',
                                           on_delete=models.CASCADE,
                                           related_name='product_child',
                                           verbose_name='p_option_parent_id', null=True, blank=True)
    p_option_child_title = models.CharField(max_length=20, null=False, blank=False)


'''
    제품의 카테고리를 저장할 model
        Product와 N:1(ProductCategory) 관계로 설정
'''
class ProductCategory(models.Model):
    category_parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)  # 계층적 구조
    category_name = models.CharField(max_length=20)

    def __str__(self):
        return '{} > {}'.format(self.category_parent, self.category_name)