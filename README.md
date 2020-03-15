# hon-macros
A PyQt5 GUI wrapper for some hon macros.

Macros should execute on parallel threads by starting an implementation of `QRunnable`.  This prevents the app being frozen until a macro completes.

Macros consist of a sequential set of actions.  Some common actions are mouse clicks and keystrokes.  Clicks are defined in relative coordinates to the HonWindow of interest.  

The HonWindow object(s) are instantiated upon app startup.  They contain global bounding boxes for some useful pieces of the hon UI, notably the clock and minimap.  Image searching in these regions is used for checking the time, hero location, and creep location.
