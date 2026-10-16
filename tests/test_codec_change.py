""" A re-INVITE that does not offer the call's codec is rejected """
# pylint: disable=missing-function-docstring

import unittest
from unittest import mock

from aiortc import RTCRtpCodecParameters

import engine

SDP = ("v=0\r\n"
       "o=- 1 2 IN IP4 192.0.2.1\r\n"
       "s=-\r\n"
       "c=IN IP4 192.0.2.1\r\n"
       "t=0 0\r\n"
       "m=audio 4000 RTP/AVP {}\r\n")


def make_call():
    """ Returns a mock call using PCMA """
    call = mock.Mock()
    call.codec.params = RTCRtpCodecParameters(mimeType="audio/PCMA",
                                              clockRate=8000, payloadType=8)
    call.get_body.return_value = "answer"
    return call


@mock.patch("engine.mi_reply")
class TestCodecChange(unittest.TestCase):
    """ RFC 3264 6.1: the answer's formats must come from the offer """

    def test_other_codec(self, mi_reply):
        call = make_call()
        engine.handle_call(call, "key", "INVITE", {"body": SDP.format("0")})
        mi_reply.assert_called_once_with("key", "INVITE", 488, "Not Acceptable Here")
        call.resume.assert_not_called()

    def test_same_codec(self, mi_reply):
        engine.handle_call(make_call(), "key", "INVITE", {"body": SDP.format("0 8")})
        mi_reply.assert_called_once_with("key", "INVITE", 200, "OK", "answer")
