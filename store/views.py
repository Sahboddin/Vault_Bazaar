from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating
from category.models import Category
from django.core.paginator import Paginator
from .forms import ReviewForm
from cart.models import CartItem


def store(request, category_slug=None):
    """
    Store view:
    Displays a paginated list of available products. If a category_slug is provided,
    filters products by that category; otherwise shows all available products.

    Context:
    - products: Page object of Product instances for the current page.
    - categories: All Category instances for navigation.
    """
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(is_available=True, category=category)
        paginator = Paginator(products, 1)  # Number of products per page when filtered
    else:
        products = Product.objects.filter(is_available=True)
        paginator = Paginator(products, 3)  # Number of products per page when unfiltered

    page = request.GET.get('page')
    paged_product = paginator.get_page(page)
    categories = Category.objects.all()

    context = {
        'products': paged_product,
        'categories': categories,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    """
    Product detail view:
    Retrieves a single product based on its slug and category, and fetches approved reviews.

    Parameters:
    - category_slug: Slug of the category to which the product belongs.
    - product_slug: Slug of the product to display.

    Context:
    - product: Product instance matching the slugs.
    - reviews: QuerySet of approved ReviewRating instances for the product.
    """
    single_product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug)
    reviews = ReviewRating.objects.filter(product=single_product, status=True)
    return render(
        request,
        'store/product-detail.html',
        {'product': single_product, 'reviews': reviews}
    )


def submit_review(request, product_id):
    """
    Submit or update a product review:
    - If a review by the current user exists for the product, updates it.
    - Otherwise, creates a new ReviewRating instance.

    After saving, redirects back to the referring page.

    Parameters:
    - product_id: ID of the Product being reviewed.
    """
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            # Check if user has already reviewed this product
            product = get_object_or_404(Product, id=product_id)
            existing_review = ReviewRating.objects.get(user=request.user, product=product)
            form = ReviewForm(request.POST, instance=existing_review)
            if form.is_valid():
                form.save()
            return redirect(url)
        except ReviewRating.DoesNotExist:
            # Create a new review
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating(
                    subject=form.cleaned_data['subject'],
                    rating=form.cleaned_data['rating'],
                    review=form.cleaned_data['review'],
                    product_id=product_id,
                    user=request.user
                )
                data.save()
                return redirect(url)
    return redirect(url)
