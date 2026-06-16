def get_av_stock(av):
    consumed_fob = sum(d.fob for d in av.declarations.all())
    consumed_qte = sum(d.quantite for d in av.declarations.all())
    consumed_poids = sum(d.poids for d in av.declarations.all())
    consumed_prix = sum(d.prixUnitaire for d in av.declarations.all())

    return {
        "restant_fob": av.valeurApprouvee - consumed_fob,
        "restant_qte": av.quantite - consumed_qte,
        "restant_poids": av.poids - consumed_poids,
        "restant_prix": av.prixUnitaire - consumed_prix,
    }


from decimal import Decimal

def safe_subtract(value, minus):
    value = value or Decimal("0")
    minus = minus or Decimal("0")

    result = value - minus
    return result if result > 0 else Decimal("0")