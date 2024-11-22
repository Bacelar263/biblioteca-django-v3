from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from core.models import Colecao, Livro

class ColecaoTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.livro = Livro.objects.create(titulo='Livro Teste', autor_id=1, categoria_id=1, publicado_em='2023-01-01')

    def test_create_colecao(self):
        data = {'nome': 'Minha Coleção', 'descricao': 'Descrição da Coleção', 'livros': [self.livro.id]}
        response = self.client.post('/colecoes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Colecao.objects.count(), 1)
        self.assertEqual(Colecao.objects.get().nome, 'Minha Coleção')

    def test_edit_colecao(self):
        colecao = Colecao.objects.create(nome='Coleção Original', colecionador=self.user)
        data = {'nome': 'Coleção Editada', 'descricao': 'Descrição Editada', 'livros': [self.livro.id]}
        response = self.client.put(f'/colecoes/{colecao.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Colecao.objects.get().nome, 'Coleção Editada')

    def test_delete_colecao(self):
        colecao = Colecao.objects.create(nome='Coleção para Deletar', colecionador=self.user)
        response = self.client.delete(f'/colecoes/{colecao.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Colecao.objects.count(), 0)

    def test_list_colecoes(self):
        Colecao.objects.create(nome='Coleção 1', colecionador=self.user)
        Colecao.objects.create(nome='Coleção 2', colecionador=self.user)
        response = self.client.get('/colecoes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_permissions(self):
        user2 = User.objects.create_user(username='user2', password='pass2')
        colecao = Colecao.objects.create(nome='Coleção do User1', colecionador=self.user)
        self.client.force_authenticate(user=user2)
        data = {'nome': 'Tentativa de Edição', 'descricao': 'Descrição Tentativa', 'livros': [self.livro.id]}
        response = self.client.put(f'/colecoes/{colecao.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
