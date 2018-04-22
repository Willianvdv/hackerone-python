# HackerOne Binding Via GraphQL

Very experimental, don't use me.

## Usage

All reports reported to team 13 (/security)

```python
HackeroneClient().reports(
  filters = Report.team_id == 13,
  columns = [Report.team(Team.id)]
)
```

Fetch a specific report
```python
HackeroneClient().report(329798, columns = [Report.id])
```
