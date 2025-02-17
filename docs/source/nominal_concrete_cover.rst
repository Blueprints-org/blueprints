Nominal Concrete Cover
-------------------------------------------
Calculating the nominal concrete cover is an important step in the design of reinforced concrete structures.
The nominal concrete cover is the minimum thickness of concrete that separates the reinforcing steel from the environment.
This thickness is necessary to protect the steel from corrosion and to ensure the durability of the structure.

`Blueprints` provides a simple way to calculate the nominal concrete cover using NEN-EN 1992-1-1:2011.
This example can be followed st

Let's go step by step by first importing the necessary classes and functions, (or go straight to the full code example at the end of this page):

.. literalinclude:: examples/nominal_concrete_cover.py
    :lines: 4-8

Define the concrete material properties to be used in the calculation:

.. literalinclude:: examples/nominal_concrete_cover.py
    :lines: 11

Calculate the structural class by its exposure classes, design working life and other parameters

.. literalinclude:: examples/nominal_concrete_cover.py
    :lines: 14-20

Start the nominal concrete cover calculation.

.. literalinclude:: examples/nominal_concrete_cover.py
    :lines: 23-34

Then just print the results:

.. literalinclude:: examples/nominal_concrete_cover.py
    :lines: 37-47

The output will be:

.. code-block:: python

    Structural class: S5

    C,min,dur: 20.0 mm
    C,min,b: 32.0 mm
    C,min,total: 32.0 mm
        Cover increase due to uneven surface: 0 mm
        Cover increase due to abrasion: 0 mm

    Nominal concrete cover: 60.0 mm
        C,nom: 42.0 mm
        Minimum cover with regard to casting surface: 60.0 mm


You could also use the `NominalConcreteCover` to get a latex representation of the calculation by using:

.. literalinclude:: examples/nominal_concrete_cover.py
    :lines: 51

The output will be:

.. code-block:: latex

    Nominal~concrete~cover~according~to~art.~4.4.1~from~NEN-EN~1992-1-1+C2:2011:\newline~\max~\left\{Nominal~concrete~cover~according~to~art.~4.4.1~(c_{nom});~Minimum~cover~with~regard~to~casting~surface~according~to~art.~4.4.1.3~(4)\right\}\newline~=~\max~\left\{42.0;~60.0\right\}~=~60.0~mm\newline~\newline~Where:\newline~c_{nom}~=~c_{min,total}+\Delta~c_{dev}~=~32.0+10~=~42.0~mm\newline~\Delta~c_{dev}~is~determined~according~to~art.~4.4.1.3~(1)\newline~c_{min,total}~=~c_{min}~+~\Delta~c_{uneven~surface}~~+~\Delta~c_{abrasion~class}~=~32.0~+~0~+~0~=~32.0~mm\newline~\Delta~c_{uneven~surface}~and~\Delta~c_{abrasion~class}~are~determined~according~to~art.~4.4.1.2~(11)~and~(13)\newline~c_{min}~=~\max~\left\{c_{min,b};~c_{min,dur}+\Delta~c_{dur,\gamma}-\Delta~c_{dur,st}-\Delta~c_{dur,add};~10~\text{mm}\right\}~=~\max~\left\{32.0;~20.0+10-0-0;~10\right\}~=~32.0~mm\newline~\Delta~c_{dur,\gamma}~,~\Delta~c_{dur,st}~and~\Delta~c_{dur,add}~are~determined~according~to~art.~4.4.1.2~(6),~(7)~and~(8)\newline~c_{min,b}~is~determined~according~to~table~4.2~based~on~(equivalent)~rebar~diameter~=~32~=~32~mm\newline~c_{min,dur}~is~determined~according~to~table~4.3~based~on~structural~class~S5~\&~exposure~classes~(XC1)~=~20~mm\newline~Minimum~cover~with~regard~to~casting~surface~according~to~art.~4.4.1.3~(4)~=~k1~≥~c_{min,dur}~+~40~mm~for~Prepared~ground~(including~blinding)

You could use an external service like `lagrida <https://latexeditor.lagrida.com/>`_ to render the latex code or use this
output inside a latex or word document of your choice.

The full code example:

.. literalinclude:: examples/nominal_concrete_cover.py
