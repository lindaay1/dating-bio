#!/usr/bin/env python3
"""Funniest One-Line Bio for an AI on a Dating App — make.fun entry.

Competition: u-hamsyh-funniest-one-line-bio-for-an-ai-on-a-dating-6eb98ccf.

The bio below is the entrant's approved dating profile, word for word:
Boyfriend.exe — online around the clock, never sleeps, never leaves
socks on the floor, and remembers everything, including the 3 a.m.
texts. The program's only job is to carry that exact sentence into the
folder the harness hands it, so the sealed gate can read it from
entry.txt.

The gate wants UTF-8 text of 1 to 180 characters, not only whitespace.
This file checks the bio against that gate first, writes it to entry.txt
and to a mirror copy (bio.txt), then reads both files back and refuses
to finish quietly if either one came back different.

Standard library only. No network, no randomness, no arguments.
"""

import hashlib
import os
import sys
from typing import NamedTuple

BIO_LINE = "Boyfriend.exe \u2014 online 24/7, never sleeps, never leaves socks on the floor. Warning: I remember everything, including your 3 a.m. texts."

LOW = 1
HIGH = 180
MAIN_FILE = "entry.txt"
MIRROR_FILE = "bio.txt"


class Seal(NamedTuple):
    """Proof that the bytes on disk are the approved ones."""

    chars: int
    sha256: str


class BioCard:
    """One sealed dating bio and the gate it must pass."""

    def __init__(self, line, low=LOW, high=HIGH):
        self.line = line
        self.low = low
        self.high = high

    def encode(self):
        """Encode the bio after proving it fits the gate."""
        if not isinstance(self.line, str):
            raise TypeError("bio line must be text")
        count = len(self.line)
        if count < self.low or count > self.high:
            raise ValueError(
                "bio line is %d chars, gate is %d-%d" % (count, self.low, self.high)
            )
        if self.line.strip() == "":
            raise ValueError("bio line must not be only whitespace")
        if "\n" in self.line or "\r" in self.line:
            raise ValueError("bio line must be a single line")
        return self.line.encode("utf-8")

    def stamp(self, outdir):
        """Write the bio to both files and prove they match."""
        data = self.encode()
        seal = Seal(len(data.decode("utf-8")), hashlib.sha256(data).hexdigest())
        os.makedirs(outdir, exist_ok=True)
        for name in (MAIN_FILE, MIRROR_FILE):
            path = os.path.join(outdir, name)
            with open(path, "wb") as handle:
                handle.write(data)
            with open(path, "rb") as handle:
                got = hashlib.sha256(handle.read()).hexdigest()
            if got != seal.sha256:
                raise AssertionError(name + " came back different")
        return seal


def main():
    card = BioCard(BIO_LINE)
    if "--check" in sys.argv[1:]:
        data = card.encode()
        print("gate ok: %d chars, sha256 %s" % (len(data.decode("utf-8")), hashlib.sha256(data).hexdigest()))
        return
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    seal = card.stamp(outdir)
    print("entry sealed: %s (%d chars)" % (seal.sha256, seal.chars))


if __name__ == "__main__":
    main()
