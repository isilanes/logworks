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
DEFAULT_FORMATTER = logging.Formatter(
        fmt='{asctime} {colored_levelname} {message}',
        datefmt="%Y-%m-%d %H:%M:%S",
        style="{"
)


# Functions:
def example():
    """Show some examples."""

    print("Code:\n")
    code  = "from logworks import logworks\n"
    code += "logger = logworks.Logger()\n"
    code += "logger.info(\"This is some info\")\n"
    code += "logger.warning(\"Danger! Danger!\")\n"
    code += "logger.error(\"Something went wrong\")"
    print(code)

    print("\nYields:\n")
    logger = Logger()
    logger.info("This is some info")
    logger.warning("Danger! Danger!")
    logger.error("Something went wrong")

    print("\nCustom formatter:\n")
    formatter = logging.Formatter(
            fmt='{asctime} {colored_levelname} {message}',
            datefmt="%H:%M:%S",
            style="{"
    )
    logger = Logger(formatter=formatter, which_logger="altered")
    logger.info("This is some custom info")


# Classes:
class Logger(object):
    """Class to hold logging stuff."""
    
    # Constructor:
    def __init__(self, conf_fn=None, use_color=True, formatter=DEFAULT_FORMATTER, which_logger=__name__):
        # If given a configuration file name, try to read it:
        self.conf = Logger.read_conf(conf_fn)

        # Avoid colors?:
        self.no_color = not use_color

        # Logger object:
        self.logger = logging.getLogger(which_logger)
        self.logger.setLevel(logging.DEBUG)

        # Console output handler:
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        ch.setLevel(logging.DEBUG)
        self.logger.addHandler(ch)


    # Public methods:
    def info(self, text):
        """Log (print) 'text' as info."""

        extra = {
            "colored_levelname": self.with_info_color("[INFO]"),
        }

        self.logger.info(text, extra=extra)

    def warning(self, text):
        """Log (print) 'text' as warning."""

        extra = {
            "colored_levelname": self.with_warning_color("[WARNING]"),
        }

        self.logger.warning(text, extra=extra)

    def error(self, text):
        """Log (print) 'text' as error."""

        extra = {
            "colored_levelname": self.with_error_color("[ERROR]"),
        }

        self.logger.error(text, extra=extra)

    def with_name_color(self, text):
        """Return 'text' with color for name."""

        return self._colorize_as(text, "name")

    def with_info_color(self, text):
        """Return 'text' with color for 'info'."""

        return self._colorize_as(text, "info")

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


# If called directly, show some examples:
if __name__ == "__main__":
    example()

