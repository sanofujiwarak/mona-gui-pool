mona-gui-pool
=============

Quickstart(Include to your Django app)
----------

1. execute commands in below::

    cd /path/to/app
    pip install -r requirements.pip
    pip install -e .

2. Add "app" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'gui_if',
      )

3. Include the gui_ifs URLconf in your project urls.py like this::

    url(r'^gui_if/', include('gui_if.urls', namespace="gui_if")),

4. Start the development server and visit http://127.0.0.1:8000/gui_if/
   to participate in the gui_if.
