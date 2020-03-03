#!/usr/bin/env python

"""Tests for `viewclust` package."""


import unittest

import viewclust


class TestViewclust(unittest.TestCase):
    """Tests for `viewclust` package."""

    def setUp(self):
        self.series_output = 2185

    def test_target_series(self):
        # Q4:
        d_from = '2019-10-01T00:00:00'
        d_dec = '2019-12-01T00:00:00'
        d_to = '2019-12-31T00:00:00'

        time_frames = [(d_from, d_dec, 100), (d_dec, d_to, 500)]
        series = viewclust.target_series(time_frames)
        assert self.series_output == series.size
