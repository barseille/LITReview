from django import template

# Création d'une instance de la classe Library, qui peut stocker un ensemble de tags et de filtres personnalisés.
register = template.Library()

# Définition d'un filtre qui peut être utilisé dans les templates pour accéder à une valeur d'un dictionnaire par sa clé.
@register.filter
def get_item(dictionary, key):
    """
    Récupère une valeur d'un dictionnaire en utilisant sa clé.
    """
    return dictionary.get(key)

# Définition d'un filtre qui peut être utilisé dans les templates pour récupérer le nom de la classe d'un objet.
@register.filter
def classname(obj):
    """
    Récupère le nom de la classe de l'objet.
    """
    return obj.__class__.__name__
