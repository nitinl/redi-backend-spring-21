"""
Description: Custom Exceptions for the messaging application
"""


class ChatNotFoundException(Exception):
    pass


class ChatAlreadyExistsException(Exception):
    pass


class NoPreviousMessageException(Exception):
    pass
