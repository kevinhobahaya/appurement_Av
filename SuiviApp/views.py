from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.core.paginator import Paginator
from decimal import Decimal

from .models import *
from .forms import *
# ======user ======
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserRegisterForm
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def role_required(roles=[]):

    def decorator(view_func):

        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect("SuiviApp:login")

            if request.user.role not in roles:
                return redirect("SuiviApp:login")

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


@role_required("admin")
def user_list(request):
    ...

def user_list(request):
    users = User.objects.all()

    return render(request, "users/list_user.html", {
        "users": users
    })
# =======create user ======
def user_create(request):

    form = UserRegisterForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("SuiviApp:user_list")

    return render(request, "users/user_form.html", {
        "form": form,
        "title": "Ajouter utilisateur"
    })
# =======update user ======
from django.shortcuts import get_object_or_404, render, redirect
from .models import CustomUser
from .forms import UserRegisterForm
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser
from .forms import UserRegisterForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser
from .forms import UserRegisterForm

from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser
from .forms import UserRegisterForm

from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser
from .forms import UserRegisterForm


from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser
from .forms import UserRegisterForm


def user_update(request, uuid):
    user = get_object_or_404(CustomUser, uuid=uuid)

    if request.method == "POST":
        form = UserRegisterForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect("SuiviApp:user_list")
    else:
        form = UserRegisterForm(instance=user)

    return render(request, "users/user_form.html", {
        "form": form
    })
# =======delete user ======
from django.shortcuts import get_object_or_404, redirect
from .models import CustomUser

def user_delete(request, uuid):
    user = get_object_or_404(CustomUser, uuid=uuid)

    user.delete()

    return redirect('SuiviApp:user_list')
# ======= login =====
from django.contrib.auth import authenticate, login


from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def login_view(request):

    if request.user.is_authenticated:
        return redirect("SuiviApp:av_list")

    error = None

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 🔥 redirection selon rôle
            if user.role == "ADMIN":
                return redirect("SuiviApp:home")
            elif user.role == "AGENT":
                return redirect("SuiviApp:home")
            elif user.role == "Utilisateur":
                return redirect("SuiviApp:home")
            else:
                return redirect("SuiviApp:home")

        else:
            error = "Identifiants incorrects"

    return render(request, "users/login.html", {"error": error})

# ====logout =====
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect("SuiviApp:login")
# =========================================================
# ERP DASHBOARD
# =========================================================
def erp_dashboard(request):

    data = []

    avs = AV.objects.select_related(
        "importateur"
    ).prefetch_related(
        "produits__declarations"
    ).order_by("-id")

    for av in avs:

        total = av.valeurApprouvee
        consomme = av.valeur_consomme
        restant = av.valeur_restante
        progress = av.progression

        if progress >= 100:
            color = "red"
            statut = "ÉPUISÉ"

        elif progress >= 70:
            color = "orange"
            statut = "CRITIQUE"

        else:
            color = "green"
            statut = "ACTIF"

        data.append({
            "av": av,
            "total": total,
            "consomme": consomme,
            "restant": restant,
            "progress": progress,
            "color": color,
            "statut": statut,
        })

    return render(request, "admin/home.html", {
        "data": data
    })


# =========================================================
# AV LIST
from django.core.paginator import Paginator

def av_list(request):

    search = request.GET.get("search", "")

    data = AV.objects.all()

    if search:
        data = data.filter(
            num_av__icontains=search
        )

    paginator = Paginator(data, 5)  # 5 AV par page

    page = request.GET.get("page")

    data = paginator.get_page(page)

    return render(
        request,
        "av/avs.html",
        {
            "data": data,
            "search": search
        }
    )
# =========================================================
# AV CREATE
# =========================================================
def av_create(request):

    form = AVForm(request.POST or None)

    if form.is_valid():

        av = form.save()

        messages.success(
            request,
            "AV créé avec succès"
        )

        return redirect(
            "SuiviApp:av_detail",
            av.uuid
        )

    return render(request, "av/av_form.html", {
        "form": form,
        "title": "Créer AV"
    })


