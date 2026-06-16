from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser
 

import uuid
from django.db import models


class UUIDModel(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    class Meta:
        abstract = True

    
class CustomUser(AbstractUser):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'Utilisateur'),
    )

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user'
    )

    
    # 🔥 AJOUT IMPORTANT
    is_active = models.BooleanField(default=True)
    def save(self, *args, **kwargs):

        # 🔥 si superuser → role admin automatiquement
        if self.is_superuser:
            self.role = 'admin'

        super().save(*args, **kwargs)

# ========VUE TOGGLE ACTIVER / DÉSACTIVER UTILISATEUR========

from django.shortcuts import get_object_or_404, redirect
from .models import CustomUser

def toggle_user_status(request, id):

    user = get_object_or_404(CustomUser, id=id)

    # bascule état
    user.is_active = not user.is_active
    user.save()

    return redirect('SuiviApp:user_list')
# =========================
# IMPORTATEUR
# =========================
class Importateur(UUIDModel):

    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    num_telephone = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.nom


# =========================
# AV
# =========================
class AV(UUIDModel):

    importateur = models.ForeignKey(
        Importateur,
        on_delete=models.CASCADE,
        related_name="avs"
    )

    num_av = models.CharField(max_length=100)
    num_nif = models.CharField(max_length=100)
    license = models.CharField(max_length=100)

    dateValidation = models.DateField()

    # BUDGET GLOBAL AV
    valeurApprouvee = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.num_av

    # =========================
    # TOTAL PRODUITS
    # =========================
    @property
    def total_produits(self):
        return self.produits.count()

    # =========================
    # VALEUR CONSOMMÉE
    # =========================
    @property
    def valeur_consomme(self):

        total = sum(
            p.valeur_consomme
            for p in self.produits.all()
        )

        return total or Decimal("0.00")

    # =========================
    # VALEUR RESTANTE
    # =========================
    @property
    def valeur_restante(self):

        restant = self.valeurApprouvee - self.valeur_consomme

        if restant < 0:
            return Decimal("0.00")

        return restant

    # =========================
    # PROGRESSION %
    # =========================
    @property
    def progression(self):

        if self.valeurApprouvee <= 0:
            return 0

        return round(
            (self.valeur_consomme / self.valeurApprouvee) * 100,
            2
        )

    # =========================
    # STATUT
    # =========================
    @property
    def statut(self):

        if self.valeur_restante <= 0:
            return "ÉPUISÉ"

        elif self.progression >= 70:
            return "CRITIQUE"

        return "ACTIF"


# =========================
# PRODUITS AV
# =========================
class AVProduit(UUIDModel):

    av = models.ForeignKey(
        AV,
        on_delete=models.CASCADE,
        related_name="produits"
    )

    produit = models.CharField(max_length=255)

    quantite = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    prix_unitaire = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.produit} - {self.av.num_av}"

    # =========================
    # VALEUR INITIALE
    # =========================
    @property
    def valeur_initiale(self):

        return self.quantite * self.prix_unitaire

    # =========================
    # QUANTITÉ CONSOMMÉE
    # =========================
    @property
    def quantite_consomme(self):

        total = sum(
            d.quantite
            for d in self.declarations.all()
        )

        return total or Decimal("0.00")

    # =========================
    # QUANTITÉ RESTANTE
    # =========================
    @property
    def quantite_restante(self):

        restant = self.quantite - self.quantite_consomme

        if restant < 0:
            return Decimal("0.00")

        return restant

    # =========================
    # VALEUR CONSOMMÉE
    # =========================
    @property
    def valeur_consomme(self):

        total = sum(
            d.valeur_totale
            for d in self.declarations.all()
        )

        return total or Decimal("0.00")

    # =========================
    # VALEUR RESTANTE
    # =========================
    @property
    def valeur_restante(self):

        restant = self.valeur_initiale - self.valeur_consomme

        if restant < 0:
            return Decimal("0.00")

        return restant

    # =========================
    # STATUT
    # =========================
    @property
    def statut(self):

        if self.quantite_restante <= 0:
            return "ÉPUISÉ"

        elif self.quantite_restante <= (self.quantite * Decimal("0.2")):
            return "STOCK FAIBLE"

        return "DISPONIBLE"


# =========================
# DECLARATION
# =========================
class Declaration(UUIDModel):

    av_produit = models.ForeignKey(
        AVProduit,
        on_delete=models.CASCADE,
        related_name="declarations"
    )

    article = models.CharField(max_length=255)

    quantite = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    prixUnitaire = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    bureauDouane = models.CharField(max_length=255)
    position_tarifaire = models.CharField(max_length=255)
    norme_appliquee = models.CharField(max_length=255)
    mum_E = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.article

    # =========================
    # VALEUR TOTALE
    # =========================
    @property
    def valeur_totale(self):

        return self.quantite * self.prixUnitaire

    # =========================
    # VALIDATION ERP
    # =========================
    def clean(self):

        if not self.av_produit:
            return

        declarations = self.av_produit.declarations.exclude(id=self.id)

        # =========================
        # QUANTITÉ DÉJÀ UTILISÉE
        # =========================
        qty_used = sum(
            d.quantite
            for d in declarations
        )

        qty_disponible = self.av_produit.quantite - qty_used

        if self.quantite > qty_disponible:
            raise ValidationError(
                "❌ Quantité AV insuffisante"
            )

        # =========================
        # VALEUR DÉJÀ UTILISÉE
        # =========================
        value_used = sum(
            d.valeur_totale
            for d in declarations
        )

        value_disponible = (
            self.av_produit.valeur_initiale - value_used
        )

        if self.valeur_totale > value_disponible:
            raise ValidationError(
                "❌ Valeur AV insuffisante"
            )

        # =========================
        # VÉRIFICATION AV GLOBAL
        # =========================
        av = self.av_produit.av

        av_used = av.valeur_consomme - value_used

        av_disponible = av.valeurApprouvee - av_used

        if self.valeur_totale > av_disponible:
            raise ValidationError(
                "❌ Budget AV global insuffisant"
            )

    # =========================
    # SAVE ERP
    # =========================
    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)


# models.py

class Appurement(UUIDModel):

    av = models.ForeignKey(
        AV,
        on_delete=models.CASCADE,
        related_name="appurements"
    )

    numero = models.CharField(max_length=100)
    numero_e = models.CharField(max_length=100, blank=True, null=True)
    datee = models.DateField()

    bureau_douane = models.CharField(max_length=255)

    fob = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cif = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    appurement_fob = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    appurement_cif = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    poids = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.numero