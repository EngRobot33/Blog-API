from django.core.exceptions import ValidationError

import re


def validator_numbers(password):
    regex = re.compile("[0-9]")
    if regex.search(password) is None:
        raise ValidationError('Password must include numbers!')


def validator_letters(password):
    regex = re.compile("[a-zA-Z]")
    if regex.search(password) is None:
        raise ValidationError('Password must include letters!')


def validator_special_chars(password):
    regex = re.compile("[@_!#$%^&*()<>?/\|}{~:]")
    if regex.search(password) is None:
        raise ValidationError('Password must include special characters!')


def validator_length(password):
    if len(password < 10):
        raise ValidationError(f'Password length must be 10 or more, not {len(password)}!')
