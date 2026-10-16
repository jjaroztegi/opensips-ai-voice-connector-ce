""" A hold re-INVITE is answered with the direction RFC 3264 6.1 requires """
# pylint: disable=missing-function-docstring

import unittest

from aiortc.sdp import SessionDescription

from call import Call

SDP = ("v=0\r\n"
       "o=- 1 1 IN IP4 192.0.2.1\r\n"
       "s=-\r\n"
       "c=IN IP4 192.0.2.1\r\n"
       "t=0 0\r\n"
       "m=audio 4000 RTP/AVP 8\r\n"
       "a=rtpmap:8 PCMA/8000\r\n"
       "a=sendrecv\r\n")


def make_call():
    """ Returns a Call with only its SDP set up """
    call = Call.__new__(Call)
    call.b2b_key = "key"
    call.paused = False
    call.sdp = SessionDescription.parse(SDP)
    return call


class TestHold(unittest.TestCase):
    """ sendonly -> recvonly, inactive -> inactive, sendrecv -> sendrecv """

    def test_hold_and_resume(self):
        call = make_call()
        call.pause("sendonly")
        self.assertEqual(call.sdp.media[0].direction, "recvonly")
        call.pause("inactive")  # already on hold
        self.assertEqual(call.sdp.media[0].direction, "inactive")
        self.assertTrue(call.paused)
        call.resume()
        self.assertEqual(call.sdp.media[0].direction, "sendrecv")
        self.assertFalse(call.paused)

    def test_inactive(self):
        call = make_call()
        call.pause("inactive")
        self.assertEqual(call.sdp.media[0].direction, "inactive")
