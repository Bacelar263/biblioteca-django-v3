from django.urls import path
from core import views
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('livros/', views.LivroList.as_view(), name='livros-list'),
    path('livros/<int:pk>/', views.LivroDetail.as_view(), name='livrodetail'),

    path('categorias/', views.CategoriaList.as_view(), name='categorias-list'),
    path('categorias/<int:pk>/', views.CategoriaDetail.as_view(), name='categoriasdetail'),

    path('autores/', views.AutorList.as_view(), name='autores-list'),
    path('autores/<int:pk>/', views.AutorDetail.as_view(), name='autoresdetail'),

    # Rotas para Colecoes
    path('colecoes/', views.ColecaoListCreate.as_view(), name='colecao-list-create'),
    path('colecoes/<int:pk>/', views.ColecaoDetail.as_view(), name='colecao-detail'),

    # Endpoint para obtenção de Token de Autenticação
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # Endpoints para documentação da API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
