{{ name | escape | underline}}

.. automodule:: {{ fullname }}
    :members:
    :undoc-members:
    :show-inheritance:

{% block modules %}
{% if modules %}
.. autosummary::
   :toctree:
   :template: custom-module-template.rst
   :recursive:
{% for item in modules %}
   {{ item }}
{%- endfor %}
{% endif %}
{% endblock %}