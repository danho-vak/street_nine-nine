from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from productapp.models import Product
from reviewapp.forms import ReviewCreationForm
from reviewapp.models import Review, ReviewImage


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewCreationForm
    template_name = 'reviewapp/create.html'

    def form_valid(self, form):
        product = Product.objects.get(pk=self.request.POST.get('product_pk'))
        new_review = form.save(commit=False)
        new_review.review_user = self.request.user
        new_review.review_product = product
        new_review.save()

        new_review_image = self.request.FILES.getlist('review_image', None)
        if new_review_image:
            for image in new_review_image:
                review_image = ReviewImage(review=new_review, review_detail_image=image)
                review_image.save()
        return super().form_valid(form)

    def get_success_url(self):
        print(self.object)
        return reverse('productapp:detail', kwargs={'pk': self.object.review_product.pk})
