from django.utils.translation import gettext_lazy as _

from netbox.ui import attrs, panels

__all__ = ('SettingsChoicePanel',)


class SettingsChoicePanel(panels.ObjectPanel):
    template_name = 'ui/panels/object_attributes.html'

    def __init__(self, choices, accessor='settings', **kwargs):
        super().__init__(**kwargs)
        self._accessor = accessor
        self._attrs = {}
        self._choices = choices

        for choice, label in self._choices.CHOICES:
            choice_type = self._choices.FIELD_TYPES[choice]
            if choice_type in ['ipaddr', 'string']:
                self._attrs[choice] = attrs.TextAttr('value', label=_(label))
            elif choice_type in [
                'integer',
            ]:
                self._attrs[choice] = attrs.NumericAttr('value', label=_(label))
            elif choice_type in [
                'boolean',
            ]:
                self._attrs[choice] = attrs.BooleanAttr('value', label=_(label))

    def get_context(self, context):
        ctx = super().get_context(context)
        settings = {
            setting.key: setting
            for setting in getattr(ctx['object'], self._accessor).all()
        }

        attr_names = set(settings.keys())
        return {
            **ctx,
            'attrs': [
                {
                    'label': attr.label,
                    'value': attr.render(
                        settings.get(name), {'name': name, 'perms': ctx['perms']}
                    ),
                }
                for name, attr in self._attrs.items()
                if name in attr_names
            ],
        }
