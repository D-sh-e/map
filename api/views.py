from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Point, Message
from .serializers import (
    PointSerializer, MessageSerializer, 
    PointSearchSerializer, UserRegistrationSerializer
)
from .utils import haversine_distance
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets, status, permissions, generics



class MapView(generics.GenericAPIView):
    """
    Отображение карты
    """
    def get(self, request):
        return render(request, 'map.html')


class PointApi(viewsets.ModelViewSet):
    """
    Работа с точками и сообщениями
    """
    queryset = Point.objects.all()
    serializer_class = PointSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        # Автоматически устанавливаем текущего пользователя как создателя точки
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Поиск точек в заданном радиусе
        GET /api/points/search/?latitude=1.1&longitude=1.1&radius=1
        """
        serializer = PointSearchSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        latitude = serializer.validated_data['latitude']
        longitude = serializer.validated_data['longitude']
        radius = serializer.validated_data['radius']
        

        all_points = Point.objects.all()
        
        # Фильтруем точки по расстоянию
        result_points = []
        for point in all_points:
            distance = haversine_distance(
                latitude, longitude,
                point.latitude, point.longitude
            )
            
            if distance <= radius:
                point_data = PointSerializer(point).data
                point_data['distance_km'] = round(distance, 2)
                result_points.append(point_data)
        
        return Response(result_points)
    
    @action(detail=False, methods=['get', 'post'], url_path='messages')
    def messages(self, request):
        """
        /api/points/messages/
        GET: Получить сообщения
        POST: Создать сообщение

        GET параметры:
        1. По радиусу: ?latitude=1.1&longitude=1.1&radius=1
        2. По конкретной точке: ?point_id=1
        """
        if request.method == 'GET':
            latitude = request.query_params.get('latitude')
            longitude = request.query_params.get('longitude')
            radius = request.query_params.get('radius')
            point_id = request.query_params.get('point_id')

            # Проверка параметров
            if (latitude or longitude or radius) and point_id:
                return Response(
                    {"error": "Укажите либо параметры радиуса (latitude, longitude, radius), либо point_id, но не оба сразу"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            
             # Поиск по конкретной точке
            if point_id:
                try:
                    point_id_int = int(point_id)
                    # Проверяем существование точки
                    point_exists = Point.objects.filter(id=point_id_int).exists()
                    if not point_exists:
                        return Response(
                            {"error": f"Точка с ID {point_id} не найдена"},
                            status=status.HTTP_404_NOT_FOUND
                        )
                    
                    # Получаем все сообщения для этой точки
                    messages = Message.objects.filter(point_id=point_id_int)
                    serializer = MessageSerializer(messages, many=True)
                    return Response(serializer.data)
                    
                except ValueError:
                    return Response(
                        {"error": "point_id должен быть числом"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Поиск по радиусу
            if latitude and longitude and radius:
                try:
                    lat = float(latitude)
                    lon = float(longitude)
                    rad = float(radius)
                    
                    # Проверка значений координат
                    if not (-90 <= lat <= 90):
                        return Response(
                            {"error": "Широта должна быть в диапазоне от -90 до 90"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    if not (-180 <= lon <= 180):
                        return Response(
                            {"error": "Долгота должна быть в диапазоне от -180 до 180"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    if rad <= 0:
                        return Response(
                            {"error": "Радиус должен быть больше 0"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    # Получаем все точки
                    all_points = Point.objects.all()
                    
                    # Находим подходящие точки
                    point_ids_in_radius = []
                    for point in all_points:
                        distance = haversine_distance(
                            lat, lon,
                            point.latitude, point.longitude
                        )
                        if distance <= rad:
                            point_ids_in_radius.append(point.id)
                    
                    # Получаем сообщения для точек в радиусе
                    messages = Message.objects.filter(point_id__in=point_ids_in_radius)
                    serializer = MessageSerializer(messages, many=True)

                    response_data = serializer.data
                    
                    return Response(response_data)
                    
                except (ValueError, TypeError) as e:
                    return Response(
                        {"error": f"Неверный формат параметров: {str(e)}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Если не указаны параметры для GET запроса
            return Response(
                {
                    "error": "Необходимо указать параметры поиска",
                    "примеры": {
                        "по_радиусу": "/api/points/messages/?latitude=1.1&longitude=1.1&radius=1",
                        "по_точке": "/api/points/messages/?point_id=1"
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        elif request.method == 'POST':
            # POST логика
            serializer = MessageSerializer(data=request.data, context={'request': request})
            
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Пользователь успешно создан"},
            status=status.HTTP_201_CREATED,
            headers=headers
        )
