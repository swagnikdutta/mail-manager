def translate_field_to_header(field):
    d = {
        'from': 'sender',
        'to': 'receiver',
        'subject': 'subject',
    }
    return d.get(field, None)