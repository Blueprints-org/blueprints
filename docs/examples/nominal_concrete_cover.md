# Nominal Concrete Cover

Calculating the nominal concrete cover is an important step in the design of reinforced concrete structures.
The nominal concrete cover is the minimum thickness of concrete that separates the reinforcing steel from the environment.
This thickness is necessary to protect the steel from corrosion and to ensure the durability of the structure.

`Blueprints` provides a simple way to calculate the nominal concrete cover using NEN-EN 1992-1-1:2011.
This example can be followed step by step by first importing the necessary classes and functions, (or [go to the full code example](#full-code-example)):

```python
--8<-- "examples/_code/nominal_concrete_cover.py:4:8"
```

Define the concrete material properties to be used in the calculation:

```python
--8<-- "examples/_code/nominal_concrete_cover.py:11"
```

Calculate the structural class by its exposure classes, design working life and other parameters:

```python
--8<-- "examples/_code/nominal_concrete_cover.py:14:20"
```

Start the nominal concrete cover calculation:

```python
--8<-- "examples/_code/nominal_concrete_cover.py:23:34"
```

Then just print the results:

```python
--8<-- "examples/_code/nominal_concrete_cover.py:37:47"
```

The output will be:

```python
Structural class: S5

C,min,dur: 20.0 mm
C,min,b: 32.0 mm
C,min,total: 32.0 mm
    Cover increase due to uneven surface: 0 mm
    Cover increase due to abrasion: 0 mm

Nominal concrete cover: 60.0 mm
    C,nom: 42.0 mm
    Minimum cover with regard to casting surface: 60.0 mm
```

You could also use the `NominalConcreteCover` to get a latex representation of the calculation by using:

```python
--8<-- "examples/_code/nominal_concrete_cover.py:51"
```

The output will be:

```latex
Nominal~concrete~cover~according~to~art.~4.4.1~from~NEN-EN~1992-1-1+C2:2011:\newline~\max~\left\{Nominal~concrete~cover~according~to~art.~4.4.1~(c_{nom});~Minimum~cover~with~regard~to~casting~surface~according~to~art.~4.4.1.3~(4)\right\}\newline~=~\max~\left\{42.0;~60.0\right\}~=~60.0~mm\newline~\newline~Where:\newline~\hspace{4ex}c_{nom}~=~c_{min,total}+\Delta~c_{dev}~=~32.0+10~=~42.0~mm\newline~\hspace{4ex}\Delta~c_{dev}~is~determined~according~to~art.~4.4.1.3~(1)\newline~\hspace{4ex}c_{min,total}~=~c_{min}~+~\Delta~c_{uneven~surface}~~+~\Delta~c_{abrasion~class}~=~32.0~+~0~+~0~=~32.0~mm\newline~\hspace{4ex}\Delta~c_{uneven~surface}~and~\Delta~c_{abrasion~class}~are~determined~according~to~art.~4.4.1.2~(11)~and~(13)\newline~\hspace{4ex}c_{min}~=~\max~\left\{c_{min,b};~c_{min,dur}+\Delta~c_{dur,\gamma}-\Delta~c_{dur,st}-\Delta~c_{dur,add};~10~\text{mm}\right\}~=~\max~\left\{32.0;~20.0+10-0-0;~10\right\}~=~32.0~mm\newline~\hspace{4ex}\Delta~c_{dur,\gamma}~,~\Delta~c_{dur,st}~and~\Delta~c_{dur,add}~are~determined~according~to~art.~4.4.1.2~(6),~(7)~and~(8)\newline~\hspace{4ex}c_{min,b}~is~determined~according~to~table~4.2~based~on~(equivalent)~rebar~diameter~=~32~=~32~mm\newline~\hspace{4ex}c_{min,dur}~is~determined~according~to~table~4.4~based~on~structural~class~S5~\&~exposure~classes~(XC1)~=~20~mm
```

You could use an external service like [lagrida](https://latexeditor.lagrida.com/) to render the latex code or use this output inside a latex or word document of your choice.

<a name="full-code-example">
The full code example:

```python
--8<-- "examples/_code/nominal_concrete_cover.py"
```
</a>
