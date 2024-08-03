A component in django-components is the combination of four things: CSS, Javascript, a Django template, and some Python code to put them all together.

```
sampleproject/
    ├── calendarapp/
    ├── components/             🆕
    │   └── calendar/           🆕
    │       ├── calendar.py     🆕
    │       ├── script.js       🆕
    │       ├── style.css       🆕
    │       └── template.html   🆕
    ├── sampleproject/
    ├── manage.py
    └── requirements.txt
```
# Render a string as html
To render a string as HTML in Django, you can use the `safe` filter or the `autoescape` template tag. Here are the steps for both methods:

### Using the `safe` Filter
The `safe` filter tells Django that the string should be rendered as HTML without escaping it.

```html
{{ my_string|safe }}
```

### Using the `autoescape` Template Tag
The `autoescape` tag can be used to turn off auto-escaping for a block of code.

```html
{% autoescape off %}
    {{ my_string }}
{% endautoescape %}
```

### Example
Suppose you have a string with HTML content:

```python
my_string = "<p>This is a paragraph.</p>"
```

In your template, you can render it as HTML using either method:

```html
<!-- Using the safe filter -->
{{ my_string|safe }}

<!-- Using the autoescape tag -->
{% autoescape off %}
    {{ my_string }}
{% endautoescape %}
```

Both methods will render the string as HTML, displaying the paragraph correctly on the web page.