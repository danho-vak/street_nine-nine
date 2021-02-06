from django.db.models import Q
from django.views.generic import ListView, DetailView

from productapp.models import Product


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
