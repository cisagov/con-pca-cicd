"""
This is the type file.

Here we define types to be imported into models and used for validation.
This is using schematics.type as a base
"""
# Standard Python Libraries
import datetime
import uuid

# Third-Party Libraries
# These imports are so models.py can import all its types from this file.
from schematics.types import BooleanType as BaseBooleanType
from schematics.types import DateTimeType as BaseDateTimeType
from schematics.types import DictType as BaseDictType
from schematics.types import FloatType as BaseFloatType
from schematics.types import IntType as BaseIntType
from schematics.types import ListType as BaseListType
from schematics.types import ModelType as BaseModelType
from schematics.types import StringType as BaseStringType


class UUIDType(BaseStringType):
    """
    UUIDType.

    Base class for UUIDType.
    """

    def __init__(self, *args, **kwargs):
        """
        Init.

        Adding regex, required, _mock and max_length checking.
        """
        self.regex = r"^[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}$"
        self.required = kwargs.get("required", True)
        self._mock = lambda self_instance, context=None: str(uuid.uuid4())
        self.max_length = self.min_length = 36
        super().__init__(
            required=self.required,
            min_length=self.min_length,
            max_length=self.max_length,
            regex=self.regex,
        )


class StringType(BaseStringType):
    """
    StringType.

    Base class for StringType.
    """

    def __init__(self, **kwargs):
        """
        Init.

        Adding required checking.
        """
        try:
            self.example = kwargs.pop("example")
        except KeyError:
            # raise TypeError("Example is a required parameter.")
            pass
        super().__init__(**kwargs)


class IntType(BaseIntType):
    """
    IntType.

    Base class for IntType.
    """

    def __init__(self, *arg, **kwargs):
        """
        Init.

        Adding required checking.
        """
        try:
            self.example = kwargs.pop("example")
        except KeyError:
            # raise TypeError("Example is a required parameter.")
            pass
        super().__init__(**kwargs)


class FloatType(BaseFloatType):
    """
    FloatType.

    Base class for FloatType.
    """

    def __init__(self, *arg, **kwargs):
        """
        Init.

        Adding required checking.
        """
        try:
            self.example = kwargs.pop("example")
        except KeyError:
            # raise TypeError("Example is a required parameter.")
            pass
        super().__init__(**kwargs)


class EmailType(BaseStringType):
    """
    EmailType.

    Base class for EmailType.
    Adding regex for email validation.
    """

    def __init__(self, *arg, **kwargs):
        """
        Init.

        Adding required and regex checking.
        """
        self._mock = lambda self_instance, context=None: "Mr.Example@example.com"
        if "regex" in kwargs:
            self.regex = kwargs.pop("regex")
        else:
            self.regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        super().__init__(required=self.required, regex=self.regex)


class DateTimeType(BaseDateTimeType):
    """
    DateTimeType.

    Base class for DateTimeType.
    """

    def _mock(self, context=None):
        """
        A wrapper function.

        Around the the BaseDateTimeType class' _mock
        function that truncates the datetime object's microseconds to a
        precision tolerable by MongoDB's DateTime native type
        :param context:
        :return: python native datetime object
        :rtype: datetime.dateime

        To ensure we can compare the return value of tests
        for now let's just generate everything in utc
        """
        dt = super(DateTimeType, self)._mock(context).astimezone(datetime.timezone.utc)
        return dt.replace(microsecond=int(dt.microsecond / 1000) * 1000)

    def to_primitive(self, value, context=None):
        """
        To_primitive.

        Circumvent around the inherited to_primitive function to ensure that serialized
        datetime str is in the format that matches ``datetime.datetime.astimzezone(datetime.timezone.utc).isformat()``
        :param value: Native value of this field in the model's object
        :param context: Optional context can be none
        :return: Serialized string containing datetime in the following ISO format ``<YYYY>-<MM>-<DD>T<hh>:<mm>[:<ss.ssssss>]±<hh>[:][<mm>].
        :rtype: str
        """
        if isinstance(value, datetime.datetime):
            return value.astimezone(datetime.timezone.utc).isoformat()
        else:
            # huh it is NOT an instance of datetime.datetime?
            # ok let the super method deal with this
            return super(DateTimeType, self).to_primitive(value, context)


class BooleanType(BaseBooleanType):
    """
    BooleanType.

    Base class for BooleanType.
    """

    def __init__(self, *arg, **kwargs):
        """
        Init.

        Adding required checking.
        """
        try:
            self.example = kwargs.pop("example")
        except KeyError:
            # raise TypeError("Example is a required parameter.")
            pass
        super().__init__(**kwargs)


class DictType(BaseDictType):
    """
    DictType.

    Base class for DictType.
    """

    def __init__(self, *arg, **kwargs):
        """
        Init.

        Adding required checking.
        """
        try:
            self.example = kwargs.pop("example")
        except KeyError:
            # raise TypeError("Example is a required parameter.")
            pass
        super().__init__(**kwargs)


class ListType(BaseListType):
    """
    ListType.

    Base class for ListType.
    """

    def __init__(self, *arg, **kwargs):
        """
        Init.

        Adding required checking.
        """
        try:
            self.example = kwargs.pop("example")
        except KeyError:
            # raise TypeError("Example is a required parameter.")
            pass
        super().__init__(**kwargs)


class ModelType(BaseModelType):
    """
    ModelType.

    Base class for ModelType.
    """

    def __init__(self, *arg, **kwargs):
        """
        Init.

        Adding required checking.
        """
        try:
            self.example = kwargs.pop("example")
        except KeyError:
            # raise TypeError("Example is a required parameter.")
            pass
        super().__init__(**kwargs)
