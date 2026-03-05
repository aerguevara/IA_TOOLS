import unittest
from unittest.mock import patch, MagicMock
from infra.external.notification_adapter import EmailNotificationAdapter

class TestNotificationAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = EmailNotificationAdapter()

    @patch('smtplib.SMTP')
    @patch.dict('os.environ', {
        'SMTP_SERVER': 'localhost',
        'SMTP_PORT': '1025',
        'SENDER_EMAIL': 'test@release.com'
    })
    def test_send_release_report_success(self, mock_smtp):
        mock_server = mock_smtp.return_value.__enter__.return_value
        
        report_data = {
            "release_id": "REL-1",
            "status": "Success",
            "pr_links": ["http://pr1", "http://pr2"]
        }
        
        self.adapter.send_release_report(["boss@company.com"], report_data)
        
        self.assertTrue(mock_server.send_message.called)
        msg = mock_server.send_message.call_args[0][0]
        self.assertEqual(msg['To'], "boss@company.com")
        self.assertIn("REL-1", msg['Subject'])

    @patch('smtplib.SMTP')
    def test_send_release_report_failure(self, mock_smtp):
        mock_smtp.side_effect = Exception("SMTP Server Down")
        # Should not raise exception, just print error (as per implementation)
        self.adapter.send_release_report(["boss@company.com"], {})
