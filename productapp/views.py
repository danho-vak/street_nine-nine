import json

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from multi_form_view import MultiFormView

from productapp.forms import ProductCreationForm, ProductThumbnailCreationForm, ProductCategoryCreationForm, \
    ProductDetailImageCreationForm
from productapp.models import Product, ProductThumbnailImage, ProductCategory, ProductDetailImage


'''
    상품 카테고리를 생성하는 view
'''
class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    form_class = ProductCategoryCreationForm
    template_name = 'productapp/create/product_category_create.html'
    success_url = reverse_lazy('storeapp:index')

    def form_valid(self, form):
        return super(ProductCategoryCreateView, self).form_valid(form)


'''
    상품을 생성하는 view
     - MultiFormView(django-multi-form-view 패키지)를 사용하여
       여러 form을 한 페이지에 구현
'''
class ProductCreateView(MultiFormView):
    form_classes = {'ProductCreationForm': ProductCreationForm,
                    'ProductThumbnailCreationForm': ProductThumbnailCreationForm,
                    'ProductDetailImageCreationForm': ProductDetailImageCreationForm}

    template_name = 'productapp/create/product_create.html'
    success_url = reverse_lazy('storeapp:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = json.dumps(list(ProductCategory.objects.select_related().all().values()),
                                              ensure_ascii=False)
        return context

    def forms_valid(self, forms):
        product = forms['ProductCreationForm'].save(commit=False)
        thumb_list = self.request.FILES.getlist('p_thumbnail', None)
        detail_list = self.request.FILES.getlist('p_detail_image', None)

        category_form = ProductCategoryCreationForm({'category_parent': self.request.POST.get('category_parent'),
                                                     'category_name': self.request.POST.get('category_name')})
        if category_form.is_valid():
            category = category_form.save()

            product.product_category = category
            product.save()

        if thumb_list:  # 썸네일 저장
            for thumb_image in thumb_list:
                new_thumb = ProductThumbnailImage()
                new_thumb.p_target_product_id = product
                new_thumb.p_thumbnail = thumb_image
                new_thumb.save()

        if detail_list:  # 제품 상세 이미지 저장
            for detail_image in detail_list:
                new_detail_image = ProductDetailImage()
                new_detail_image.p_target_product_id = product
                new_detail_image.p_detail_image = detail_image
                new_detail_image.save()

        return super(ProductCreateView, self).forms_valid(forms)


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'target_product'
    template_name = 'productapp/detail.html'