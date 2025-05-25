from django import template

register = template.Library()

@register.filter
def stars(rating):
    """Returns a string of filled and empty stars."""
    rating = int(round(rating))
    total_stars = ""
    for i in range(1,6):
        if i <= rating:
            total_stars += '★'
        else:
            total_stars += '☆'
    return total_stars
