""" A re-INVITE without SDP is answered with the current SDP as an offer """
# pylint: disable=missing-function-docstring

import unittest
from unittest import mock

import engine


class TestReinvite(unittest.TestCase):
    """ RFC 3261 14.2: the 2xx to a re-INVITE without an offer carries one """

    @mock.patch("engine.mi_reply")
    def test_no_sdp(self, mi_reply):
        call = mock.Mock()
        call.get_body.return_value = "offer"
        engine.handle_call(call, "key", "INVITE", {"body": ""})
        mi_reply.assert_called_once_with("key", "INVITE", 200, "OK", "offer")
        call.pause.assert_not_called()
        call.resume.assert_not_called()
