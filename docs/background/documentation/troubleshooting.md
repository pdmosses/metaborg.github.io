# Documentation Troubleshooting


## Macro Syntax Error: Missing end of comment tag
The macros in the documentation, including in code blocks, is expanded through the `mkdocs-macros` plugin which uses the Jinja2 template processor. [Its template syntax](https://jinja.palletsprojects.com/en/3.0.x/templates/) is very advanced, allowing not only to replace simple references, but also more complex statements and comments. In this case, Jinja sees `{{'{#'}}` and interprets it as a comment. Of course, then it cannot find the end of the comment and produces an error.

{% raw %}
~~~plaintext
INFO - [macros] - ERROR # _Macro Syntax Error_
       _Line 11 in Markdown file:_ **Missing end of comment tag**
       ```python
       {# This is not a Jinja comment }
       ```
~~~
{% endraw %}


To work around this, wrap the block in a `{{'{% raw %}'}}` and `{{"{% endraw %}"}}` tag. For example:

~~~plaintext
{{'{% raw %}'}}
```
{{'{#'}} This is not a Jinja comment }
```
{{"{% endraw %}"}}
~~~

Alternatively, if you still want to use other macros in the code, wrap the offending character sequence in a template:

{% raw %}
```plaintext
{{'{#'}}
```
{% endraw %}

For example:

{% raw %}
~~~plaintext
```
{{'{#'}} This is not a Jinja comment }
```
~~~
{% endraw %}

In both cases the example gets rendered as:

```
{{'{#'}} This is not a Jinja comment }
```
