""" An INVITE without SDP gets an offer in the 200 OK (RFC 3261 13.2.1) """
# pylint: disable=missing-function-docstring

import asyncio
import unittest
from unittest import mock

from aiortc import RTCRtpCodecParameters
from aiortc.sdp import SessionDescription

import engine
from codec import PCMU


async def invite_without_sdp(mi_reply):
    ai = mock.AsyncMock()
    ai.get_codec = mock.Mock(return_value=PCMU(RTCRtpCodecParameters(
        mimeType="audio/PCMU", clockRate=8000, payloadType=0)))
    with mock.patch("call.get_ai", return_value=ai), \
            mock.patch("engine.parse_params", return_value=("openai", None, None)):
        engine.handle_call(None, "key", "INVITE", {"body": ""})
    await engine.calls.pop("key").close()
    return mi_reply.call_args.args


class TestLateOffer(unittest.TestCase):
    """ The 200 OK offers one codec on the call's RTP port """

    @mock.patch("engine.mi_reply")
    def test_no_sdp(self, mi_reply):
        _, _, code, _, body = asyncio.run(invite_without_sdp(mi_reply))
        self.assertEqual(code, 200)
        offer = SessionDescription.parse(body)
        self.assertEqual(offer.media[0].fmt, [0])
        self.assertNotEqual(offer.media[0].port, 9)
        self.assertNotEqual(offer.media[0].host or offer.host, "0.0.0.0")
