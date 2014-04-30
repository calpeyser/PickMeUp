import autocomplete_light

from create_account.models import User


class UserAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['netid']
autocomplete_light.register(User, UserAutocomplete)
