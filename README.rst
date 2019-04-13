hardback: hard-copy backup of digital data
------------------------------------------------

Newest updates are
`here <https://github.com/rec/hardback/blob/master/UPDATES.rst>`_.

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

Update: EBookLib is fairly gnarly, but the underlying format is just XHTML,
so I'm having reasonable success getting output.

The data format within the book is QR code
=============================================

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


Data layout
=============================

The binary data is divided into 1K *chunks*. A chunk is written to a QR code
as part of a *block*, which also contains a sequence number and a hash of the
original documet.

The layout in bytes within the block  is like this:

.. code-block:: text

    | sequence [8] | hash [16] | chunk [up to 1024] |

There's no checksum or error correction for this block itself, as the QR code is
already taking care of that for us.

``hash`` is the first 16 bytes of the 32-byte SHA256 hash of the entire
document.  ``data`` is one kilobyte from your target file.

``sequence`` is an 8-byte signed integer - a number that can be positive,
negative or zero, and that fits into 8 bytes (or equivalently 16 hex digits).

If the sequence number is zero or negative, then it is a metadata block.

The block with sequence number zero always contains a JSON description of the
original file with the fields ``filename``, ``timestamp``, ``size`` and
``sha256``.  If the original filename is too long (which would be about 900
characters or so!), it is truncated from the left.

Blocks with negative sequence numbers are currently unspecified and reserved
for future expansion or individuals to use.  The first version of the software
will only produce output with non-negative sequence numbers.

If ``sequence`` is positive, it's the sequence number of a data block.  This
means that the first data block has ``sequence`` 1.

Eight bytes allows us to generate 2 to the power of 63 blocks of 1K each, or
about 9 zetabytes (which is 9,000,000,000,000 gigabytes) - roughly the entire
size of all the world's data in 2019.

Within a block, ``sequence`` is is represented in `big-endian
<https://en.wikipedia.org/wiki/Endianness>`_ (or intuitive or network order) -
which means the *most* significant digits occur first.

Intel processors are little-ended, where the *least* significant digits come
first, so we use the `struct library
<https://docs.python.org/3/library/struct.html#byte-order-size-and-alignment>`_
to make sure that the output is system-independent.

Remembering that one byte is equal to two hex digits, if the hash of a
full document is
``56484fd9aad8e87540609ca6c938f98fab60296b3bec808ea8b3e24da2035ce9``
then the resulting sequence of QR codes would look like:

.. code-block:: text

    0000000000000000 56484fd9aad8e87540609ca6c938f98f {"filename": "me.jpg", ...
    0000000000000001 56484fd9aad8e87540609ca6c938f98f ... 1024 bytes ...
    0000000000000002 56484fd9aad8e87540609ca6c938f98f ... more data  ...
    ... etc

This means that each QR code identifies itself as to what part of the whole
document it is.

It also means that the metadata block is key to understanding how the whole
system works!  If you have a metadata block, then you can reconstruct at least
part of the data even if a lot of it is lost.  Otherwise, you really have to
guess.

So we're going to have to intersperse the metadata block within all the other
blocks periodically if we really want something that can be partially
reconstructed!

Update - this is done: the metadata blocks appear in varying locations on each
page so even a hole were punched through the book, some copy of the metadata
would probably survive.

Also, "raw" formats like RAW and AIFF are much preferable for this sort of
archival activity because compressed formats dramatically magnify the effect of
any errors or gaps.  If you had a book containing the digital data for an AIFF
or RAW, you could still reconstruct pieces of it even if you only have a
limited number of pages, whereas you might get nothing at all if you were using
mp3 or jpg files.
