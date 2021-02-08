from django.db import models

from accountapp.models import User
from productapp.models import Product


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, name='review_user')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, name='review_product')
    content = models.CharField(max_length=300, null=False, blank=False)
    product_rate = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_detail_image')
    review_detail_image = models.ImageField(upload_to='ProductReviews', null=True, blank=True)

