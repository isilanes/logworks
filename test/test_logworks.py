# Standard libs:
import os
import mock
import logging
import unittest
from io import StringIO

# Our libs:
from logworks import logworks


# Classes:
class TestLogger(unittest.TestCase):
    """Test Logger() class."""

    # Setup and teardown:
    def setUp(self):
        self.TEXTS = ["something", "yadda yadda", "", None]
        self.COLORS = {
            "name": 31,
            "info": 32,
            "warning": 33,
            "error": 34,
        }
        with mock.patch("sys.stdout"), mock.patch("sys.stderr"):
            self.logger = logworks.Logger()

    def tearDown(self):
        logger = None
        if os.path.isfile("logworks.log"):
            os.unlink("logworks.log")

    # Test constructor:
    def test_constructor_no_args(self):
        # Run:
        logger = self.logger

        # Assert:
        self.assertIsInstance(logger.conf, dict)
        self.assertEqual(logger.no_color, False)
        self.assertIsInstance(logger.logger, logging.Logger)
    
    def test_constructor_no_color(self):
        # Run:
        with mock.patch("sys.stdout", new_callable=StringIO) as stdout, mock.patch("sys.stderr"):
            logger = logworks.Logger(use_color=False)

        # Assert:
        self.assertIsInstance(logger.conf, dict)
        self.assertEqual(logger.no_color, True)
        self.assertIsInstance(logger.logger, logging.Logger)
    
    def test_constructor_with_empty_conf_file(self):
        # Run:
        with mock.patch("sys.stdout", new_callable=StringIO) as stdout, mock.patch("sys.stderr"):
            logger = logworks.Logger(conf_fn="whatever")

        # Assert:
        self.assertIsInstance(stdout.getvalue(), str)
        self.assertIsInstance(logger.conf, dict)
        self.assertEqual(logger.conf, {})
        self.assertIsInstance(logger.logger, logging.Logger)
    
    # Test print shortcuts:
    def test_info(self):
        # Prepare:
        logger = self.logger
        logger.logger.info = mock.Mock()
        logger.with_info_color = mock.Mock()

        for text in self.TEXTS:
            # Prepare:
            logger.logger.info.reset_mock()
            logger.with_info_color.reset_mock()

            # Run:
            logger.info(text)

            # Assert:
            logger.logger.info.assert_called_once()
            self.assertIn(text, logger.logger.info.call_args[0])
            logger.with_info_color.assert_called_once()

    def test_warning(self):
        # Prepare:
        logger = self.logger
        logger.logger.warning = mock.Mock()
        logger.with_warning_color = mock.Mock()

        for text in self.TEXTS:
            # Prepare:
            logger.logger.warning.reset_mock()
            logger.with_warning_color.reset_mock()

            # Run:
            logger.warning(text)

            # Assert:
            logger.logger.warning.assert_called_once()
            self.assertIn(text, logger.logger.warning.call_args[0])
            logger.with_warning_color.assert_called_once()

    def test_error(self):
        # Prepare:
        logger = self.logger
        logger.logger.error = mock.Mock()
        logger.with_error_color = mock.Mock()

        for text in self.TEXTS:
            # Prepare:
            logger.logger.error.reset_mock()
            logger.with_error_color.reset_mock()

            # Run:
            logger.error(text)

            # Assert:
            logger.logger.error.assert_called_once()
            self.assertIn(text, logger.logger.error.call_args[0])
            logger.with_error_color.assert_called_once()

    # Test colorizers:
    def test_with_name_color(self):
        # Prepare:
        logger = self.logger

        # Run:
        for text in self.TEXTS:
            ret = logger.with_name_color(text)

            # Assert:
            self.assertIn(str(text), str(ret))

    def test_with_info_color(self):
        # Prepare:
        logger = self.logger

        # Run:
        for text in self.TEXTS:
            ret = logger.with_info_color(text)

            # Assert:
            self.assertIn(str(text), str(ret))

    def test_with_warning_color(self):
        # Prepare:
        logger = self.logger

        # Run:
        for text in self.TEXTS:
            ret = logger.with_warning_color(text)

            # Assert:
            self.assertIn(str(text), str(ret))

    def test_with_error_color(self):
        # Prepare:
        logger = self.logger

        # Run:
        for text in self.TEXTS:
            ret = logger.with_error_color(text)

            # Assert:
            self.assertIn(str(text), str(ret))

    def test_colorize_as_with_colors(self):
        # Prepare:
        logger = self.logger
        with mock.patch("logworks.logworks.Logger.use_colors"): # to be able to override it (being a @property)
            logger.use_colors = True
            logger.conf = {"colors": self.COLORS}

            # Run:
            for which in self.COLORS:
                ret = logger._colorize_as(which, which)

                # Assert:
                self.assertIn(which, ret)
                self.assertNotEqual(which, ret)

    def test_colorize_as_without_colors(self):
        # Prepare:
        logger = self.logger
        with mock.patch("logworks.logworks.Logger.use_colors"): # to be able to override it (being a @property)
            logger.use_colors = False
            logger.conf = {"colors": self.COLORS}

            # Run:
            for which in self.COLORS:
                ret = logger._colorize_as(which, which)

                # Assert:
                self.assertEqual(which, ret)

    def test_color_for_can(self):
        # Prepare:
        logger = self.logger
        logger.conf = {"colors": self.COLORS}

        for which in self.COLORS:
            # Run:
            ret = logger._color_for(which)

            # Assert:
            self.assertEqual(ret, self.COLORS[which])

    def test_color_for_cant(self):
        # Prepare:
        logger = self.logger
        logger.conf = {}

        for which in self.COLORS:
            # Run:
            ret = logger._color_for(which)

            # Assert:
            self.assertEqual(ret, 0)

    def test_colorize(self):
        # Run:
        for text in self.TEXTS:
            ret = logworks.Logger.colorize(text, 666)
            
            # Assert:
            self.assertIn(str(text), str(ret))
            self.assertIn("666", str(ret))

    def test_colorize_none(self):
        # Run:
        for text in self.TEXTS:
            ret = logworks.Logger.colorize(text, None)
            
            # Assert:
            self.assertEqual(ret, text)

    # Test other:
    def test_use_colors_no_conf(self):
        # Prepare:
        logger = self.logger

        # Assert:
        self.assertTrue(logger.use_colors)

    def test_use_colors_empty_conf(self):
        # Prepare:
        logger = self.logger
        logger.conf = {}

        # Assert:
        self.assertFalse(logger.use_colors)

    def test_use_colors_nocolor_overrides(self):
        # Prepare:
        logger = self.logger
        logger.no_color = True
        logger.conf = {"colorize": True}

        # Assert:
        self.assertFalse(logger.use_colors)

    def test_use_colors_yes(self):
        # Prepare:
        logger = self.logger
        logger.nocolor = False
        logger.conf = {"colorize": True}

        # Assert:
        self.assertTrue(logger.use_colors)

    def test_read_conf(self):
        # Prepare:
        conf_data = {"a": 3}
        conf_string = '{"a": 3}'
        fn = "file_which_does_not_exist"

        # Run:
        with mock.patch("builtins.open", mock.mock_open(read_data=conf_string)) as mock_file:
            ret = logworks.Logger.read_conf(fn)
            mock_file.assert_called_with(fn)
            
        # Assert:
        self.assertEqual(ret, conf_data)

    def test_read_conf_no_conf(self):
        # Run:
        ret = logworks.Logger.read_conf()

        # Assert:
        self.assertEqual(ret, {})

    def test_read_conf_cant_read(self):
        with mock.patch("sys.stdout"):
            # Run:
            ret = logworks.Logger.read_conf("file_which_does_not_exist")
            
        # Assert:
        self.assertEqual(ret, {})


