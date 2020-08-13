class Keycode:
    # common keycodes
    # TODO extend this keycode list
    BACKSPACE = 8
    CAPS_LOCK = 20
    CONTROL = 17
    DELETE = 46
    END = 35
    ESCAPE = 27

    @staticmethod
    def function(num):
        """
        Returns the keycode for function keys
        :param num:
        :return:
        """
        if num > 12 or num < 1:
            raise ValueError("Function keys should be between 1 and 12 inclusive")
        return 111 + num


class ShortcutDispatch(object):
    """
    Utility class to help create keyboard layout independent
    shortcut bindings.
    """
    # state mask values
    CONTROL = 0x004
    SHIFT = 0x0001
    ALT = 0x20000
    MASKS = (CONTROL, SHIFT, ALT)
    _windows = {}

    def __init__(self, window):
        self._bindings = {}
        self.window = window

    def bind(self):
        """
        Use bind method of the window attribute to set up dispatch
        :return: None
        """
        self.window.bind('<Key>', self._dispatch)
        # Alt key is kinda buggy and needs to be bound separately
        self.window.bind('<Alt-Key>', self._dispatch)

    def bind_all(self):
        """
        Use bind all method of the window attribute to set up global dispatch, similar
        to using bind_all directly
        :return: None
        """
        self.window.bind_all('<Key>', self._dispatch)
        self.window.bind_all('<Alt-Key>', self._dispatch)

    def add(self, func, key_code, *masks):
        """
        Bind a method to window using the dispatch system.
        :param func: A function/method accepting one argument, event
        :param key_code: the tk keycode corresponding to the physical key
            1. use ord function to obtain keycode for alphanumeric values for instance
            ord('X') for physical 'X' key Note: it is advisable to use the uppercase variant of a letter
            2. use Keycode class for common physical keys like Keycode.DELETE, Keycode.ESCAPE
            3. use Keycode.function for function keys like Keycode.function(3) for F3
            4. an integer value determined empirically from event.keycode property of any key
        :param masks: Modifiers either CONTROL, ALT, SHIFT defined in ShortcutDispatch
        :return: None
        """
        # for the sake of consistency ensure masks are sorted in the modifier
        # this makes it easy to compare it to modifiers generated from event state
        modifier = (key_code, ) + tuple(sorted(masks))
        self._bindings[modifier] = func

    def get_modifier(self, event):
        """
        Return a tuple representing (keycode, ...masks) where masks are sorted
        :param event: the event from which to derive the mask values
        :return: tuple (keycode, ...masks)
        """
        modifier = ()
        for mask in self.MASKS:
            if event.state & mask:
                modifier += (mask, )
        modifier = (event.keycode, ) + tuple(sorted(modifier))
        return modifier

    def _dispatch(self, event):
        # obtain the modifier form from the event
        modifier = self.get_modifier(event)
        # keycode is always the first item and masks ar sorted so the
        # modifier can be matched to a similar one in the bindings dictionary
        if modifier in self._bindings:
            # run the bound callback and pass event as argument
            self._bindings[modifier](event)

    @classmethod
    def acquire(cls, window):
        """
        Factory method for creating Dispatch systems. Ensures only
        one dispatch exists for any given window. Avoid initializing
        ShortcutDispatch directly.
        :param window:
        :return:
        """
        if window not in cls._windows:
            cls._windows[window] = cls(window)
        return cls._windows[window]
