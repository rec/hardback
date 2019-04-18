Updates on 12 April 2019.
----------------------------


First light
============

I've been generating really quite nice books in the epub format for several
days now - here's a
`very little one <https://raw.githubusercontent.com/rec/hardback/master/images/laser.epub>`_
where the QR codes contain the data for the image on the front cover.

There's quite a bit more I want to do in terms of flexibility - I have it
hardcoded to one specific size of QR code that made nice neat 1K blocks per QR
code, and a bunch of them look really nice on a page - but now I'm like, well,
there are 20 different QR codes to choose from, so I should really be able to
try all sorts of different types and block sizes!

And different layouts too of course - those were already configurable.

So I want all of this configurable now.  :-D

But that won't take too many more days.


What does this look like as an actual book?
================================================
I don't fully know!  Actual printing will come quite late in the process:
I don't want to waste the world's resources on random pre-pre-pre-pre-proofs.

epub does appear to be _the_ open-source format for doing both ebooks and
hardcopy printing.

I don't suppose we know anyone who works in this epub format already?

It's pretty easy for me to read an existing epub book that someone designed
and just insert the last few chapters of QR codes as documents, so that's my
eventual intention - get a designer and let them pretty it up.


Packaging
===========

Of course, like so many technical things, "packaging and productionizing" takes
a huge amount of time.  :-D

It would save me a huge amount of work if I could deliver this to you as a
command line application - in other words, where you open a terminal and type a
bit of code (that I would tell you how to type).

(For various dull reasons, drag-and-drop/application-land on Mac is hard to
accomplish "right now".)

More error correction?
========================

I'm spending considerable time contemplating how this book could be damaged.
For example, what if you made a hole in it - one that happened to get rid of the
metadata chunk?

Well, that's not actually an issue because there's already code that puts a
duplicate metadata block at some increment "around 1.5 pages apart" and with a
greatest common divisor of 1 with the page size, which means that the metadata
will appear in every area of the page over enough pages.

(Actually, as I explained this I realized there's a subtle bug in my code
there, which I `just fixed
<https://github.com/rec/hardback/commit/712da73d61e5c78ee2c76d955d73bc31e288f55d>`_)

And there's actual error correction on each individual RFC code (Reed-Solomon
error correction codes to be specific.

But we could easily add Reed-Solomon correction also to the whole thing.

The advantage of error correction is that you can reproduce the document even if
some whole QR codes were completely obliterated or even changed - even if
they're error-correcting QR codes that are obliterated or changed.

I'll look into this.  Perhaps we can use less error correction on each
individual QR code and more on the whole document?


Another idea
============

I could use RGB to put three layers on top of each other and get three times as
much data into the same page - but then recovering the data becomes more
challenging.

It might just be a more interesting book even if it were less useful for
archival formats.
