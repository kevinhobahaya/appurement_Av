from django import forms
from .models import Importateur, AV, AVProduit, Declaration


# =========================
# IMPORTATEUR FORM
# =========================
class ImportateurForm(forms.ModelForm):

    class Meta:
        model = Importateur

        fields = [
            "nom",
            "adresse",
            "num_telephone",
            "email"
        ]

        widgets = {

            "nom": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nom importateur"
            }),

            "adresse": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Adresse"
            }),

            "num_telephone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Téléphone"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email"
            }),

        }


# =========================
# AV FORM
# =========================
class AVForm(forms.ModelForm):

    class Meta:
        model = AV

        fields = [
            "importateur",
            "num_av",
            "num_nif",
            "license",
            "dateValidation",
            "valeurApprouvee",
        ]

        widgets = {

            "importateur": forms.Select(attrs={
                "class": "form-select"
            }),

            "num_av": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Numéro AV"
            }),

            "num_nif": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "NIF"
            }),

            "license": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Licence"
            }),

            "dateValidation": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "valeurApprouvee": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Valeur approuvée"
            }),

        }


# =========================
# AV PRODUIT FORM
# =========================
class AVProduitForm(forms.ModelForm):

    class Meta:
        model = AVProduit

        fields = [
            "produit",
            "quantite",
            "prix_unitaire"
        ]

        widgets = {

            "produit": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nom produit"
            }),

            "quantite": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Quantité"
            }),

            "prix_unitaire": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Prix unitaire"
            }),

        }

    # =========================
    # VALIDATION PRODUIT AV
    # =========================
    def clean(self):

        cleaned_data = super().clean()

        quantite = cleaned_data.get("quantite") or 0
        prix_unitaire = cleaned_data.get("prix_unitaire") or 0

        if quantite <= 0:
            raise forms.ValidationError(
                "La quantité doit être supérieure à 0"
            )

        if prix_unitaire <= 0:
            raise forms.ValidationError(
                "Le prix unitaire doit être supérieur à 0"
            )

        return cleaned_data


# =========================
# DECLARATION FORM
# =========================
class DeclarationForm(forms.ModelForm):

    class Meta:
        model = Declaration

        fields = [
            "av_produit",
            "article",
            "quantite",
            "prixUnitaire",
            "bureauDouane",
            "position_tarifaire",
            "norme_appliquee",
            "mum_E",
        ]

        widgets = {

            "av_produit": forms.Select(attrs={
                "class": "form-select"
            }),

            "article": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Article"
            }),

            "quantite": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Quantité déclarée"
            }),

            "prixUnitaire": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Prix unitaire déclaré"
            }),

            "bureauDouane": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Bureau Douane"
            }),

            "position_tarifaire": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Position tarifaire"
            }),

            "norme_appliquee": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Norme appliquée"
            }),

            "mum_E": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "MUM E"
            }),

        }

    # =========================
    # VALIDATION ERP
    # =========================
    def clean(self):

        cleaned_data = super().clean()

        av_produit = cleaned_data.get("av_produit")
        quantite = cleaned_data.get("quantite") or 0
        prix = cleaned_data.get("prixUnitaire") or 0

        if not av_produit:
            return cleaned_data

        # =========================
        # QUANTITÉ RESTANTE
        # =========================
        total_qte_utilisee = sum(
            d.quantite
            for d in av_produit.declarations.exclude(id=self.instance.id)
        )

        quantite_restante = av_produit.quantite - total_qte_utilisee

        # =========================
        # VALEUR RESTANTE
        # =========================
        total_valeur_utilisee = sum(
            d.valeur_totale
            for d in av_produit.declarations.exclude(id=self.instance.id)
        )

        valeur_restante = (
            av_produit.valeur_initiale - total_valeur_utilisee
        )

        nouvelle_valeur = quantite * prix

        # =========================
        # VALIDATION QUANTITÉ
        # =========================
        if quantite > quantite_restante:

            raise forms.ValidationError(
                f"❌ Quantité insuffisante. Reste: {quantite_restante}"
            )

        # =========================
        # VALIDATION VALEUR
        # =========================
        if nouvelle_valeur > valeur_restante:

            raise forms.ValidationError(
                f"❌ Valeur AV insuffisante. Reste: {valeur_restante}"
            )

        return cleaned_data
    
from django import forms
from .models import AVProduit


class AVProduitForm(forms.ModelForm):

    class Meta:

        model = AVProduit

        fields = [
            "av",
            "produit",
            "quantite",
            "prix_unitaire"
        ]

        widgets = {

            "av": forms.Select(attrs={
                "class": "form-select"
            }),

            "produit": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "quantite": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "prix_unitaire": forms.NumberInput(attrs={
                "class": "form-control"
            }),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["produit"].label_from_instance = lambda obj: obj.nom


# =====form user ======
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': "Nom d'utilisateur"
            }),

            'email': forms.EmailInput(attrs={
                'placeholder': "Email"
            }),

            'role': forms.Select(),

            'password1': forms.PasswordInput(attrs={
                'placeholder': "Mot de passe"
            }),

            'password2': forms.PasswordInput(attrs={
                'placeholder': "Confirmation mot de passe"
            }),
        }
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']

    def clean_role(self):
        role = self.cleaned_data.get('role')

        # ❌ bloquer admin
        if role == 'admin':
            raise forms.ValidationError("Vous ne pouvez pas vous attribuer le rôle admin.")

        return role