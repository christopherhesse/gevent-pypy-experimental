import weakref

class Lookupable(object):
    """
    Allows the class to be used to find instances using a key set by
    the child class in the "_get_key" method.

    Subclasses must call self._register_instance() when _get_key()
    is ready to be called to register the class instance.
    """
    def _register_instance(self):
        cls = self.__class__
        if not hasattr(cls, '_instance_lookup_table'):
            cls._instance_lookup_table = weakref.WeakValueDictionary()
        cls._instance_lookup_table[self._get_key()] = self

    def _unregister_instance(self):
        # this should not be necessary normally, since the entry in the lookup table
        # will automatically be deleted when there are no other references to the instance
        cls = self.__class__
        if hasattr(cls, '_instance_lookup_table'):
            key = self._get_key()
            if key in cls._instance_lookup_table:
                del cls._instance_lookup_table[key]

    def _get_key(self):
        raise NotImplementedError("child classes should provide this method")

    @classmethod
    def lookup_instance(cls, key):
        if hasattr(cls, '_instance_lookup_table'):
            return cls._instance_lookup_table.get(key, None)
        else:
            return None
