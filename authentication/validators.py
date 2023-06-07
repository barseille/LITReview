# ValidationError est une exception intégrée dans Django.
from django.core.exceptions import ValidationError


class ContainsLetterValidator:
    """
    Classe pour valider qu'un mot de passe contient au moins une lettre.
    Cette classe est utilisée dans la validation des mots de passe
    dans le cadre de l'inscription ou du changement de mot de passe.
    """
    def validate(self, password, user=None):
        """
        Cette méthode vérifie si le mot de passe contient au moins une lettre.
        Si ce n'est pas le cas, elle soulève une ValidationError.
        """
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir une lettre', code='password_no_letters')

    def get_help_text(self):
        """
        Cette méthode retourne un message d'aide qui peut être utilisé
        comme guide pour l'utilisateur lors de la création d'un mot de passe.
        """
        return 'Votre mot de passe doit contenir au moins une lettre majuscule ou minuscule.'
