"""
Todos application views.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from rest_framework import status
from todo_app.serializers import TodoSerializer, UserSerializer, AuthTokenSerializer
from todo_app.models import Todo
from todo_app import auth_token


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for account."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class LogoutUserAPIView(APIView):
    """Logout account."""

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)


class CreateUserAPIView(APIView):
    """Account creation."""

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()

            data['response'] = "Successfully registrated"
            data['name'] = user.name
            data['email'] = user.email

            token = Token.objects.get(user=user).key
            data['token'] = token
        else:
            data = serializer.errors

        return Response(data)


class TodoListAPIView(APIView):
    """Todo list and todo creation APIs."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        todos = Todo.objects.filter(user=user)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDetailAPIView(APIView):
    """Todo Deail/Put/Patch/Delete APIs."""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response({'error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    def put(self, request, pk):
        todo = Todo.objects.get(pk=pk)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        todo = Todo.objects.get(pk=pk)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        todo = Todo.objects.get(pk=pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
