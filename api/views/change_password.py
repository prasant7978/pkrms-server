
from django.contrib.auth import authenticate
from api.serializers.PasswordChangeSerializer import PasswordChangeSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user  # Get the currently logged-in user
    serializer = PasswordChangeSerializer(data=request.data)
    
    if serializer.is_valid():
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        
        # Check if the old password is correct
        if not user.check_password(old_password):
            return Response({'detail': 'Old password is incorrect'}, status=400)
        
        # Change the password to the new one
        user.password = make_password(new_password)  # Hash the new password
        user.save()

        return Response({'detail': 'Password changed successfully.'}, status=200)
    
    return Response(serializer.errors, status=400)