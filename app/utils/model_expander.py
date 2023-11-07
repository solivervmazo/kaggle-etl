def expand_dict(self, value, rel) -> dict:
    if rel:
        for key_as_attr in rel:
            if hasattr(self, key_as_attr):
                next_rel = rel.get(key_as_attr)
                if next_rel is True:
                    if isinstance(self.__dict__[key_as_attr], list):
                        value[key_as_attr] = [
                            d.to_dict() for d in self.__dict__[key_as_attr]
                        ]
                    else:
                        value[key_as_attr] = self.__dict__[key_as_attr].to_dict()
                else:
                    if "." in next_rel:
                        # if value has . (classModel.model_attr) then
                        # instead of giving the dict, we will just
                        # the value of model_attr to self.attr and cut the cycle
                        # Note: the model_attr provided should not be a dict or Model
                        pulled_dict = self.__dict__[key_as_attr].to_dict()
                        attr = next_rel.split(".")[1]
                        value[key_as_attr] = pulled_dict.get(attr, None)
                    else:
                        if isinstance(self.__dict__[key_as_attr], list):
                            value[key_as_attr] = [
                                d.to_dict() for d in self.__dict__[key_as_attr]
                            ]
                        else:
                            value[key_as_attr] = self.__dict__[key_as_attr].to_dict(
                                rel=next_rel
                            )
    return value
