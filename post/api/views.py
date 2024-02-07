from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from account.models import Account
from post.models import BlogPost
from post.api.serializers import BlogPostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_get_view(request, slug):
    try:
        blog_post = BlogPost.objects.get(slug=slug)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BlogPostSerializer(blog_post)
        return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def api_update_view(request, slug):
    try:
        blog_post = BlogPost.objects.get(slug=slug)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if blog_post.author != user:
        return Response({'response': "You don't have permission"})

    if request.method == 'PUT':
        serializer = BlogPostSerializer(blog_post, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = 'update successful'
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_view(request, slug):
    try:
        blog_post = BlogPost.objects.get(slug=slug)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if blog_post.author != user:
        return Response({'response': "You don't have permission"})

    if request.method == 'DELETE':
        operation = blog_post.delete()
        data = {}
        if operation:
            data['success'] = 'delete successful'
        else:
            data['failure'] = 'delete failed'
        return Response(data=data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_create_view(request):
    account = request.user
    blog_post = BlogPost(author=account)
    if request.method == 'POST':
        serializer = BlogPostSerializer(blog_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiBlogView(ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    authentication_classes = TokenAuthentication,
    permission_classes = IsAuthenticated,
    pagination_class = PageNumberPagination
    filter_backends = SearchFilter, OrderingFilter
    search_fields = ('title', 'body', 'author__username')
