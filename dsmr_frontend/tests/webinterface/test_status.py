from unittest import mock

from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse

from dsmr_consumption.models.consumption import ElectricityConsumption, GasConsumption
from dsmr_consumption.models.energysupplier import EnergySupplierPrice
from dsmr_stats.models.statistics import DayStatistics


class TestViews(TestCase):
    """ Test whether views render at all. """
    fixtures = [
        'dsmr_frontend/test_dsmrreading.json',
        'dsmr_frontend/test_note.json',
        'dsmr_frontend/test_energysupplierprice.json',
        'dsmr_frontend/test_statistics.json',
        'dsmr_frontend/test_meterstatistics.json',
        'dsmr_frontend/test_electricity_consumption.json',
        'dsmr_frontend/test_gas_consumption.json',
    ]
    namespace = 'frontend'
    support_data = True
    support_gas = True

    def setUp(self):
        self.client = Client()

    @mock.patch('django.utils.timezone.now')
    def test_status(self, now_mock):
        now_mock.return_value = timezone.make_aware(timezone.datetime(2016, 1, 1))
        response = self.client.get(
            reverse('{}:status'.format(self.namespace))
        )
        self.assertEqual(response.status_code, 200, response.content)
        self.assertIn('monitoring_issues', response.context)


class TestViewsWithoutData(TestViews):
    """ Same tests as above, but without any data as it's flushed in setUp().  """
    fixtures = []
    support_data = support_gas = False

    def setUp(self):
        super(TestViewsWithoutData, self).setUp()

        for current_model in (ElectricityConsumption, GasConsumption, DayStatistics):
            current_model.objects.all().delete()

        self.assertFalse(ElectricityConsumption.objects.exists())
        self.assertFalse(GasConsumption.objects.exists())
        self.assertFalse(DayStatistics.objects.exists())


class TestViewsWithoutPrices(TestViews):
    """ Same tests as above, but without any price data as it's flushed in setUp().  """

    def setUp(self):
        super(TestViewsWithoutPrices, self).setUp()
        EnergySupplierPrice.objects.all().delete()
        self.assertFalse(EnergySupplierPrice.objects.exists())


class TestViewsWithoutGas(TestViews):
    """ Same tests as above, but without any GAS related data.  """
    fixtures = [
        'dsmr_frontend/test_dsmrreading_without_gas.json',
        'dsmr_frontend/test_note.json',
        'dsmr_frontend/test_energysupplierprice.json',
        'dsmr_frontend/test_statistics.json',
        'dsmr_frontend/test_meterstatistics.json',
        'dsmr_frontend/test_electricity_consumption.json',
    ]
    support_gas = False

    def setUp(self):
        super(TestViewsWithoutGas, self).setUp()
        self.assertFalse(GasConsumption.objects.exists())