# =========================================================
# AV UPDATE
# =========================================================
def av_update(request, uuid):

    av = get_object_or_404(
        AV,
        uuid=uuid
    )

    form = AVForm(
        request.POST or None,
        instance=av
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            "AV modifié avec succès"
        )

        return redirect("SuiviApp:av_list")

    return render(request, "av/av_form.html", {
        "form": form,
        "title": "Modifier AV"
    })


# =========================================================
# AV DELETE
# =========================================================
def av_delete(request, uuid):

    av = get_object_or_404(
        AV,
        uuid=uuid
    )

    if av.produits.exists():

        messages.error(
            request,
            "Impossible : cet AV contient déjà des produits"
        )

        return redirect("SuiviApp:av_list")

    av.delete()

    messages.success(
        request,
        "AV supprimé avec succès"
    )

    return redirect("SuiviApp:av_list")


# =========================================================
# AV DETAIL
# =========================================================
from django.shortcuts import render, get_object_or_404
from .models import AV

def av_detail(request, uuid):

    av = get_object_or_404(
        AV.objects.prefetch_related(
            "produits__declarations",
            "appurements"
        ),
        uuid=uuid
    )

    return render(request, "av/av_detail.html", {
        "av": av
    })
# =========================================================
# AV PRODUIT CREATE
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AVProduitForm

def av_produit_create(request):

    form = AVProduitForm(request.POST or None)

    if form.is_valid():
        av_produit = form.save(commit=False)

        # 🔥 (OPTIONNEL MAIS ERP IMPORTANT)
        # recalcul automatique valeur initiale si ton model ne le fait pas
        if hasattr(av_produit, "quantite") and hasattr(av_produit, "prix_unitaire"):
            av_produit.valeur_initiale = av_produit.quantite * av_produit.prix_unitaire

        av_produit.save()

        messages.success(request, "Produit AV ajouté avec succès")

        return redirect("SuiviApp:av_produit_list")

    return render(request, "avProduit/avproduit_form.html", {
        "form": form,
        "title": "Ajouter AVProduit"
    })
# =========================================================
# DECLARATION LIST
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def register_view(request):

    form = UserCreationForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Utilisateur créé avec succès")
        return redirect("SuiviApp:login")

    return render(request, "users/register.html", {
        "form": form
    })
# =========================================================
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Declaration


def declaration_list(request):

    search = request.GET.get("search", "").strip()

    declarations = Declaration.objects.select_related(
        "av_produit",
        "av_produit__av"
    ).order_by("-id")

    if search:
        declarations = declarations.filter(
            Q(article__icontains=search) |
            Q(av_produit__produit__icontains=search) |
            Q(av_produit__av__num_av__icontains=search)
        )

    paginator = Paginator(declarations, 5)  # 5 par page

    page_number = request.GET.get("page")

    data = paginator.get_page(page_number)

    return render(request, "declaration/declarations.html", {
        "data": data,
        "search": search
    })

# =========================================================
# DECLARATION CREATE
# =========================================================
def declaration_create(request):

    form = DeclarationForm(request.POST or None)

    if form.is_valid():

        try:

            declaration = form.save()

            messages.success(
                request,
                "Déclaration enregistrée avec succès"
            )

            return redirect("SuiviApp:declaration_list")

        except Exception as e:

            messages.error(
                request,
                str(e)
            )

    return render(request, "declaration/declaration_form.html", {
        "form": form,
        "title": "Ajouter Déclaration"
    })


# =========================================================
# DECLARATION UPDATE
# =========================================================
def declaration_update(request, uuid):

    declaration = get_object_or_404(
        Declaration,
        uuid=uuid
    )

    form = DeclarationForm(
        request.POST or None,
        instance=declaration
    )

    if form.is_valid():

        try:

            form.save()

            messages.success(
                request,
                "Déclaration modifiée avec succès"
            )

            return redirect("SuiviApp:declaration_list")

        except Exception as e:

            messages.error(
                request,
                str(e)
            )

    return render(request, "declaration/declaration_form.html", {
        "form": form,
        "title": "Modifier Déclaration"
    })


# =========================================================
# DECLARATION DELETE
# =========================================================
def declaration_delete(request, uuid):

    declaration = get_object_or_404(
        Declaration,
        uuid=uuid
    )

    declaration.delete()

    messages.success(
        request,
        "Déclaration supprimée avec succès"
    )

    return redirect("SuiviApp:declaration_list")


