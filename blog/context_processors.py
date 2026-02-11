from .models import Category

def categories_processor(request):
    """
    Returns all categories to templates (e.g., sidebar).
    """
    return {'categories': Category.objects.all()}
