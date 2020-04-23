"""
Customer Serializers.

These are Django Rest Famerwork Serializers. These are used for
serializing data coming from the db into a request responce.
"""
# Third-Party Libraries
from api.models.customer_models import CustomerModel
from rest_framework import serializers


class CustomerContactSerializer(serializers.Serializer):
    """
    This is the CustomerContact Serializer.

    This is a formats the data coming out of the Db.
    """

    first_name = serializers.CharField(max_length=250)
    last_name = serializers.CharField(max_length=250)
    title = serializers.CharField(max_length=250)
    phone = serializers.CharField(max_length=250)
    email = serializers.EmailField(max_length=None, min_length=None, allow_blank=False)
    notes = serializers.CharField(max_length=None, min_length=None, allow_blank=True)


class CustomerGetSerializer(serializers.Serializer):
    """
    This is the CustomerGet Serializer.

    This is a formats the data coming out of the Db.
    """

    # created by mongodb
    customer_uuid = serializers.UUIDField()
    # user created fields
    name = serializers.CharField(max_length=250)
    identifier = serializers.CharField(max_length=250)
    address_1 = serializers.CharField(max_length=250)
    address_2 = serializers.CharField(max_length=250)
    city = serializers.CharField(max_length=250)
    state = serializers.CharField(max_length=250)
    zip_code = serializers.CharField(max_length=250)
    contact_list = CustomerContactSerializer(many=True)
    # db data tracking added below
    created_by = serializers.CharField(max_length=100)
    cb_timestamp = serializers.DateTimeField()
    last_updated_by = serializers.CharField(max_length=100)
    lub_timestamp = serializers.DateTimeField()


class CustomerPostSerializer(serializers.Serializer):
    """
    This is the CustomerPost Serializer.

    This is a formats the data coming in from the user for a post create.
    """

    # user created fields
    name = serializers.CharField(max_length=250)
    identifier = serializers.CharField(max_length=250)
    address_1 = serializers.CharField(max_length=250)
    address_2 = serializers.CharField(max_length=250)
    city = serializers.CharField(max_length=250)
    state = serializers.CharField(max_length=250)
    zip_code = serializers.CharField(max_length=250)
    contact_list = CustomerContactSerializer(many=True)


class CustomerPostResponseSerializer(serializers.Serializer):
    """
    This is the CustomerPostResponse Serializer.

    This is a formats the data coming out of the Db from a create.
    """

    # created by mongodb
    customer_uuid = serializers.UUIDField()


class ExpSerializer(serializers.ModelSerializer):
    """
    This is the CustomerPostResponse Serializer.

    This is a formats the data coming out of the Db from a create.
    """

    class Meta:
        """Meta Class."""

        model = CustomerModel
        fields = ("customer_uuid", "name")
