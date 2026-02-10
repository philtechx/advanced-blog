<<<<<<< HEAD
from .models import Category

def categories_processor(request):
    """
    Returns all categories to templates (e.g., sidebar).
    """
    return {'categories': Category.objects.all()}
=======
from .models import Category

def categories_processor(request):
    """
    Returns all categories to templates (e.g., sidebar).
    """
    return {'categories': Category.objects.all()}
>>>>>>> 4a481a0 (Updated blog added comment system and authentication)
