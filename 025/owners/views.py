from django.db import models
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Building, House, Owner
from .serializers import BuildingSerializer, HouseSerializer, OwnerSerializer


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all().order_by('-create_time')
    serializer_class = BuildingSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__contains=name)
        return queryset


class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all().order_by('building', 'floor', 'room_number')
    serializer_class = HouseSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        building_id = self.request.query_params.get('building_id')
        room_number = self.request.query_params.get('room_number')
        status = self.request.query_params.get('status')

        if building_id:
            queryset = queryset.filter(building_id=building_id)
        if room_number:
            queryset = queryset.filter(room_number__contains=room_number)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    @action(detail=False, methods=['get'])
    def by_building(self, request):
        building_id = request.query_params.get('building_id')
        if building_id:
            houses = self.queryset.filter(building_id=building_id)
            serializer = self.get_serializer(houses, many=True)
            return Response(serializer.data)
        return Response({'error': 'building_id is required'}, status=status.HTTP_400_BAD_REQUEST)


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all().order_by('-create_time')
    serializer_class = OwnerSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        phone = self.request.query_params.get('phone')
        room_number = self.request.query_params.get('room_number')
        building_id = self.request.query_params.get('building_id')
        status = self.request.query_params.get('status')

        if name:
            queryset = queryset.filter(name__contains=name)
        if phone:
            queryset = queryset.filter(phone__contains=phone)
        if room_number:
            queryset = queryset.filter(house__room_number__contains=room_number)
        if building_id:
            queryset = queryset.filter(house__building_id=building_id)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    @action(detail=False, methods=['get'])
    def search(self, request):
        keyword = request.query_params.get('keyword', '')
        if keyword:
            owners = self.queryset.filter(
                models.Q(name__contains=keyword) |
                models.Q(phone__contains=keyword) |
                models.Q(house__room_number__contains=keyword)
            )
            page = self.paginate_queryset(owners)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(owners, many=True)
            return Response(serializer.data)
        return Response({'error': 'keyword is required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_house(self, request):
        house_id = request.query_params.get('house_id')
        if house_id:
            owners = self.queryset.filter(house_id=house_id)
            serializer = self.get_serializer(owners, many=True)
            return Response(serializer.data)
        return Response({'error': 'house_id is required'}, status=status.HTTP_400_BAD_REQUEST)
