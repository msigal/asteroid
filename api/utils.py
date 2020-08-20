import functools

from rest_framework import status, serializers
from rest_framework.fields import to_choices_dict, flatten_choices_dict
from rest_framework.response import Response

from core.core_functions import check_if_asteroid_exists


def check_asteroid_exists(func):
    @functools.wraps(func)
    def wrapper(self, request, name: str, *args, **kwargs):
        if not check_if_asteroid_exists(name=name):
            return Response(
                f'Asteroid with name {name} not found.',
                status=status.HTTP_404_NOT_FOUND
            )

        return func(self, request, name, *args, **kwargs)

    return wrapper


class LazyChoiceField(serializers.ChoiceField):
    _use_context_for_choices = False

    def __init__(self, choices, **kwargs):
        self._choices_source = None
        self._choices_loaded = False
        self.grouped_choices = None
        self._choices = None
        self.choice_strings_to_values = None
        super().__init__(choices, **kwargs)

    def _set_choices(self, choices):
        self._choices_source = choices

    def _load_choices(self):
        if self._choices_loaded:
            return

        choices = self._choices_source
        if callable(self._choices_source):
            if self._use_context_for_choices:
                choices = self._choices_source(**self.context)
            else:
                choices = self._choices_source()

        # Copy Past from ChoiceField._set_choices.
        # Can not call ChoiceField._set_choices (choices) because it calls self.choices, which leads to recursion
        self.grouped_choices = to_choices_dict(choices)
        self._choices = flatten_choices_dict(self.grouped_choices)
        self.choice_strings_to_values = {
            str(key): key for key in self._choices
        }

        self._choices_loaded = True

    def _get_choices(self):
        self._load_choices()
        return super()._get_choices()

    def iter_options(self):
        self._load_choices()
        return super().iter_options()

    def to_internal_value(self, data):
        self._load_choices()
        return super().to_internal_value(data)

    def to_representation(self, value):
        self._load_choices()
        return super().to_representation(value)

    choices = property(_get_choices, _set_choices)


class LazyMultipleChoiceField(serializers.MultipleChoiceField, LazyChoiceField):
    pass
