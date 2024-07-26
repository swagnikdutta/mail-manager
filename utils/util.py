def translate_field_to_header(field):
    d = {
        'from': 'sender',
        'to': 'receiver',
        'subject': 'subject',
        'datetime': 'datetime'
    }
    return d[field]