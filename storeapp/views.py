from django.db.models import Q
from django.views.generic import ListView, DetailView

from productapp.models import Product, ProductCategory


#  메인 화면 List View
class StoreMainList(ListView):
    context_object_name = 'product_list'
    template_name = 'storeapp/main/index.html'

    def get_queryset(self):
        return Product.objects.all().select_related()


#  검색 결과를 처리할 List View
class StoreSearchResultView(ListView):
    context_object_name = 'product_list'
    template_name = 'storeapp/search/search.html'

    def get_queryset(self):
        keyword = self.request.GET.get('q', None)

        if keyword:
            search_result = Product.objects.filter(Q(product_title__icontains=keyword) | Q(product_description__icontains=keyword))
            return search_result


#  카테고리별 상품 List View
class StoreCategoryResultView(ListView):
    model = Product
    template_name = 'storeapp/search/search.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        target_category = self.kwargs['category_code']

        if (target_category == 100) or (target_category == 200) or (target_category == 300) or (target_category == 400):
            print(Product.objects.all().select_related('product_category').filter(category_code__startswith=str(target_category)[:1]))
            context['product_list'] = ProductCategory.objects.filter(category_code__startswith=str(target_category)[:1])
        else:
            print(ProductCategory.objects.filter(category_code=target_category))
            context['product_list'] = ProductCategory.objects.filter(category_code=target_category)

        return context