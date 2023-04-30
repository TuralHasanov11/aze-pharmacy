from wishlist.processor import WishlistProcessor


def wishlist(request):
    return {"wishlist": WishlistProcessor(request)}