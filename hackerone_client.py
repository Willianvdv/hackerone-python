import urllib2, urllib, json

class And:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def to_graphql(self):
        return 'and: { left: { %(left)s }, right: { %(right)s } }' % {
            'left': self.left.to_graphql(),
            'right': self.right.to_graphql()
        }

class Or:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def to_graphql(self):
        return 'or: { left: { %(left)s }, right: { %(right)s } }' % {
            'left': self.left.to_graphql(),
            'right': self.right.to_graphql()
        }

class EqualExpression:
    def __or__(self, other):
        return Or(self, other)

    def __and__(self, other):
        return And(self, other)

    def __init__(self, field, value):
       self.field = field
       self.value = value

    def to_graphql(self):
       return '%(field_name)s: { equals: "%(value)s" }' % {
           'field_name': self.field.to_graphql(),
           'value': self.value
       }

class FakeGraphqlable:
    def __init__(self, graphql):
        self.graphql = graphql

    def to_graphql(self):
         return self.graphql

class Field:
    def __init__(self, name):
       self.name = name

    def to_graphql(self):
        return self.name

    def __eq__(self, value):
        return EqualExpression(self, value)

    def __call__(self, *children):
        return FakeGraphqlable(
            '%(field_name)s { %(children)s }' % {
                'field_name': self.to_graphql(),
                'children': ' '.join([child.to_graphql() for child in children])
            }
        )

class Team:
    id = Field('id')

class Report:
    def __init__(self, attributes):
        self.attributes = attributes

    @property
    def id(self):
      return self.attributes['id']

    id = Field('id')
    team_id = Field('team_id')
    team = Field('team')

class HackeroneClient:
    def report(self, id, columns=[]):
        graphql_query = '''
          query {
            report(id: %(id)i) {
              id
              %(report_fragment)s
            }
          }
        ''' % {
            'id': id,
            'report_fragment': self._report_fragment(columns)
        }

        return Report(self._query_graphql(graphql_query)['data']['report'])

    def reports(self, first = 10, filters = [], columns = []):
        graphql_where = filters.to_graphql()

        graphql_query = '''
          query {
            reports(first: %(first)s, filter: { %(filter)s }) {
              edges {
                node {
                  id
                  %(report_fragment)s
                }
              }
            }
          }
        ''' % {
            'filter': graphql_where,
            'first': first,
            'report_fragment': self._report_fragment(columns)
        }

        nodes = self._query_graphql(graphql_query)['data']['reports']['edges']
        return [Report(n['node']) for n in nodes]

    def _report_fragment(self, columns):
        return '... on Report { %s }' % \
            ' '.join([column.to_graphql() for column in columns])

    def _query_graphql(self, graphql_query):
        response = urllib2.urlopen(
            'https://hackerone.com/graphql',
            urllib.urlencode({ 'query': graphql_query })
        )

        json_response = json.loads(response.read())

        # TODO: Raise whem json_response['data'] is present

        return json_response
