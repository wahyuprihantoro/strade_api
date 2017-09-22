def success_context(**kwargs):
    context = {
        'status': True,
        'message': "OK",
        **kwargs
    }
    return context


def fail_context(message=None, **kwargs):
    context = {
        'status': False,
        'message': message,
        **kwargs
    }
    return context


def fatal_context():
    context = {
        'status': False,
        'message': 'terjadi kesalahan pada server'
    }
    return context
