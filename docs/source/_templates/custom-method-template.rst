.. currentmodule:: {{ modname }}

.. autoclass:: {{ class_name }}
   :members:
   :show-inheritance:
   :inherited-members:
   :special-members: __init__

{% for method in methods %}
   {% if "SuperClass." not in method %}
   .. automethod:: {{ method }}
   {% endif %}
{% endfor %}
