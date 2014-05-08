import autocomplete_light

from create_account.models import User


class UserAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['netid', 'first_name', 'last_name']
autocomplete_light.register(User, UserAutocomplete)