# =========================================================
# DECLARATION DETAIL
# =========================================================
def declaration_detail(request, uuid):

    declaration = get_object_or_404(
        Declaration.objects.select_related(
            "av_produit",
            "av_produit__av"
        ),
        uuid=uuid
    )

    av_produit = declaration.av_produit

    av = av_produit.av

    quantite_restante = av_produit.quantite_restante

    valeur_restante = av_produit.valeur_restante

    valeur_declaration = declaration.valeur_totale

    alertes = []

    seuil = av_produit.quantite * Decimal("0.2")

    if quantite_restante <= 0:

        alertes.append("❌ Stock AV épuisé ou la quantité")

    elif quantite_restante <= seuil:

        alertes.append("⚠️ Stock AV faible ou la quantité")

    else:

        alertes.append("✅ Stock AV disponible")

    if valeur_restante <= 0:

        alertes.append("❌ Valeur AV épuisée")

    return render(request, "declaration/declaration_detail.html", {
        "declaration": declaration,
        "av_produit": av_produit,
        "av": av,
        "quantite_restante": quantite_restante,
        "valeur_restante": valeur_restante,
        "valeur_declaration": valeur_declaration,
        "alertes": alertes
    })


# =========================================================
# IMPORTATEUR LIST
# =========================================================
def importateurs_list(request):

    search = request.GET.get("search", "")

    data = Importateur.objects.annotate(
        nb_av=Count("avs")
    ).order_by("-id")

    if search:

        data = data.filter(
            Q(nom__icontains=search) |
            Q(email__icontains=search) |
            Q(num_telephone__icontains=search)
        )

    paginator = Paginator(data, 10)

    page = request.GET.get("page")

    data = paginator.get_page(page)

    return render(request, "admin/importateurs.html", {
        "data": data,
        "search": search
    })


# =========================================================
# IMPORTATEUR DETAIL
# =========================================================
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from decimal import Decimal

from .models import Importateur


def importateur_detail(request, uuid):
    importateur = get_object_or_404(
        Importateur.objects.prefetch_related(
            "avs__produits__declarations"
        ),
        uuid=uuid
    )

    avs = importateur.avs.all().order_by("-id")

    total_av = avs.count()

    total_valeur = avs.aggregate(
        total=Sum("valeurApprouvee")
    )["total"] or Decimal("0.00")

    total_consomme = sum(
        av.valeur_consomme for av in avs
    )

    total_restant = total_valeur - total_consomme

    return render(request, "admin/importateur_detail.html", {
        "importateur": importateur,
        "avs": avs,
        "total_av": total_av,
        "total_valeur": total_valeur,
        "total_consomme": total_consomme,
        "total_restant": total_restant,
    })

# =========================================================
# IMPORTATEUR CREATE
# =========================================================
def importateur_create(request):

    form = ImportateurForm(request.POST or None)

    if form.is_valid():

        form.save()

        messages.success(
            request,
            "Importateur ajouté avec succès"
        )

        return redirect("SuiviApp:importateur")

    return render(request, "admin/importateur_form.html", {
        "form": form,
        "title": "Ajouter Importateur"
    })


# =========================================================
# IMPORTATEUR UPDATE
# =========================================================
def importateur_update(request, uuid):

    obj = get_object_or_404(
        Importateur,
        uuid=uuid
    )

    form = ImportateurForm(
        request.POST or None,
        instance=obj
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            "Importateur modifié avec succès"
        )

        return redirect("SuiviApp:importateur")

    return render(request, "admin/importateur_form.html", {
        "form": form,
        "title": "Modifier Importateur"
    })


# =========================================================
# IMPORTATEUR DELETE
# =========================================================
def importateur_delete(request, uuid):

    obj = get_object_or_404(
        Importateur,
        uuid=uuid
    )

    obj.delete()

    messages.success(
        request,
        "Importateur supprimé avec succès"
    )

    return redirect("SuiviApp:importateur")

# ===========avProuit ==========

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import AV, AVProduit
from .forms import AVProduitForm

# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import AV, AVProduit
from .forms import AVProduitForm


# =========================
# LISTE AVPRODUIT
# =========================
from django.shortcuts import render
from django.db.models import Sum
from .models import AVProduit
from django.shortcuts import render
from django.db.models import Sum
from .models import AVProduit

from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render
from .models import AVProduit


