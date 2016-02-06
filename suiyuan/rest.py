from django.http import Http404
from .model import Passage
from rest_framework import routers, serializers, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins,generics
import math


class SixResultPagination(PageNumberPagination):
	page_size = 6
	page_size_query_param = "page"
	max_page_size = 6


class PassageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Passage
		fields = ('pub_date', 'pass_title', 'pass_summery', 'img_url', 'pass_url')


class PassageDetail(APIView):

	def get_object(self, py):
		try:
			queryset = Passage.objects.all()
			if py != "all":
				return queryset.filter(pass_type=py)
			return queryset
		except Passage.DoesNotExist:
			raise Http404

	def get(self, request, py, format=None):
		passage = self.get_object(py)

		if request.method == "GET" and 'max_page' in request.GET:
			return Response(math.ceil(passage.count()/6))

		serializers = PassageSerializer(passage, many=True)
		paginator = SixResultPagination()
		paginator.paginate_queryset(passage, request)
		return paginator.get_paginated_response(serializers.data)
