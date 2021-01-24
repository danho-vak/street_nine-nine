from django.forms import ModelForm, Select
from productapp.models import Product, ProductThumbnailImage, ProductCategory, ProductDetailImage, ProductOption


class ProductCategoryCreationForm(ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductCreationForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['product_category']

    def __init__(self, *args, **kwargs):
        super(ProductCreationForm, self).__init__(*args, **kwargs)
        self.fields['product_sale_id'].widget.attrs.update({'disabled': 'disabled'})

'''
    상품의 썸네일을 저장할 form
        - __init__()에서 input file의 속성값을 multiple로 업데이트함
        - p_target_product_id는 제외(제품 등록시 Product.pk는 미등록 상태이기 때문에 ProductCreateView의 forms_vaild에서 설정) 
'''
class ProductThumbnailCreationForm(ModelForm):
    class Meta:
        model = ProductThumbnailImage
        fields = ['p_thumbnail']
        exclude = ['p_target_product_id']

    def __init__(self, *args, **kwargs):
        super(ProductThumbnailCreationForm, self).__init__(*args, **kwargs)
        self.fields['p_thumbnail'].widget.attrs.update({'multiple': 'multiple'})


'''
    상품의 상세 이미지를 저장할 form
        - 위의 ProductThumbnailCreationForm과 같은 로직
'''
class ProductDetailImageCreationForm(ModelForm):
    class Meta:
        model = ProductDetailImage
        fields = ['p_detail_image']
        exclude = ['p_target_product_id']

    def __init__(self, *args, **kwargs):
        super(ProductDetailImageCreationForm, self).__init__(*args, **kwargs)
        self.fields['p_detail_image'].widget.attrs.update({'multiple': 'multiple'})

#
#   상품의 옵션을 담을 form
#
class ProductOptionCreationForm(ModelForm):
    class Meta:
        model = ProductOption
        fields = ['p_product_option_class_1', 'p_product_option_class_2']
        exclude = ['p_target_product_id']