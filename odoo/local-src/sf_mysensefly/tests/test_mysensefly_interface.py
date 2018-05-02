# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from mock import patch

MOCK_PATH = 'odoo.addons.sf_mysensefly.models.mysensefly_interface'


class TestMySenseFlyInterface(TransactionCase):
    def setUp(self):
        super(TestMySenseFlyInterface, self).setUp()
        self.MySenseFlyInterface = self.env['sf.mysensefly.interface']

    def test_interface_call_with_get_spare_parts(self):
        drone_type = self.env.ref('sf_drone_info.sf_drone_type01')
        partner = self.env.ref('sf_drone_info.sf_partner01')
        outcome = \
            self.env['sf.mysensefly.interface'].call(
                'get_spare_parts', [drone_type.id, partner.id])
        self.assertEqual(len(outcome), 1)

    @patch(MOCK_PATH + '.requests.put')
    @patch(MOCK_PATH + '.MySenseFlyInterface.get_sensefly_api_parameters')
    def test_assign_invitation_key_with_success(
            self, mock_get_api_params, mock_put):
        mock_get_api_params.return_value = {
            'base_url': 'https://test.sensefly.io/v1/',
            'user': 'odoo-service',
            'password': 'mypassword',
            'endpoint': 'invitation-keys/'
        }

        mock_put.return_value.status_code = 204

        data = {
            "invitationKey": "1234-9876",
            "product": {
                "model": {
                    "category": "drone",
                    "code": "eb",
                    "designation": "Ebee Plus"
                },
                "serialNumber": "EB-001-58414",
                "uuid": "product_uuid231231"
            }
        }

        result = self.MySenseFlyInterface.assign_invitation_key(data)
        self.assertTrue(result)

    @patch(MOCK_PATH + '.MySenseFlyInterface.get_sensefly_api_parameters')
    def test_assign_invitation_key_with_wrong_param_config_fail(
            self, mock_get_api_params):
        mock_get_api_params.return_value = {
            'base_url': 'https://test.sensefly.io/v1/',
            'user': 'odoo-service',
            # No pass provided
            'password': '',
            'endpoint': 'invitation-keys/'
        }

        data = {
            "invitationKey": "1234-9876",
            "product": {
                "model": {
                    "category": "drone",
                    "code": "EB",
                    "designation": "something"
                },
                "serialNumber": "EB-001-58414",
                "uuid": "product_uuid231231"
            }
        }

        result = self.MySenseFlyInterface.assign_invitation_key(data)
        self.assertFalse(result)