class TestConsoleLogger(unittest.TestCase):
    """Test ConsoleLogger() class."""

    # Setup and teardown:
    def setUp(self):
        self.TEXTS = ["something", "yadda yadda", "", None]
        self.COLORS = {
            "name": 31,
            "info": 32,
            "warning": 33,
            "error": 34,
        }
        with mock.patch("sys.stdout"), mock.patch("sys.stderr"):
            self.logger = logworks.ConsoleLogger()

    def tearDown(self):
        pass

    # Test constructor:
    def test_constructor_no_args(self):
        # Run:
        logger = self.logger

        # Assert:
        self.assertIsInstance(logger.conf, dict)
        self.assertEqual(logger.no_color, False)
        self.assertIsInstance(logger.logger, logging.Logger)
    
    def test_constructor_no_color(self):
        # Run:
        with mock.patch("sys.stdout"), mock.patch("sys.stderr"):
            logger = logworks.ConsoleLogger(use_color=False)

        # Assert:
        self.assertIsInstance(logger.conf, dict)
        self.assertEqual(logger.no_color, True)
        self.assertIsInstance(logger.logger, logging.Logger)
    
    def test_constructor_with_empty_conf_file(self):
        # Run:
        with mock.patch("sys.stdout", new_callable=StringIO) as stdout, mock.patch("sys.stderr"):
            logger = logworks.ConsoleLogger(conf_fn="whatever")

        # Assert:
        self.assertIsInstance(stdout.getvalue(), str)
        self.assertIsInstance(logger.conf, dict)
        self.assertEqual(logger.conf, {})
        self.assertIsInstance(logger.logger, logging.Logger)


