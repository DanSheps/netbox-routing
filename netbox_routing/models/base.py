class SearchAttributeMixin:

    @property
    def search_display_name(self) -> str:
        return self.__str__()
