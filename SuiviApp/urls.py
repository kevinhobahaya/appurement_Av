from django.contrib import admin
from django.urls import path, include
from SuiviApp import views
from SuiviApp.views import *

app_name='SuiviApp'
urlpatterns = [


    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    path("users/", user_list, name="user_list"),
    path("users/add/", user_create, name="user_create"),
    path("users/<uuid:uuid>/edit/", user_update, name="user_update"),
    path("users/<uuid:uuid>/delete/", user_delete, name="user_delete"),
    path('home',erp_dashboard, name='home'),
    path(
    "parametres/",
    views.parametres,
    name="parametres"
    ),
   
    path('importateur/<uuid:uuid>/', importateur_detail, name='importateur_detail'),
    path(
    "importateur/",
    importateurs_list,
    name="importateur"
),

path(
    "importateur/create/",
    importateur_create,
    name="importateur_create"
),

path(
    "importateur/update/<uuid:uuid>/",
    importateur_update,
    name="importateur_update"
),

path(
    "importateur/delete/<uuid:uuid>/",
    importateur_delete,
    name="importateur_delete"
),
path(
    "declaration/",
    declaration_list,
    name="declaration"
),

path(
    "declaration/create/",
    declaration_create,
    name="declaration_create"
),

path(
    "declaration/update/<uuid:uuid>/",
    declaration_update,
    name="declaration_update"
),

path(
    "declaration/delete/<uuid:uuid>/",
    declaration_delete,
    name="declaration_delete"
),

path(
    "declaration/<uuid:uuid>/",
    declaration_detail,
    name="declaration_detail"
),


#  ====  AV URLS ====

path(
    "av/",
    av_list,
    name="av_list"
),

path(
    "av/create/",
    av_create,
    name="av_create"
),

path(
    "av/update/<uuid:uuid>/",
    av_update,
    name="av_update"
),

path(
    "av/delete/<uuid:uuid>/",
    av_delete,
    name="av_delete"
),

path(
    "av/<uuid:uuid>/",
    av_detail,
    name="av_detail"

),
# path("av/produits/create/", av_produit_list, name="av_produit_list"),

path("declaration/<uuid:uuid>/", declaration_detail, name="declaration_detail"),
path("produits/", av_produit_list, name="av_produit_list"),
# path("av/<int:av_id>/produit/add/", av_produit_create, name="av_produit_create"),

# path("produit/<uuid:uuid>/edit/", av_produit_update, name="av_produit_update"),
path("produit/<uuid:uuid>/delete/", av_produit_delete, name="av_produit_delete"),
path("declarations/", declaration_list, name="declaration_list"),
    path(
        "produits/",
       av_produit_list,
        name="av_produit_list"
    ),

    path(
        "produits/create/",
       av_produit_create,
        name="av_produit_create"
    ),

    path(
        "produits/<uuid:uuid>/detail/",
       av_produit_detail,
        name="av_produit_detail"
    ),

    path(
        "produits/<uuid:uuid>/update/",
       av_produit_update,
        name="av_produit_update"
    ),

    path(
        "produits/<uuid:uuid>/delete/",
       av_produit_delete,
        name="av_produit_delete"
    ),
    path("register/", register_user, name="register"),

    path('users/', user_list, name='user_list'),
    path('users/create/', user_create, name='user_create'),
    path('users/update/<uuid:uuid>/', user_update, name='user_update'),
    path('users/delete/<uuid:uuid>/', user_delete, name='user_delete'),
    path('users/toggle/<uuid:uuid>/', toggle_user_status, name='toggle_user'),
    path("importateur/<uuid:uuid>/export/excel/", views.export_excel_importateur, name="export_excel_importateur"),
    path("importateur/<uuid:uuid>/export/pdf/", views.export_pdf_importateur, name="export_pdf_importateur"),
   
    path('appurement/pdf/<uuid:uuid>/', av_pdf, name='appurement_av_pdf'),
    path(
    "av-produit/<uuid:uuid>/detail/",
    views.av_produit_detail,
    name="av_produit_detail"
    ),
    path(
    "av-produit/<uuid:uuid>/pdf/",
    views.av_produit_pdf,
    name="av_produit_pdf"
    ),
    ]