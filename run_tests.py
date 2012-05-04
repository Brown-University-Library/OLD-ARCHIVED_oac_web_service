#!/usr/bin/env jython

import unittest2

# First, discover all tests in the project
loader = unittest2.TestLoader()
tests = loader.discover('.')

# Create a runner and run those tests.
testRunner = unittest2.runner.TextTestRunner()
testRunner.run(tests)