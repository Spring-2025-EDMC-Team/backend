from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator,
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator,
    validate_password
)
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(["POST"])
def validate_password_strength(request):
    """
    API endpoint to validate password strength without creating a user.
    
    Request body should contain:
    {
        "password": "the_password_to_validate",
        "username": "optional_username_for_similarity_check"
    }
    """
    password = request.data.get("password", "")
    username = request.data.get("username", "")
    
    # Create a user-like object for the similarity validator
    user_props = {}
    if username:
        user_props['username'] = username
    
    try:
        # Run the password through Django's validation
        validate_password(password, user_props)
        
        # If we get here, the password passed all validations
        return Response({
            "valid": True,
            "message": "Password meets all requirements"
        }, status=status.HTTP_200_OK)
        
    except ValidationError as e:
        # Return the validation errors
        return Response({
            "valid": False,
            "errors": e.messages
        }, status=status.HTTP_400_BAD_REQUEST)
