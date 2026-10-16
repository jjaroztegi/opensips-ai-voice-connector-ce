""" A re-INVITE with a 0.0.0.0 connection address puts the call on hold """
# pylint: disable=missing-function-docstring

import unittest
from unittest import mock

from aiortc import RTCRtpCodecParameters

import engine

SDP = ("v=0\r\n"
       "o=- 1 2 IN IP4 192.0.2.1\r\n"
       "s=-\r\n"
       "c=IN IP4 {}\r\n"
       "t=0 0\r\n"
       "m=audio 4000 RTP/AVP 8\r\n"
       "a=rtpmap:8 PCMA/8000\r\n")


def make_call():
    """ Returns a mock call using PCMA """
    call = mock.Mock()
    call.codec.params = RTCRtpCodecParameters(mimeType="audio/PCMA",
                                              clockRate=8000, payloadType=8)
    return call


@mock.patch("engine.mi_reply")
class TestHoldZero(unittest.TestCase):
    """ RFC 3264 8.4: c=0.0.0.0 means nothing is to be sent to the peer """

    def test_zero_address(self, mi_reply):
        call = make_call()
        engine.handle_call(call, "key", "INVITE", {"body": SDP.format("0.0.0.0")})
        call.pause.assert_called_once_with("inactive")
        call.resume.assert_not_called()
        mi_reply.assert_called_once()

    def test_address(self, _):
        call = make_call()
        engine.handle_call(call, "key", "INVITE", {"body": SDP.format("192.0.2.1")})
        call.resume.assert_called_once()
        call.pause.assert_not_called()
