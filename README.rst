hardback: hard-copy backup of digital data
------------------------------------------------

In one sentence
==================

Archive a digital document as a hardcopy book that can then be turned back
into the original document.


High level picture
======================

There are only two parts to this project:
* Writing the original document or book from a digital document
* Reading the book back in

Writing is non-trivial, but there is a clear path to a good solution for that.

But I really don't have any solid solution yet to reading, short of someone
scanning each QR code individually.

Of course, that is a reasonable solution if you care about the data and don't
mind paying someone to take the time.


The book format is EPUB
============================================

The output format will be EPUB, https://en.wikipedia.org/wiki/EPUB -
the only choice for an open-source book format, full-featured and universally
accepted.

I'm using a Python library called EBookLib for this - I haven't looked
into it thoroughly yet, but it seems well-received and there is no other
candidate in Python.

The data format within the book is QR code
=======================

QR codes will be used to store the data in 1k blocks - again, QR is the only
reasonable choice for solving the problem of printable data.

A Python library called segno can write each one as a tiny PNG file about 2K in
size. This is quite reasonable - it means that we can aim to create a book
document that's less than three times the size of the original digital
document. (Interestingly enough, SVG files were an order of magnitude larger -
in some cases over one hundred times larger!)

We'll be using QR code format 36, which holds up to 1,051 bytes at the highest
error correction code level, 'H'.

The official list of all the QR code formats,
https://www.qrcode.com/en/about/version.html is poorly organized - click on
31-40 and then scroll down.

I'm going to use that to hold 1024 bytes of target data with a sequence number
and a hash of the original document, totalling 1,048 bytes.  (The extra 3 bytes
aren't entirely wasted - we get a tiny bit better error correction.)

The layout in bytes within the QR data is like this:

| data [1024] | hash [16] | sequence number [8] |

There's no checksum or error correction for the data itself, as the QR code is
already taking care of that for us.

The hash is the first 16 bytes of the 32-byte SHA256 hash of the entire
document.

The sequence number is a _signed_ (i.e. positive, negative or zero) 8-byte
integer.

If the sequence number is positive, then this QR code contains a data
block, and the sequence number says how many blocks it is from the start.
Eight bytes allows us to generate 2 to the power of 63 blocks of 1K each,
or about 9 zetabytes (which is 9,000,000,000,000 gigabytes) - roughly the
entire size of all the world's data in 2019.

If the sequence number is zero or negative, then it is a metadata block.

The block with sequence number zero always contains a JSON description of the
original file with the fields ``filename``, ``timestamp``, ``size`` and
``sha256``.  If the original filename is too long (which would be about 900
characters or so!), it is truncated from the left.

Blocks with negative sequence numbers are currently unspecified and reserved
for future expansion or individuals to use.  The first version of the software
will only produce output with non-negative sequence numbers.
