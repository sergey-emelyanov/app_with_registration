def validate(user):
    errors = {}
    if not user['name']:
        errors['name'] = 'Form cant be empty'
    if not user['email']:
        errors['email'] = 'Form cant be empty'
    return errors
