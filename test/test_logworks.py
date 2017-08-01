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
        self.TEXTS = ["something", "yadda yadda", "", None]
        self.COLORS = {
            "name": 31,
            "info": 32,
            "warning": 33,
            "error": 34,
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
        logger = logworks.Logger()
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
        logger = logworks.Logger()
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
        logger = logworks.Logger()

        # Run:
        for text in self.TEXTS:
            ret = logger.with_name_color(text)

            # Assert:
            self.assertIn(str(text), str(ret))

    def test_with_info_color(self):
        # Prepare:
        logger = logworks.Logger()

        # Run:
        for text in self.TEXTS:
            ret = logger.with_info_color(text)

            # Assert:
            self.assertIn(str(text), str(ret))

    def test_with_warning_color(self):
        # Prepare:
        logger = logworks.Logger()

        # Run:
        for text in self.TEXTS:
            ret = logger.with_warning_color(text)

            # Assert:
            self.assertIn(str(text), str(ret))

    def test_with_error_color(self):
        # Prepare:
        logger = logworks.Logger()

        # Run:
        for text in self.TEXTS:
            ret = logger.with_error_color(text)

            # Assert:
            self.assertIn(str(text), str(ret))

    def test_colorize_as_with_colors(self):
        # Prepare:
        logger = logworks.Logger()
        with mock.patch("logworks.Logger.use_colors"): # to be able to override it (being a @property)
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
        logger = logworks.Logger()
        with mock.patch("logworks.Logger.use_colors"): # to be able to override it (being a @property)
            logger.use_colors = False
            logger.conf = {"colors": self.COLORS}

            # Run:
            for which in self.COLORS:
                ret = logger._colorize_as(which, which)

                # Assert:
                self.assertEqual(which, ret)

    def test_color_for_can(self):
        # Prepare:
        logger = logworks.Logger()
        logger.conf = {"colors": self.COLORS}

        for which in self.COLORS:
            # Run:
            ret = logger._color_for(which)

            # Assert:
            self.assertEqual(ret, self.COLORS[which])

    def test_color_for_cant(self):
        # Prepare:
        logger = logworks.Logger()
        logger.conf = {}

        for which in self.COLORS:
            # Run:
            ret = logger._color_for(which)

            # Assert:
            self.assertEqual(ret, 0)


    # Test other:
    def test_use_colors_no_conf(self):
        # Prepare:
        logger = logworks.Logger()

        # Assert:
        self.assertFalse(logger.use_colors)

    def test_use_colors_empty_conf(self):
        # Prepare:
        logger = logworks.Logger()
        logger.conf = {}

        # Assert:
        self.assertFalse(logger.use_colors)

    def test_use_colors_nocolor_overrides(self):
        # Prepare:
        logger = logworks.Logger()
        logger.nocolor = True
        logger.conf = {"colorize": True}

        # Assert:
        self.assertFalse(logger.use_colors)

    def test_use_colors_yes(self):
        # Prepare:
        logger = logworks.Logger()
        logger.nocolor = False
        logger.conf = {"colorize": True}

        # Assert:
        self.assertTrue(logger.use_colors)

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

    def test_read_conf_ok(self):
        # Run:
        with mock.patch("__builtin__.open") as mock_open:
            mock_open.return_value = mock.MagickMock(spec=file)
            mock_open.return_value.__enter__.return_value = "abc"
            ret = logworks.Logger.read_conf("file_which_does_not_exist")
            
        # Assert:
        self.assertEqual(ret, {})

