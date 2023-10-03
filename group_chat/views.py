
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Group,GroupMessage
from .serializers import GroupSerializer,GroupMessageSerializer
from django.contrib.auth.models import User
from admin_module.serializers import UserSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_group(request):
    request.data['creator']=request.user.id
    serializer = GroupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_groups(request):
    groups = Group.objects.filter(is_active=True)
    serializer = GroupSerializer(groups, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_group(request, group_id):
    try:
        group = Group.objects.get(pk=group_id)
    except Group.DoesNotExist:
        return Response({'message': 'Group does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.user == group.creator:
        group.is_active=False
        group.save()
        return Response({'message': 'Group deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    






@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_group(request, group_id):
    try:
        group = Group.objects.get(pk=group_id,is_active=True)
    except Group.DoesNotExist:
        return Response({'message': 'Group does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.user == group.creator:
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    

# admin_module/views.py

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_group_details(request, group_id):
    try:
        group = Group.objects.get(pk=group_id,is_active=True)
    except Group.DoesNotExist:
        return Response({'message': 'Group does not exist'}, status=status.HTTP_404_NOT_FOUND)

    serializer = GroupSerializer(group)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_group_messages(request, group_id):
    try:
        group = Group.objects.get(pk=group_id,is_active=True)
    except Group.DoesNotExist:
        return Response({'message': 'Group does not exist'}, status=status.HTTP_404_NOT_FOUND)

    messages = GroupMessage.objects.filter(group=group)
    serializer = GroupMessageSerializer(messages, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_unlike_message(request, message_id):
    try:
        message = GroupMessage.objects.get(pk=message_id)
    except GroupMessage.DoesNotExist:
        return Response({'message': 'Message does not exist'}, status=status.HTTP_404_NOT_FOUND)

    user = request.user

    if user in message.likes.all():
        message.likes.remove(user)
        return Response({'message': 'Message unliked'}, status=status.HTTP_200_OK)
    else:
        message.likes.add(user)
        return Response({'message': 'Message liked'}, status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message_to_group(request, group_id):
    try:
        group = Group.objects.get(id=group_id, is_active=True)
    except Group.DoesNotExist:
        return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the user is a member of the group
    if request.user not in group.group_members.all():
        return Response({'error': 'User is not a member of the group'}, status=status.HTTP_403_FORBIDDEN)

    # Create a new message
    message_text = request.data.get('text', '')
    message = GroupMessage(group=group, sender=request.user, text=message_text)
    message.save()

    # Serialize and return the created message
    serializer = GroupMessageSerializer(message)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_member_to_group(request, group_id):
    try:
        group = Group.objects.get(id=group_id, is_active=True)
    except Group.DoesNotExist:
        return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if  user  is an admin or creator of the group
    if request.user != group.creator and not request.user.is_staff :
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    # Get the user_id to be added from the payload
    user_id_to_add = request.data.get('user_id')

    # Check is user  exists
    try:
        user_to_add = User.objects.get(id=user_id_to_add)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if the user is already a member of the group
    if user_to_add in group.group_members.all():
        return Response({'error': 'User is already a member of the group'}, status=status.HTTP_400_BAD_REQUEST)

    # Add the user to the group 
    group.group_members.add(user_to_add)
    group.save()

    return Response({'message': 'User added to the group successfully'}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_member_from_group(request, group_id):
    try:
        group = Group.objects.get(id=group_id, is_active=True)
    except Group.DoesNotExist:
        return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check admin or creator of the group
    if request.user != group.creator and not request.user.is_staff:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    # Get the user_id to be removed from the payload
    user_id_to_remove = request.data.get('user_id')

    # Check is user is exists
    try:
        user_to_remove = User.objects.get(id=user_id_to_remove)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check the user is a member of the group
    if user_to_remove not in group.group_members.all():
        return Response({'error': 'User is not a member of the group'}, status=status.HTTP_400_BAD_REQUEST)

    # Remove the user from the group
    group.group_members.remove(user_to_remove)
    group.save()

    return Response({'message': 'User removed from the group successfully'}, status=status.HTTP_204_NO_CONTENT)