from django.core.paginator import Paginator
from django.shortcuts import render
from .models import AVProduit

def av_produit_list(request):

    produits = (
        AVProduit.objects
        .select_related("av", "av__importateur")
        .order_by("av__num_av", "produit")
    )

    paginator = Paginator(produits, 5)
    page_number = request.GET.get("page")
    produits_page = paginator.get_page(page_number)

    return render(request, "avProduit/avproduit_list.html", {
        "produits": produits_page
    })
# =========================
# AJOUT AVPRODUIT
# =========================
def av_produit_create(request):

    form = AVProduitForm(request.POST or None)

    if form.is_valid():

        form.save()

        messages.success(
            request,
            "Produit AV ajouté avec succès"
        )

        return redirect("SuiviApp:av_produit_list")

    return render(request, "avProduit/avproduit_form.html", {
        "form": form,
        "title": "Ajouter AVProduit"
    })


# =========================
# MODIFIER AVPRODUIT
# =========================
def av_produit_update(request, uuid):

    produit = get_object_or_404(
        AVProduit,
        uuid=uuid
    )

    form = AVProduitForm(
        request.POST or None,
        instance=produit
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            "Produit AV modifié avec succès"
        )

        return redirect("SuiviApp:av_produit_list")

    return render(request, "avProduit/avproduit_form.html", {
        "form": form,
        "title": "Modifier AVProduit"
    })


# =========================
# DETAIL AVPRODUIT
# =========================
def av_produit_detail(request, uuid):

    produit = get_object_or_404(
        AVProduit.objects.select_related(
            "av",
            "av__importateur"
        ),
        uuid=uuid
    )

    return render(request, "avProduit/avproduit_detail.html", {
        "produit": produit
    })


