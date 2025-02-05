from rest_framework import serializers

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        # Validate if new_password and confirm_new_password match
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError("New password and confirm password do not match.")
        return attrs
