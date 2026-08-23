#!/usr/bin/env python3

import os
import site
import struct
import sys
from pathlib import Path


platformio_core_dir = Path(os.environ.get("PLATFORMIO_CORE_DIR", Path.home() / ".platformio"))
site.addsitedir(str(platformio_core_dir / "packages" / "tool-stcgal"))

from stcgal.frontend import StcGal, cli
from stcgal.protocols import Stc8gProtocol


initialize_protocol = StcGal.initialize_protocol
choose_range = Stc8gProtocol.choose_range


def initialize_stc8g_protocol(self, opts):
    if opts.protocol != "stc8g":
        return initialize_protocol(self, opts)

    self.protocol = Stc8gProtocol(
        opts.port,
        opts.handshake,
        opts.baud,
        round(opts.trim * 1000),
    )
    self.protocol.debug = opts.debug


def choose_stc8g_range(self, packet, response, target_count):
    result = choose_range(self, packet, response, target_count)
    if result is not None:
        return result

    calibration_length = response[1]
    challenge_data = packet[2:]
    calibration_data = response[2:]
    samples_by_range = {}

    for index in range(calibration_length):
        trim, trim_range = struct.unpack(
            "BB", challenge_data[index * 2:index * 2 + 2]
        )
        count, = struct.unpack(
            ">H", calibration_data[index * 2:index * 2 + 2]
        )
        samples_by_range.setdefault(trim_range, []).append((trim, count))

    for trim_range, samples in samples_by_range.items():
        samples.sort()
        for (trim_a, count_a), (trim_b, count_b) in zip(samples, samples[1:]):
            if not min(count_a, count_b) <= target_count <= max(count_a, count_b):
                continue
            if count_a == count_b:
                continue

            target_trim = round(
                (target_count - count_a) * (trim_b - trim_a)
                / (count_b - count_a) + trim_a
            )
            if 6 <= target_trim <= 250:
                return target_trim, trim_range

    return None


StcGal.initialize_protocol = initialize_stc8g_protocol
Stc8gProtocol.choose_range = choose_stc8g_range


if __name__ == "__main__":
    sys.exit(cli())
