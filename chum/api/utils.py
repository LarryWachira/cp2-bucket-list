from flask import jsonify


def error_response(validation_errors=None,
                   message='Please correct the errors',
                   status=400,
                   error='Bad request'):

    if validation_errors:
        response = jsonify(
            {'status': status, 'error': error,
             'error(s)': validation_errors,
             'message': message}
        )

    else:
        response = jsonify(
            {'status': status, 'error': error,
             'message': message}
        )

    response.status_code = status
    return response


def success_response(message, status=200):
    response = jsonify(
        {'status': status,
         'message': message}
    )
    response.status_code = status
    return response
