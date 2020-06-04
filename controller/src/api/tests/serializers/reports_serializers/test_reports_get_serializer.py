from api.serializers.reports_serializers import ReportsGetSerializer
from faker import Faker


fake = Faker()

def create(cusomter_name, templates, start_date, end_date, sent, opened, clicked, target_count):
    data = {
        'customer_name': cusomter_name,
        'templates': templates,
        'start_date': start_date,
        'end_date': end_date,
        'sent': sent,
        'opened': opened,
        'clicked': clicked,
        'target_count': target_count
    }
    serializer = ReportsGetSerializer(data=data)
    return serializer


def test_creation():
    serializer = create(fake.name(), fake.pydict(), fake.date_time(), fake.date_time(), fake.random_number(), fake.random_number(), fake.random_number(), fake.random_number())

    assert isinstance(serializer, ReportsGetSerializer)
    assert serializer.is_valid()
