import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from multi_form_view import MultiFormView

from productapp.decorator import user_is_admin
from productapp.forms import ProductCreationForm, ProductThumbnailCreationForm, ProductCategoryCreationForm, \
    ProductDetailImageCreationForm
from productapp.models import Product, ProductThumbnailImage, ProductCategory, ProductDetailImage


CHECK_AUTHENTICATION = [login_required, user_is_admin]


#
# 상품 카테고리를 생성하는 view
#
@method_decorator(CHECK_AUTHENTICATION, 'get')
@method_decorator(CHECK_AUTHENTICATION, 'post')
class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    form_class = ProductCategoryCreationForm
    template_name = 'productapp/create/product_category_create.html'
    success_url = reverse_lazy('storeapp:index')

    def form_valid(self, form):
        return super(ProductCategoryCreateView, self).form_valid(form)


#
# 상품을 생성하는 view
#   - MultiFormView(django-multi-form-view 패키지)를 사용하여
#     여러 form을 한 페이지에 구현
#   - Product, ProductThumbnailImage, ProductDetailImage 3개의 object를 생성
#   - MultiFormView.forms_valid()를 이용해 여러 form의 Validation을 검사하고
#     Product의 category는 form을 이용하지 않고 받기 때문에 is_vaild()를 통해 따로 validation 검사
#
@method_decorator(CHECK_AUTHENTICATION, 'get')
@method_decorator(CHECK_AUTHENTICATION, 'post')
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

        if category_form.is_valid():  # category form 유효성 체크
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


#
# 상품 상세페이지 view
#
class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'target_product'
    template_name = 'productapp/detail.html'


#
# 상품을 삭제하는 view
#   - 해당 상품의 썸네일, 이미지를 삭제하기 위해 post()를 오버라이딩 함
#
@method_decorator(CHECK_AUTHENTICATION, 'get')
@method_decorator(CHECK_AUTHENTICATION, 'post')
class ProductDeleteView(DeleteView):
    model = Product
    context_object_name = 'target_product'
    template_name = 'productapp/delete.html'
    success_url = reverse_lazy('storeapp:index')

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        thumbnail_list = product.product_thumbnails.all()  # product_thumbnails는 ProductThumbnailImage 모델의 realeted_name
        detail_image_list = product.product_detail_images.all()  # product_detail_images는 ProductDetailImage 모델의 realeted_name

        for thumbnail in thumbnail_list:
            thumbnail.p_thumbnail.delete()

        for detail_image in detail_image_list:
            detail_image.p_detail_image.delete()

        return super(ProductDeleteView, self).post(request, *args, **kwargs)


#
# 상품의 정보를 수정하는 view
#
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductCreationForm
    template_name = 'productapp/update/update.html'
    context_object_name = 'target_product'

    def get_success_url(self):
        return reverse('productapp:detail', kwargs={'pk':self.object.pk})

#
# 상품의 이미지를 수정하기 전 기존 이미지를 보여주는 view
#
class ProductImageAll(DetailView):
    model = Product
    context_object_name = 'target_product'
    template_name = 'productapp/update/update_image_list.html'



#
# 상품의 이미지(Thumbnail, Detail)를 수정하는 view
#
# class ProductImageChangeView(MultiFormView):
#     form_classes = {'ProductThumbnailCreationForm': ProductThumbnailCreationForm,
#                     'ProductDetailImageCreationForm': ProductDetailImageCreationForm}
#
#     template_name = ''
#
#     def forms_valid(self, forms):
#         target_product_pk = self.request.POST.get('pk')
#         input_thumbnails = self.request.FILES.getlist('thumbnails', None)
#         input_detail_images = self.request.FILES.getlist('detail_images', None)
#
#
#     def get_success_url(self):
#         return reverse('productapp:detail', kwargs={'pk':self.request.POST.get('pk')})


def ProductImageChangeView(request, pk):
    if request.method == 'POST':
        target_case = request.POST.get('target_case', None)
        target_pk_list = request.POST.getlist('modal_input_hidden', None)
        new_image_list = request.POST.getlist('modal_input_file', None)
        target_object = None

        if target_case == 'thumbnail':
            target_object = ProductThumbnailImage.objects.filter(pk=pk)

        elif target_case == 'detail_image':
            target_object = ProductDetailImage.objects.filter(pk=pk)

        for target_pk in target_pk_list:
            print(target_object.get(pk=target_pk))
            print(target_object.filter(pk=target_pk))