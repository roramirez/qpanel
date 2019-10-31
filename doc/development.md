# Development

There some notes about development process


## Translations
Search and update the strings for `messages.po`

`pybabel extract -F qpanel/translations/babel.cfg -o qpanel/translations/messages.pot qpanel`


Update the translations for languages

`pybabel update -i qpanel/translations/messages.pot -o qpanel/translations`



## Reset Queue Stats

Using the dependencies `requirements/development.txt` is possible to use the dashboard monitor by

    `rq-scheduler-dashboard`
