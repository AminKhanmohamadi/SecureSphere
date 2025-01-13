from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import ListView
from django.db.models import Case, When, DecimalField
from products.models import Product, Category


# Create your views here.
class ProductListView(ListView):
    model=Product
    context_object_name='products'
    paginate_by=20
    template_name='products/product_list.html'

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        sort_by = self.request.GET.get('sort_by', 'newest')
        products = Product.objects.filter(category_id=pk).order_by('-created_at')

        products = products.annotate(
            final_price=Case(
                When(off_price__isnull=False, then='off_price'),
                default='price',
                output_field=DecimalField()
            )
        )

        if sort_by == 'price_asc':
            products = products.order_by('final_price')
        elif sort_by == 'price_desc':
            products = products.order_by('-final_price')
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(parent__isnull=False)
        return context
    def render_to_response(self, context, **response_kwargs):
        # بررسی درخواست AJAX
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('products/partials/product_list_partial.html', context)
            return JsonResponse({'html': html})
        # در صورت نبود درخواست AJAX، صفحه کامل رندر شود
        return super().render_to_response(context, **response_kwargs)