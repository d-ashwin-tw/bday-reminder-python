from rest_framework.response import Response


def response_data(status, message, data=dict(), errors=dict()):
    try:
        if status != 200:
            if isinstance(errors, str):
                errors = {
                    'non_field_errors': [str(errors)]
                }
            if isinstance(errors, list):
                errors = {
                    'non_field_errors': [(errors[0])]
                }
            if errors is None or isinstance(errors, dict) and len(errors) == 0:
                errors = {
                    'non_field_errors': [str(message)]
                }
        return Response({'status_code': status, 'message': message, 'data': data, 'errors': errors}, status=status)
    except Exception as e:
        return Response({'status_code': status, 'message': message, 'data': data, 'errors': errors,}, status=status)