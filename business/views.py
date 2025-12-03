from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authorization.permissions import require_permission, get_user_permissions


MOCK_PRODUCTS = [
    {'id': 1, 'name': 'Ноутбук', 'price': 50000, 'owner_id': 1},
    {'id': 2, 'name': 'Смартфон', 'price': 30000, 'owner_id': 2},
    {'id': 3, 'name': 'Планшет', 'price': 25000, 'owner_id': 1},
    {'id': 4, 'name': 'Наушники', 'price': 5000, 'owner_id': 3},
]

MOCK_SHOPS = [
    {'id': 1, 'name': 'Магазин Электроники', 'address': 'ул. Ленина, 1', 'owner_id': 1},
    {'id': 2, 'name': 'Техно Мир', 'address': 'пр. Мира, 25', 'owner_id': 2},
    {'id': 3, 'name': 'Гаджет Хаус', 'address': 'ул. Пушкина, 10', 'owner_id': 1},
]

MOCK_ORDERS = [
    {'id': 1, 'product_id': 1, 'quantity': 2, 'total': 100000, 'owner_id': 2},
    {'id': 2, 'product_id': 2, 'quantity': 1, 'total': 30000, 'owner_id': 3},
    {'id': 3, 'product_id': 4, 'quantity': 3, 'total': 15000, 'owner_id': 1},
]


class ProductListView(APIView):
    def get(self, request):
        if not request.current_user:
            return Response({'error': 'Не авторизован'}, status=status.HTTP_401_UNAUTHORIZED)

        permissions = get_user_permissions(request.current_user, 'products')
        if permissions.get('read_all'):
            return Response({'products': MOCK_PRODUCTS, 'access_level': 'full'})
        elif permissions.get('read'):
            user_products = [p for p in MOCK_PRODUCTS if p['owner_id'] == request.current_user.id]
            return Response({'products': user_products, 'access_level': 'own_only'})
        return Response({'error': 'Доступ запрещен'}, status=status.HTTP_403_FORBIDDEN)

    @require_permission('products', 'create')
    def post(self, request):
        new_product = {
            'id': len(MOCK_PRODUCTS) + 1,
            'name': request.data.get('name', 'Новый товар'),
            'price': request.data.get('price', 0),
            'owner_id': request.current_user.id
        }
        return Response({'message': 'Товар создан (mock)', 'product': new_product}, status=status.HTTP_201_CREATED)


class ShopListView(APIView):
    def get(self, request):
        if not request.current_user:
            return Response({'error': 'Не авторизован'}, status=status.HTTP_401_UNAUTHORIZED)

        permissions = get_user_permissions(request.current_user, 'shops')
        if permissions.get('read_all'):
            return Response({'shops': MOCK_SHOPS, 'access_level': 'full'})
        elif permissions.get('read'):
            user_shops = [s for s in MOCK_SHOPS if s['owner_id'] == request.current_user.id]
            return Response({'shops': user_shops, 'access_level': 'own_only'})
        return Response({'error': 'Доступ запрещен'}, status=status.HTTP_403_FORBIDDEN)

    @require_permission('shops', 'create')
    def post(self, request):
        new_shop = {
            'id': len(MOCK_SHOPS) + 1,
            'name': request.data.get('name', 'Новый магазин'),
            'address': request.data.get('address', ''),
            'owner_id': request.current_user.id
        }
        return Response({'message': 'Магазин создан (mock)', 'shop': new_shop}, status=status.HTTP_201_CREATED)


class OrderListView(APIView):
    def get(self, request):
        if not request.current_user:
            return Response({'error': 'Не авторизован'}, status=status.HTTP_401_UNAUTHORIZED)

        permissions = get_user_permissions(request.current_user, 'orders')
        if permissions.get('read_all'):
            return Response({'orders': MOCK_ORDERS, 'access_level': 'full'})
        elif permissions.get('read'):
            user_orders = [o for o in MOCK_ORDERS if o['owner_id'] == request.current_user.id]
            return Response({'orders': user_orders, 'access_level': 'own_only'})
        return Response({'error': 'Доступ запрещен'}, status=status.HTTP_403_FORBIDDEN)

    @require_permission('orders', 'create')
    def post(self, request):
        new_order = {
            'id': len(MOCK_ORDERS) + 1,
            'product_id': request.data.get('product_id', 1),
            'quantity': request.data.get('quantity', 1),
            'total': request.data.get('total', 0),
            'owner_id': request.current_user.id
        }
        return Response({'message': 'Заказ создан (mock)', 'order': new_order}, status=status.HTTP_201_CREATED)
