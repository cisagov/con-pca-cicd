"""Utils file for api."""

# Third-Party Libraries
from config.settings import DB_CONFIG
from database.service import Service

sample_data = [
    {
        "SubscriptionName": "SC-1031.Matt-Daemon.1.1",
        "Status": "  Waiting on SRF",
        "PrimaryContact": " Matt Daemon",
        "Customer": "Some Company.2com",
        "LastActionDate": " 3/26/2020",
        "Active": "prohibit",
    },
    {
        "SubscriptionName": "SC-1221.Ben-Aflex.1.1",
        "Status": "  Waiting on SRF",
        "PrimaryContact": " Ben Aflex",
        "Customer": "Some Company.3com",
        "LastActionDate": " 3/26/2020",
        "Active": True,
    },
    {
        "SubscriptionName": "SC-654.George-Clooney.1.1",
        "Status": "  Stopped",
        "PrimaryContact": " George Clooney",
        "Customer": "Some Company.1com",
        "LastActionDate": " 3/26/2020",
        "Active": True,
    },
    {
        "SubscriptionName": "SC-654.George-Clooney.1.2",
        "Status": "  Stopped",
        "PrimaryContact": " George Clooney",
        "Customer": "Some Company.1com",
        "LastActionDate": " 3/26/2020",
        "Active": True,
    },
    {
        "SubscriptionName": "SC-654.George-Clooney.1.3",
        "Status": "  Waiting for New Template",
        "PrimaryContact": " George Clooney",
        "Customer": "Some Company.1com",
        "LastActionDate": " 3/26/2020",
        "Active": True,
    },
    {
        "SubscriptionName": "SC-654.George-Clooney.2.1",
        "Status": "  Stopped",
        "PrimaryContact": " George Clooney",
        "Customer": "Some Company.1com",
        "LastActionDate": " 3/26/2020",
        "Active": True,
    },
    {
        "SubscriptionName": "SC-654.George-Clooney.2.2",
        "Status": "  Stopped",
        "PrimaryContact": " George Clooney",
        "Customer": "Some Company.1com",
        "LastActionDate": " 3/26/2020",
        "Active": True,
    },
    {
        "SubscriptionName": "SC-654.George-Clooney.2.3",
        "Status": "  Running Campaign",
        "PrimaryContact": " George Clooney",
        "Customer": "Some Company.1com",
        "LastActionDate": "3/26/2020",
        "Active": True,
    },
    {
        "SubscriptionName": "IDEQ-1234.Mary-Stephens.1.1",
        "Status": "  Waiting on ROE",
        "PrimaryContact": " Mary Stephens",
        "Customer": "Idaho DEQ State Agency",
        "LastActionDate": "4/2/2020",
        "Active": True,
    },
    {
        "SubscriptionName": "DOE-1.Don-Mann.1.1",
        "Status": " Waiting on Domain Approval",
        "PrimaryContact": " Don Mann",
        "Customer": "DOE Federal",
        "LastActionDate": "4/2/2020",
        "Active": True,
    },
    {
        "SubscriptionName": "DOE-1.Jane-Doe.1.1",
        "Status": "90 Day Cycle Ended",
        "PrimaryContact": "Jane Doe",
        "Customer": "DOE Federal",
        "LastActionDate": "4/2/2020",
        "Active": True,
    },
    {
        "SubscriptionName": "DODLOF-1.Jane-Moore.1.1",
        "Status": " Waiting on Template Approval",
        "PrimaryContact": " Jane Moore",
        "Customer": "DOD Little Office Federal",
        "LastActionDate": "4/2/2020",
        "Active": True,
    },
    {
        "SubscriptionName": "MDMV-1.David-Young.1.1",
        "Status": " Starting Campaigns",
        "PrimaryContact": "David Young",
        "Customer": "Maryland DMV State Agency",
        "LastActionDate": "4/2/2020",
        "Active": True,
    },
    {
        "SubscriptionName": "STO-1.Sefina.1.1",
        "Status": " Waiting for New Templates",
        "PrimaryContact": "Sefina CISO",
        "Customer": "Samoa Territorial Office",
        "LastActionDate": "4/2/2020",
        "Active": True,
    },
    {
        "SubscriptionName": "DEdu.Sarah-Jones.1.1",
        "Status": "Paused",
        "PrimaryContact": "Sarah Jones",
        "Customer": "Department of Eduation",
        "LastActionDate": "4/2/2020",
        "Active": True,
    },
    {
        "SubscriptionName": "FORD-1.Jerry-Ford.1.1",
        "Status": "Stopped",
        "PrimaryContact": "Jerry Ford",
        "Customer": "Ford New Cars",
        "LastActionDate": "4/2/2020",
        "Active": True,
    },
]


class Subscription(object):
    """Todo: remove this."""

    def __init__(self, name, status, primary_contact, customer, last_action, active):
        """Todo: remove this."""
        self.name = name
        self.status = status
        self.primary_contact = primary_contact
        self.customer = customer
        self.last_action = last_action
        self.active = active


def db_service(collection_name, model, validate_model):
    """
    Db_service.

    This is a method for handling db connection in api.
    Might refactor this into database lib.
    """
    mongo_uri = "mongodb://{}:{}@{}:{}/".format(
        DB_CONFIG["DB_USER"],
        DB_CONFIG["DB_PW"],
        DB_CONFIG["DB_HOST"],
        DB_CONFIG["DB_PORT"],
    )

    service = Service(
        mongo_uri,
        collection_name=collection_name,
        model=model,
        model_validation=validate_model,
    )

    return service