# =========================
# SUPPRIMER AVPRODUIT
# =========================
def av_produit_delete(request, pk):

    produit = get_object_or_404(
        AVProduit,
        uuid=uuid
    )

    if request.method == "POST":

        produit.delete()

        messages.success(
            request,
            "Produit AV supprimé avec succès"
        )

        return redirect("SuiviApp:av_produit_list")

    return render(request, "avProduit/avproduit_delete.html", {
        "produit": produit
    })

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def register_user(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # sécurité supplémentaire
            if user.role == 'admin':
                user.role = 'user'

            user.save()

            return redirect('SuiviApp:login')

    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

# ======= toggle user active status ======
from django.shortcuts import get_object_or_404, redirect
from .models import CustomUser

from django.shortcuts import get_object_or_404, redirect

def toggle_user_status(request, uuid):

    user = get_object_or_404(
        CustomUser,
        uuid=uuid
    )

    user.is_active = not user.is_active
    user.save()

    return redirect('SuiviApp:user_list')


# ==========EXPORT EXCEL (IMPORTATEUR DETAIL) =========
import openpyxl
from django.http import HttpResponse
from .models import Importateur

def export_excel_importateur(request, uuid):
    importateur = Importateur.objects.get(uuid=uuid)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "AV Importateur"

    ws.append(["AV", "Produit", "Quantité", "Valeur"])

    for av in importateur.avs.all():
        for p in av.produits.all():
            ws.append([
                av.num_av,
                p.produit,
                p.quantite,
                av.valeurApprouvee
            ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="importateur.xlsx"'
    wb.save(response)

    return response

# ===================EXPORT PDF (REPORTLAB) ===================
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def export_pdf_importateur(request, uuid):
    importateur = Importateur.objects.get(uuid=uuid)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="importateur.pdf"'

    p = canvas.Canvas(response)

    y = 800
    p.drawString(100, y, f"Importateur: {importateur.nom}")

    for av in importateur.avs.all():
        y -= 30
        p.drawString(100, y, f"AV: {av.num_av} - Valeur: {av.valeurApprouvee}")

    p.showPage()
    p.save()

    return response

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
import os

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image,
    HRFlowable
)

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
import os

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image,
    HRFlowable
)

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

from .models import AV, Declaration


def av_pdf(request, uuid):

    # =====================================================
    # RECUPERATION AV
    # =====================================================

    av = get_object_or_404(AV, uuid=uuid)

    # =====================================================
    # RESPONSE PDF
    # =====================================================

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = (
        'inline; filename="apurement_occ.pdf"'
    )

    # =====================================================
    # DOCUMENT PDF
    # =====================================================

    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=10,
        leftMargin=10,
        topMargin=45,
        bottomMargin=10
    )

    elements = []

    styles = getSampleStyleSheet()

    # =====================================================
    # LOGO OCC
    # =====================================================

    logo_path = os.path.join(
        settings.BASE_DIR,
        "static/part4.png"
    )

    try:

        logo = Image(
            logo_path,
            width=4.4 * cm,
            height=2.2 * cm
        )

    except:

        logo = ""

    # =====================================================
    # HEADER EXACT COMME PHOTO OCC
    # =====================================================

    occ = Paragraph("""
    <font size="12">
    <b>OFFICE CONGOLAIS DE CONTROLE</b>
    </font>
    """, styles['Normal'])

    direction = Paragraph("""
    <font size="10">
    DIRECTION PROVINCIALE DU NORD-KIVU<br/>
    AGENCE DE BENI<br/>
    <u><b>DETACHEMENT DE KASINDI</b></u>
    </font>
    """, styles['Normal'])

    header = Table([
        [occ],
        [logo],
        [direction],
    ])

    header.setStyle(TableStyle([

        # TOUT A GAUCHE
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),

        # LOGO A GAUCHE AUSSI
        ('ALIGN', (0,1), (0,1), 'LEFT'),

        ('VALIGN', (0,0), (-1,-1), 'TOP'),

        # ESPACE DEPUIS LE BORD
        ('LEFTPADDING', (0,0), (-1,-1), 60),

        ('TOPPADDING', (0,0), (-1,-1), 0),

        ('BOTTOMPADDING', (0,0), (-1,-1), 1),

    ]))

    elements.append(header)

    elements.append(Spacer(1, 0.3 * cm))

    # =====================================================
    # TITRE PRINCIPAL
    # =====================================================

    title = Table(
        [["APUREMENT ATTESTATION DE VERIFICATION"]],
        colWidths=[18 * cm]
    )

    title.setStyle(TableStyle([

        ('BACKGROUND', (0,0), (-1,-1),
         colors.HexColor("#D9D9D9")),

        ('ALIGN', (0,0), (-1,-1), 'CENTER'),

        ('FONTNAME', (0,0), (-1,-1),
         'Helvetica-Bold'),

        ('FONTSIZE', (0,0), (-1,-1), 12),

        ('TOPPADDING', (0,0), (-1,-1), 5),

        ('BOTTOMPADDING', (0,0), (-1,-1), 5),

    ]))

    elements.append(title)

    elements.append(Spacer(1, 0.3 * cm))

    # =====================================================
    # INFOS IMPORTATEUR
    # =====================================================

    nif = getattr(
        av.importateur,
        "nif",
        "A1310202F"
    )

    info_importateur = [

        [f"NOM : {av.importateur.nom}"],

        [f"NIF : {nif}"]

    ]

    info_table = Table(
        info_importateur,
        colWidths=[18 * cm]
    )

    info_table.setStyle(TableStyle([

        ('FONTNAME', (0,0), (-1,-1),
         'Helvetica-Bold'),

        ('FONTSIZE', (0,0), (-1,-1), 10),

        ('BOTTOMPADDING', (0,0), (-1,-1), 3),

    ]))

    elements.append(info_table)

    elements.append(Spacer(1, 0.3 * cm))

    # =====================================================
    # AV + LICENCE
    # =====================================================

    licence = getattr(av, "license", "-")

    av_info = Table([[
        f"AV : {av.num_av}\nLicence : {licence}"
    ]], colWidths=[18 * cm])

    av_info.setStyle(TableStyle([

        ('BACKGROUND', (0,0), (-1,-1),
         colors.HexColor("#EFEFEF")),

        ('ALIGN', (0,0), (-1,-1), 'CENTER'),

        ('FONTNAME', (0,0), (-1,-1),
         'Helvetica-Bold'),

        ('FONTSIZE', (0,0), (-1,-1), 10),

        ('TOPPADDING', (0,0), (-1,-1), 4),

        ('BOTTOMPADDING', (0,0), (-1,-1), 4),

    ]))

    elements.append(av_info)

    elements.append(Spacer(1, 0.4 * cm))

    # =====================================================
    # TABLEAU PRINCIPAL
    # =====================================================

    data = [[

        "N°",
        "N° E",
        "DATE",
        "BUREAU DE DOUANE",
        "FOB EN USD",
   
        "APUREMENT FOB AV",
        
        "POIDS EN KG"

    ]]

    declarations = Declaration.objects.filter(
        av_produit__av=av
    )

    total_fob = 0
    
    total_poids = 0

    index = 1

    for d in declarations:

        fob = d.valeur_totale
        
        poids = d.quantite

        total_fob += fob
      
        total_poids += poids

        data.append([

            str(index),

            d.mum_E if d.mum_E else "-",

            d.created_at.strftime("%d/%m/%Y"),

            d.bureauDouane if d.bureauDouane else "-",

            f"{fob:,.2f}",

           
            f"{av.valeur_restante:,.2f}",

           

            f"{poids:,.2f}"

        ])

        index += 1

    # =====================================================
    # TOTAL
    # =====================================================

    data.append([

        "",
        "",
        "",
        "TOTAL",

        f"{total_fob:,.2f}",

       

        "",

        f"{total_poids:,.2f}"

    ])

    # =====================================================
    # TABLEAU STYLE
    # =====================================================

    table = Table(
        data,
        repeatRows=1
    )

    table.setStyle(TableStyle([

        # HEADER
        ('BACKGROUND', (0,0), (-1,0),
         colors.HexColor("#D9D9D9")),

        ('TEXTCOLOR', (0,0), (-1,0),
         colors.black),

        ('FONTNAME', (0,0), (-1,0),
         'Helvetica-Bold'),

        ('FONTSIZE', (0,0), (-1,-1), 7),

        # GRID
        ('GRID', (0,0), (-1,-1),
         0.7, colors.black),

        # ALIGNEMENT
        ('ALIGN', (0,0), (-1,-1),
         'CENTER'),

        ('VALIGN', (0,0), (-1,-1),
         'MIDDLE'),

        # BODY
        ('BACKGROUND', (0,1), (-1,-2),
         colors.white),

        # TOTAL
        ('BACKGROUND', (0,-1), (-1,-1),
         colors.HexColor("#EFEFEF")),

        ('FONTNAME', (0,-1), (-1,-1),
         'Helvetica-Bold'),

        # PADDING
        ('TOPPADDING', (0,0), (-1,-1), 4),

        ('BOTTOMPADDING', (0,0), (-1,-1), 4),

    ]))

    elements.append(table)

    elements.append(Spacer(1, 1 * cm))

    # =====================================================
    # SIGNATURE
    # =====================================================

    elements.append(HRFlowable(width="30%"))

    elements.append(Paragraph(
        "<b>Signature & Cachet OCC</b>",
        styles['Normal']
    ))

    # =====================================================
    # GENERATION PDF
    # =====================================================

    doc.build(elements)

    return response

