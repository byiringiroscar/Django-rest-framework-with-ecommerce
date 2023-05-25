from django.shortcuts import render, HttpResponse
from api_commerce.models import Note
from api_commerce.serializer import NoteSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User


# Create your views here.

def home(request):
    return HttpResponse('<h1>Hello world</h1>')


@permission_classes((IsAuthenticated,))
@api_view(['GET', ])
def view_note(request):
    all_note = Note.objects.all()
    serializer = NoteSerializer(all_note, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def specified_note(request, slug):
    try:
        note = Note.objects.get(note_name=slug)
    except Note.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = NoteSerializer(note)
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
@api_view(['PUT', ])
def specified_note_edit(request, slug):
    try:
        note = Note.objects.get(note_name=slug)
    except Note.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user = request.user
    if note.note_user != user:
        return Response({"response": "you don't have permission to edit that"})
    if request.method == 'PUT':
        serializer = NoteSerializer(note, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = "update successfully"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
@api_view(['DELETE', ])
def specified_note_delete(request, slug):
    try:
        note = Note.objects.get(note_name=slug)
    except Note.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user = request.user
    if note.note_user != user:
        return Response({"response": "you don't have permission to delete that"})
    if request.method == 'DELETE':
        operation = note.delete()
        data = {}
        if operation:
            data['success'] = "delete successfully"
        else:
            data["failure"] = "delete failed"
        return Response(data=data)


@permission_classes((IsAuthenticated,))
@api_view(['POST', ])
def specified_note_create(request):
    account = request.user
    note_create = Note(note_user=account)
    if request.method == 'POST':
        serializer = NoteSerializer(note_create, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST', ])
# def specified_note_create(request):
#     user_specify = User.objects.get(id=1)
#     note_create = Note(note_user=user_specify)
#     if request.method == 'POST':
#         serializer = NoteSerializer(note_create, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