class TestFileLogger(unittest.TestCase):
    """Test ConsoleLogger() class."""

    # Setup and teardown:
    def setUp(self):
        self.TEXTS = ["something", "yadda yadda", "", None]
        self.COLORS = {
            "name": 31,
            "info": 32,
            "warning": 33,
            "error": 34,
        }
        with mock.patch("sys.stdout"), mock.patch("sys.stderr"):
            self.logger = logworks.FileLogger()

    def tearDown(self):
        logger = None
        if os.path.isfile("logworks.log"):
            os.unlink("logworks.log")

    # Test constructor:
    def test_constructor_no_args(self):
        # Run:
        logger = self.logger

        # Assert:
        self.assertIsInstance(logger.conf, dict)
        self.assertEqual(logger.no_color, True)
        self.assertIsInstance(logger.logger, logging.Logger)
    
    def test_constructor_no_color(self):
        # Run:
        logger = self.logger

        # Assert:
        self.assertIsInstance(logger.conf, dict)
        self.assertEqual(logger.no_color, True)
        self.assertIsInstance(logger.logger, logging.Logger)
    
    def test_constructor_with_empty_conf_file(self):
        # Run:
        with mock.patch("sys.stdout", new_callable=StringIO) as stdout, mock.patch("sys.stderr"):
            logger = logworks.ConsoleLogger(conf_fn="whatever")

        # Assert:
        self.assertIsInstance(stdout.getvalue(), str)
        self.assertIsInstance(logger.conf, dict)
        self.assertEqual(logger.conf, {})
        self.assertIsInstance(logger.logger, logging.Logger)


class TestMain(unittest.TestCase):
    """Test stuff outside Logger() class."""

    # Setup and teardown:
    def setUp(self):
        pass

    def tearDown(self):
        if os.path.isfile("logworks.log"):
            os.unlink("logworks.log")

    # Test version:
    def test_version_ok(self):
        self.assertIsInstance(logworks.__version__, str)

    def test_version_ko(self):
        # Preprare:
        import importlib
        import pkg_resources
        
        # Run:
        with mock.patch("pkg_resources.get_distribution", side_effect=pkg_resources.DistributionNotFound) as mock_pkg:
            importlib.reload(logworks)
        
        # Assert:
        self.assertIsNone(logworks.__version__)

        # Clean:
        importlib.reload(logworks)