def parametres(request):
    return render(request, "users/parametres.html")

from django.shortcuts import get_object_or_404, render
from .models import AVProduit

def av_produit_detail(request, uuid):

    produit = get_object_or_404(
        AVProduit.objects.select_related("av", "av__importateur"),
        uuid=uuid
    )

    # declarations liées
    declarations = produit.declarations.all()

    return render(request, "avProduit/detail.html", {
        "produit": produit,
        "declarations": declarations
    })

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.conf import settings

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

import os


def av_produit_pdf(request, uuid):

    produit = get_object_or_404(
        AVProduit.objects.select_related(
            "av",
            "av__importateur"
        ),
        uuid=uuid
    )

    declarations = produit.declarations.all()

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = f'attachment; filename="AV_{produit.av.num_av}.pdf"'

    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=10,
        leftMargin=10,
        topMargin=35,
        bottomMargin=10
    )

    styles = getSampleStyleSheet()
    elements = []

    # =====================================================
    # LOGO OCC
    # =====================================================

    logo_path = os.path.join(
        settings.BASE_DIR,
        "static",
        "part4.png"
    )

    try:

        logo = Image(
            logo_path,
            width=4.5 * cm,
            height=2.4 * cm
        )

    except:

        logo = Spacer(1, 1)

    # =====================================================
    # HEADER OCC
    # =====================================================

    occ = Paragraph(
        """
        <font size="12">
        <b>OFFICE CONGOLAIS DE CONTROLE</b>
        </font>
        """,
        styles["Normal"]
    )

    direction = Paragraph(
        """
        <font size="10">
        DIRECTION PROVINCIALE DU NORD-KIVU<br/>
        AGENCE DE BENI<br/>
        <u><b>DETACHEMENT DE KASINDI</b></u>
        </font>
        """,
        styles["Normal"]
    )

    header = Table(
        [
            [occ],
            [logo],
            [direction]
        ],
        colWidths=[18 * cm]
    )

    header.setStyle(TableStyle([

        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),

        # déplacer le bloc vers la gauche
        ('LEFTPADDING', (0,0), (-1,-1), 20),

        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),

        ('BOX', (0,0), (-1,-1), 0, colors.white),
        ('GRID', (0,0), (-1,-1), 0, colors.white),

    ]))

    elements.append(header)

    elements.append(
        Spacer(
            1,
            0.5 * cm
        )
    )

    # =====================================================
    # TITRE
    # =====================================================

    titre = Paragraph(
        f"""
        <para align="center">
        <font size="16">
        <b>FICHE DE SUIVI AV PRODUIT</b>
        </font>
        <br/>
        N° {produit.av.num_av}
        </para>
        """,
        styles["Normal"]
    )

    elements.append(titre)
    elements.append(Spacer(1, 15))

    # =====================================================
    # INFOS AV
    # =====================================================

    info_data = [

        ["AV", produit.av.num_av],

        ["Importateur",
         produit.av.importateur.nom],

        ["Produit",
         produit.produit],

        ["Quantité",
         str(produit.quantite)],

        ["Valeur initiale",
         str(produit.valeur_initiale)],

        ["Valeur consommée",
         str(produit.valeur_consomme)],

        ["Valeur restante",
         str(produit.valeur_restante)]

    ]

    info_table = Table(
        info_data,
        colWidths=[170, 300]
    )

    info_table.setStyle(TableStyle([

        ("GRID", (0,0), (-1,-1), 0.5, colors.black),

        ("BACKGROUND",
         (0,0),
         (0,-1),
         colors.HexColor("#0f172a")),

        ("TEXTCOLOR",
         (0,0),
         (0,-1),
         colors.white),

        ("FONTNAME",
         (0,0),
         (0,-1),
         "Helvetica-Bold"),

        ("BACKGROUND",
         (1,0),
         (1,-1),
         colors.whitesmoke)

    ]))

    elements.append(info_table)

    elements.append(
        Spacer(
            1,
            20
        )
    )

    # =====================================================
    # DECLARATIONS
    # =====================================================

    elements.append(
        Paragraph(
            "<b>DECLARATIONS LIEES</b>",
            styles["Heading2"]
        )
    )

    elements.append(
        Spacer(
            1,
            10
        )
    )

    declaration_data = [[
        "Article",
        "Quantité",
        "Prix Unitaire",
        "Valeur"
    ]]

    for d in declarations:

        declaration_data.append([

            str(d.article),

            str(d.quantite),

            str(d.prixUnitaire),

            str(d.valeur_totale)

        ])

    declaration_table = Table(
        declaration_data,
        colWidths=[180, 80, 100, 120]
    )

    declaration_table.setStyle(TableStyle([

        ("BACKGROUND",
         (0,0),
         (-1,0),
         colors.HexColor("#0f172a")),

        ("TEXTCOLOR",
         (0,0),
         (-1,0),
         colors.white),

        ("FONTNAME",
         (0,0),
         (-1,0),
         "Helvetica-Bold"),

        ("GRID",
         (0,0),
         (-1,-1),
         0.5,
         colors.black),

        ("BACKGROUND",
         (0,1),
         (-1,-1),
         colors.HexColor("#f8fafc"))

    ]))

    elements.append(declaration_table)

    elements.append(
        Spacer(
            1,
            30
        )
    )

    # =====================================================
    # FOOTER
    # =====================================================

    footer = Paragraph(
        """
        <para align="center">
        Document généré automatiquement par le système AV
        <br/>
        OFFICE CONGOLAIS DE CONTROLE (OCC)
        </para>
        """,
        styles["Italic"]
    )

    elements.append(footer)

    # =====================================================
    # GENERATION PDF
    # =====================================================

    doc.build(elements)

    return response