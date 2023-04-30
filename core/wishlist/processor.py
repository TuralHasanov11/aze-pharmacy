from django.db.models import Prefetch
from store.models import Product, ProductImage


class WishlistProcessor:
    wishlist: list[int]

    def __init__(self, request):
        self.session = request.session
        try:
            wishlistContainer: list[int] = self.session["wishlist"]
            products = Product.objects.select_related('category').prefetch_related(
                Prefetch('product_image', queryset=ProductImage.objects.filter(
                    is_feature=True), to_attr='image_feature'),
            ).filter(id__in=[key for key in wishlistContainer])
        except Exception:
            self.session["wishlist"] = []
            wishlistContainer = []

        self.wishlist = []
        self.products = []
        if wishlistContainer:
            for product in products:
                self.wishlist.append(product.id)
            self.products = products
            self.session["wishlist"] = self.wishlist
        self.save()

    def __iter__(self):
        for item in self.products:
            yield item

    def __len__(self):
        return len(self.wishlist)

    def add(self, productId: int):
        try:
            if productId not in self.wishlist:
                self.wishlist.append(productId)
                self.session["wishlist"] = self.wishlist
                self.save()
        except Exception:
            raise Exception("Product cannot be added to Wishlist")

    def remove(self, productId: int) -> None:
        try:
            if productId in self.wishlist:
                self.wishlist.remove(productId)
                self.session["wishlist"] = self.wishlist
                self.save()
        except Exception:
            raise Exception("Product is not removed from Wishlist")

    def clear(self) -> None:
        try:
            del self.wishlist
            self.session["wishlist"] = []
            self.save()
        except Exception:
            raise Exception("Wishlist cannot be cleared")

    def save(self) -> None:
        self.session.modified = True
