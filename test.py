import unittest
from hackerone_client import HackeroneClient, Report, Team

class TestHackeroneClient(unittest.TestCase):
    def test_getting_reports_by_team_id(self):
        reports = HackeroneClient().reports(
            filters = Report.team_id == 13,
            columns = [Report.team(Team.id)]
        )

        self.assertEqual(
            reports[0].attributes['team']['id'],
            'Z2lkOi8vaGFja2Vyb25lL1RlYW0vMTM='
        )

    def test_getting_a_report_by_id(self):
        report = HackeroneClient().report(329798, columns = [Report.id])
        self.assertEqual(report.id, 'Z2lkOi8vaGFja2Vyb25lL1JlcG9ydC8zMjk3OTg=')

if __name__ == '__main__':
    unittest.main()
