class CSSSelectorBuilder:

    _selector = str()

    def id(self, _id):
        self._selector += f" #{_id}"
        return self

    def withId(self, withId):
        self._selector += f"#{withId}"
        return self

    def tag(self, tag):
        self._selector += f" {tag}"
        return self

    def clazz(self, clazz):
        self._selector += f" .{clazz}"
        return self

    def attribute(self, name, value):
        self._selector += f" [{name}='{value}']"
        return self

    def withAttribute(self, name, value):
        self._selector += f"[{name}='{value}']"
        return self

    def text(self, text):
        self._selector += f" [text='{text}']"
        return self

    def withText(self, text):
        self._selector += f"[text='{text}']"
        return self

    def build(self):
        return self._selector
