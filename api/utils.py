# utils.py
from rest_framework.response import Response
from rest_framework import status

def validate_integer(value, field_name="value"):
    """
    Validates that the given value can be converted to an integer.
    Returns either the integer value or a Response with an error message.
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return Response(
            {f'error': f"The '{field_name}' field should be a valid integer."},
            status=status.HTTP_400_BAD_REQUEST
        )