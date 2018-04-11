logworks is a convenience wrapper for the logging Python module. It is useful for me and the work I do at IHCantabria. 

I make it public with best wishes, but no implication is made about its potential utility and usability for others. logworks is distributed as free software, under the GPLv3.


## Some examples

NOTE: GitHub's markdown parser discards some HTML. As a result, the outputs below lack color.

### Default

```python
from logworks import logworks

logger = logworks.Logger()

logger.debug("Verbose debug")
logger.info("This is some info")
logger.ok("Everything is ok")
logger.warning("Danger! Danger!")
logger.error("Something went wrong")
```
    
Yields the following (your exact colors may vary). Note debug text is not logged.

<pre>
2018-04-11 12:10:35 <span style="color: blue">[INFO]</span> This is some info
2018-04-11 12:10:35 <span style="color: green">[OK]</span> Everything is ok
2018-04-11 12:10:35 <span style="color: goldenrod">[WARNING]</span> Danger! Danger!
2018-04-11 12:10:35 <span style="color: red">[ERROR]</span> Something went wrong
</pre>

### Debug

```python
import logging
from logworks import logworks

logger = logworks.Logger(level=logging.DEBUG)

logger.debug("Verbose debug")
```
    
Yields (now it logs debug). Note that default color for debug is no color.

<pre>
2018-04-11 12:10:35 [DEBUG] Verbose debug
</pre>

### No colors

```python
from logworks import logworks

logger = logworks.Logger(use_color=False)

logger.info("This is some info")
logger.ok("Everything is ok")
logger.warning("Danger! Danger!")
logger.error("Something went wrong")
```
    
Yields:

<pre>
2018-04-11 12:10:35 [INFO] This is some info
2018-04-11 12:10:35 [OK] Everything is ok
2018-04-11 12:10:35 [WARNING] Danger! Danger!
2018-04-11 12:10:35 [ERROR] Something went wrong
</pre>

### Custom formatter

```python
import logging
from logworks import logworks

myformatter = logging.Formatter(
    fmt='{clevelname} - {asctime} - {message}',
    datefmt="%H:%M:%S",
    style="{"
)

logger = logworks.Logger(console_formatter=myformatter)

logger.info("This is some custom info")
```
    
Yields:

<pre>
<span style="color: blue">[INFO]</span> - 12:10:35 - This is some custom info
</pre>
