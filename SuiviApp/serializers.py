from rest_framework import serializers
from .models import AV, AVProduit, Declaration


# =========================
# DECLARATION
# =========================
class DeclarationSerializer(serializers.ModelSerializer):

    valeur_totale = serializers.ReadOnlyField()

    class Meta:
        model = Declaration
        fields = [
            "id",
            "av_produit",
            "article",
            "quantite",
            "prixUnitaire",
            "bureauDouane",
            "position_tarifaire",
            "norme_appliquee",
            "mum_E",
            "valeur_totale",
        ]


# =========================
# AV PRODUIT
# =========================
class AVProduitSerializer(serializers.ModelSerializer):

    valeur_initiale = serializers.ReadOnlyField()
    valeur_consomme = serializers.ReadOnlyField()
    valeur_restante = serializers.ReadOnlyField()

    declarations = DeclarationSerializer(many=True, read_only=True)

    class Meta:
        model = AVProduit
        fields = [
            "id",
            "av",
            "produit",
            "quantite",
            "prix_unitaire",
            "valeur_initiale",
            "valeur_consomme",
            "valeur_restante",
            "declarations",
        ]


# =========================
# AV
# =========================
class AVSerializer(serializers.ModelSerializer):

    produits = AVProduitSerializer(many=True, read_only=True)

    valeur_consomme = serializers.ReadOnlyField()
    valeur_restante = serializers.ReadOnlyField()
    statut = serializers.ReadOnlyField()

    class Meta:
        model = AV
        fields = [
            "id",
            "importateur",
            "num_av",
            "num_nif",
            "license",
            "dateValidation",
            "valeurApprouvee",
            "valeur_consomme",
            "valeur_restante",
            "statut",
            "produits",
        ]