class _ConfigUIComponent(object):
    """Used as superclass for ConfigUI parts"""
    def __init__(self):
        """Empty constuctor"""
        pass

    def clear(self, entry):
        """Clear the given tk.Entry"""
        for c in entry.get():
            entry.delete(0)

    def set(self, entry, value):
        """Set the given tk.Entry to the given value"""
        self.clear(entry)
        for i, c in enumerate(str(value)):
            entry.insert(i, c)

    def get_value(self):
        """Method to override"""
        pass

    def set_default(self):
        """Method to override"""
        pass
