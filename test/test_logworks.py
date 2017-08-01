# Standard libs:
import mock
import logging
import unittest

# Our libs:
import logworks

# Classes:
class TestLogger(unittest.TestCase):
    """Test Logger() class."""

    # Setup and teardown:
    def setUp(self):
        self.texts = ["something", "yadda yadda", "", None]
        self.colors = ["name", "info", "warning", "error"]
        self.conf_colors = {
            "name": 1,
            "info": 2,
            "warning": 3,
            "error": 4,
        }

    def tearDown(self):
        pass


    # Test constructor:
    def test_constructor_no_args(self):
        # Run:
        logger = logworks.Logger()

        # Assert:
        self.assertEqual(logger.conf, {})
        self.assertEqual(logger.nocolor, False)
        self.assertIsInstance(logger.logger, logging.Logger)
    
    def test_constructor_no_color(self):
        # Run:
        logger = logworks.Logger(nocolor=True)

        # Assert:
        self.assertEqual(logger.conf, {})
        self.assertEqual(logger.nocolor, True)
        self.assertIsInstance(logger.logger, logging.Logger)
    

    # Test print shortcuts:
    def test_info(self):
        # Prepare:
        logger = logworks.Logger()
        logger.logger.info = mock.Mock()
        logger.with_info_color = mock.Mock()

        for text in self.texts:
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
        logger = logworks.Logger()
        logger.logger.warning = mock.Mock()
        logger.with_warning_color = mock.Mock()

        for text in self.texts:
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
        logger = logworks.Logger()
        logger.logger.error = mock.Mock()
        logger.with_error_color = mock.Mock()

        for text in self.texts:
            # Prepare:
            logger.logger.error.reset_mock()
            logger.with_error_color.reset_mock()

            # Run:
            logger.error(text)

            # Assert:
            logger.logger.error.assert_called_once()
            self.assertIn(text, logger.logger.error.call_args[0])
            logger.with_error_color.assert_called_once()


    # Text colorizers:
    def test_with_name_color(self):
        # Prepare:
        logger = logworks.Logger()

        # Run:
        for text in self.texts:
            ret = logger.with_name_color(text)

            # Assert:
            self.assertIn(str(text), str(ret))

    def test_with_info_color(self):
        # Prepare:
        logger = logworks.Logger()

        # Run:
        for text in self.texts:
            ret = logger.with_info_color(text)

            # Assert:
            self.assertIn(str(text), str(ret))

    def test_with_warning_color(self):
        # Prepare:
        logger = logworks.Logger()

        # Run:
        for text in self.texts:
            ret = logger.with_warning_color(text)

            # Assert:
            self.assertIn(str(text), str(ret))

    def test_with_error_color(self):
        # Prepare:
        logger = logworks.Logger()

        # Run:
        for text in self.texts:
            ret = logger.with_error_color(text)

            # Assert:
            self.assertIn(str(text), str(ret))

    def test_color_for_can(self):
        # Prepare:
        logger = logworks.Logger()
        logger.conf = {"colors": self.conf_colors}

        # Run:
        for which in self.colors:
            ret = logger._color_for(which)

            # Assert:
            self.assertEqual(ret, self.conf_colors[which])

    def test_color_for_cant(self):
        # Prepare:
        logger = logworks.Logger()
        logger.conf = {}

        # Run:
        for which in self.colors:
            ret = logger._color_for(which)

            # Assert:
            self.assertEqual(ret, 0)

