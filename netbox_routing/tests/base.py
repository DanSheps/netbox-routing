from netaddr.ip import IPAddress


class IPAddressFieldMixin:
    def model_to_dict(self, instance, fields, api=False):
        model_dict = super().model_to_dict(instance, fields, api)
        for key, value in list(model_dict.items()):
            if api:
                if type(value) is IPAddress:
                    model_dict[key] = str(value)
            elif not api and key in [
                'router_id',
            ]:
                if type(value) is IPAddress:
                    model_dict[key] = str(value)
        return model_dict
