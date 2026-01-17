class MantlememoError(Exception):
    pass


class AuthenticationError(MantlememoError):
    pass


class MantlememoRuntimeError(MantlememoError):
    pass

