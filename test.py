import unittest

import urllib2, urllib, json

class Report:
    def __init__(self, attributes):
        self.attributes = attributes

    @property
    def id(self):
      return self.attributes['id']

class HackeroneClient:
    def report(self, id, columns=[]):
        graphql_query = '''
          query {
            report(id: %(id)i) {
              id
              %(report_fragment)s
            }
          }
        ''' % { 'id': id, 'report_fragment':self._report_fragment(columns) }

        return Report(self._query_graphql(graphql_query)['data']['report'])

    def reports(self, first = 10, where = None, columns = []):
        graphql_query = '''
          query {
            reports(first: %(first)s, filter: %(filter)s) {
              edges {
                node {
                  id
                  %(report_fragment)s
                }
              }
            }
          }
        ''' % { 'filter': where, 'first': first, 'report_fragment': self._report_fragment(columns) }

        nodes = self._query_graphql(graphql_query)['data']['reports']['edges']
        return [Report(n['node']) for n in nodes]

    def _report_fragment(self, columns):
        return '... on Report { %s }' % ' '.join(columns)

    def _query_graphql(self, graphql_query):
        response = urllib2.urlopen(
            'https://hackerone.com/graphql',
            urllib.urlencode({ 'query': graphql_query })
        )

        return json.loads(response.read())

class TestHackeroneClient(unittest.TestCase):
    def test_getting_reports_by_team_id(self):
        reports = HackeroneClient().reports(where = '{ team_id: { equals: "13" } }', columns = ['team { id }'])
        self.assertEqual(reports[0].attributes['team']['id'], 'Z2lkOi8vaGFja2Vyb25lL1RlYW0vMTM=')

    def test_getting_a_report_by_id(self):
        report = HackeroneClient().report(329798, ['_id'])
        self.assertEqual(report.id, 'Z2lkOi8vaGFja2Vyb25lL1JlcG9ydC8zMjk3OTg=')

if __name__ == '__main__':
    unittest.main()
