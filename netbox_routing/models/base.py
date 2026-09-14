class SearchAttributeMixin:

    @property
    def search_display_name(self) -> str:
        return str(self)
