import pytomlpp

from ansible.module_utils._text import to_text


def to_toml(a):
    return to_text(pytomlpp.dumps(a), errors='surrogate_or_strict')


def from_toml(a):
    return pytomlpp.loads(to_text(a, errors='surrogate_or_strict'))


class FilterModule:
    """ TOML filters """

    def filters(self):
        return {
            'to_toml':   to_toml,
            'from_toml': from_toml,
        }
