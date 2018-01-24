# Standard libs:
import json
import logging
import pkg_resources

# Version:
try:
    __version__ = pkg_resources.get_distribution("logworks").version
except pkg_resources.DistributionNotFound: # pkg not installed
    __version__ = None

# Globals:
DEFAULT_CONSOLE_FORMATTER = logging.Formatter(
    fmt='{asctime} {clevelname} {message}',
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{"
)
DEFAULT_FILE_FORMATTER = logging.Formatter(
    fmt='{asctime} [{levelname}] {message}',
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{"
)
DEFAULT_CONF = {
    "colorize": True,
    "logfile": "logworks.log",
    "colorize": True,
    "colors": {
        "debug": 37,
        "info": 34,
        "warning": 33,
        "error": 31,
        "name": 36,
        "ok": 32,
    }
}

# Functions:
def examples():
    """Show some examples."""

    print("#\n# Some examples\n#\n")

    print("""Code:\n
    from logworks import logworks
    logger = logworks.Logger()
    logger.debug("Verbose debug")
    logger.info("This is some info")
    logger.ok("Everything is ok")
    logger.warning("Danger! Danger!")
    logger.error("Something went wrong")
    """)

    print("Yields (no debug):\n")
    logger = Logger()
    logger.info("This is some info")
    logger.ok("Everything is ok")
    logger.warning("Danger! Danger!")
    logger.error("Something went wrong")

    print("""Code:\n
    from logworks import logworks
    logger = Logger(level=logging.DEBUG)
    logger.debug("Verbose debug")
    """)

    print("Yields (with debug):\n")
    logger = Logger(level=logging.DEBUG)

    logger.debug("Verbose debug")

    print("""\nNo colors:\n
    from logworks import logworks
    logger = logworks.Logger(use_color=False)
    logger.info("This is some info")
    logger.ok("Everything is ok")
    logger.warning("Danger! Danger!")
    logger.error("Something went wrong")
    """)

    print("Yields:\n")
    logger = Logger(use_color=False, which_logger="example2")
    logger.info("This is some info")
    logger.ok("Everything is ok")
    logger.warning("Danger! Danger!")
    logger.error("Something went wrong")

    print("""\nCustom formatter:\n
    import logging
    from logworks import logworks
    myformatter = logging.Formatter(
        fmt='{clevelname} - {asctime} - {message}',
        datefmt="%H:%M:%S",
        style="{"
    )
    logger = logworks.Logger(console_formatter=myformatter)
    logger.info("This is some custom info")
    """)

    print("Yields:\n")
    myformatter = logging.Formatter(
        fmt='{clevelname} - {asctime} - {message}',
        datefmt="%H:%M:%S",
        style="{"
    )
    logger = Logger(console_formatter=myformatter, which_logger="example3")
    logger.info("This is some custom info")


# Classes:
class Logger(object):
    """Class to hold logging stuff."""
    
    # Constructor:
    def __init__(self, conf_fn=None, use_color=True, console_formatter=DEFAULT_CONSOLE_FORMATTER, file_formatter=DEFAULT_FILE_FORMATTER,  which_logger=__name__, level=logging.INFO, console_output=True, file_output=False, logfile=None):
        # If given a configuration file name, try to read it:
        if conf_fn:
            self.conf = Logger.read_conf(conf_fn)
        else:
            self.conf = DEFAULT_CONF

        # Avoid colors?:
        self.no_color = not use_color

        # Logger object:
        self.logger = logging.getLogger(which_logger)
        self.logger.setLevel(level)

        # Console output handler:
        if console_output:
            ch = logging.StreamHandler()
            ch.setFormatter(console_formatter)
            ch.setLevel(level)
            self.logger.addHandler(ch)

        # File output handler:
        if file_output:
            if not logfile:
                logfile = self.conf["logfile"]
            fh = logging.FileHandler(logfile)
            fh.setFormatter(file_formatter)
            self.logger.addHandler(fh)


    # Public methods:
    def debug(self, text):
        """Log (print) 'text' as debug."""

        extra = {
            "clevelname": self.with_debug_color("[DEBUG]"),
        }

        self.logger.debug(text, extra=extra)

    def info(self, text):
        """Log (print) 'text' as info."""

        extra = {
            "clevelname": self.with_info_color("[INFO]"),
        }

        self.logger.info(text, extra=extra)

    def ok(self, text):
        """Log (print) 'text' as OK."""

        extra = {
            "clevelname": self.with_ok_color("[OK]"),
        }

        self.logger.info(text, extra=extra)

    def warning(self, text):
        """Log (print) 'text' as warning."""

        extra = {
            "clevelname": self.with_warning_color("[WARNING]"),
        }

        self.logger.warning(text, extra=extra)

    def error(self, text):
        """Log (print) 'text' as error."""

        extra = {
            "clevelname": self.with_error_color("[ERROR]"),
        }

        self.logger.error(text, extra=extra)

    def with_debug_color(self, text):
        """Return 'text' with color for name."""

        return self._colorize_as(text, "debug")

    def with_name_color(self, text):
        """Return 'text' with color for name."""

        return self._colorize_as(text, "name")

    def with_info_color(self, text):
        """Return 'text' with color for 'info'."""

        return self._colorize_as(text, "info")

    def with_ok_color(self, text):
        """Return 'text' with color for 'ok'."""

        return self._colorize_as(text, "ok")

    def with_error_color(self, text):
        """Return 'text' with color for 'error'."""

        return self._colorize_as(text, "error")

    def with_warning_color(self, text):
        """Return 'text' with color for 'warning'."""

        return self._colorize_as(text, "warning")


    # Private methods:
    def _colorize_as(self, text, which):
        """Return 'text' with color for 'which' type of text."""

        if self.use_colors:
            return Logger.colorize(text, self._color_for(which))
        
        return text

    def _color_for(self, which):
        """Return color for 'which'."""

        try:
            return self.conf["colors"][which]
        except:
            return 0


    # Public properties:
    @property
    def use_colors(self):
        """Return True if colors should be used in terminal.
        False otherwise.
        """
        if self.no_color:
            return False

        return "colorize" in self.conf and self.conf["colorize"]


    # Static methods:
    @staticmethod
    def read_conf(fn=None):
        """Read configuration file 'fn' and return dictionary with configuration.
        Return empty dir if we couldn't read.
        """
        if not fn:
            return {}

        try:
            with open(fn) as f_conf:
                return json.load(f_conf)
        except FileNotFoundError:
            print("Could not read logger configuration file '{f}'. Ignoring...".format(f=fn))
            return {}

    @staticmethod
    def colorize(text, color_number=None):
        """Return colorized version of 'text', with terminal color 'color_number' (31, 32...).
        Return bare text if 'color_number' is None.
        """
        if color_number is None:
            return text

        return "\033[{n}m{t}\033[0m".format(t=text, n=color_number)

class FileLogger(Logger):
    """A Logger() for file output only."""

    # Constructor:
    def __init__(self,
            logfile=None,
            conf_fn=None,
            file_formatter=DEFAULT_FILE_FORMATTER,
            which_logger=__name__,
            level=logging.DEBUG):
        super().__init__(
                conf_fn=conf_fn,
                file_formatter=file_formatter,
                which_logger=which_logger,
                level=level,
                console_output=False,
                file_output=True,
                logfile=logfile)


# If called directly, show some examples:
if __name__ == "__main__":
    examples()

