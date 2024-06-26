-*- restructuredtext -*-

Linda Tuple Spaces for Python
================================

This package implements simple Linda Tuple Spaces in Python, using
multiprocessing to allow writing code that makes full use of multicore
machines by still retaining a very simple communications API. Install
is quite standard:

easy_install lindypy

or just download the sources and run setup.py install. There are testcases
you can run with setup.py test, too.

I test and work with it under Python 2.6. Since I use multiprocessing,
Python 2.6 is the minimum python version needed.

What are Linda Tuple Spaces?
-----------------------------

Linda Tuple Spaces are a very nice communications abstraction for
concurrently running code. Processes communicate by sending tuples
into a big bag. Other processes register interest in some kinds of
tuples. When a process registers interest in some kind of tuple,
this process will block. As soon as a matching tuple is available,
the process will run and will receive it.

Tuples can be removed from the big bag, or you can grab a tuple out
of the bag without removing it. The tuple space makes sure that
tuple inserts and removes are managed atomically.

Read more at Wikipedia if you are interested in the topic:

http://en.wikipedia.org/wiki/Tuple_space

What does this package implement?
----------------------------------

This package implements a simple tuple space for use in simple
multiprocess environments that are not distributed. A distributed
tuple space is a beast far beyond this little package. I mostly
wrote this package to have a way to work with parallel processes
and have a much simpler communications paradigm. Especially I
wanted to experiment a bit more with blackboard architectures
and wanted to build on ideas I implemented with TooFPy, my
webservices framework. The end goal might be to sooner or later
deconstruct TooFPy into multiple small building blocks that can
be hooked together to form the original project or be used
standalone.

Tuples that are inserted and for which there is a direct interest
are directly delivered to the interested process and not inserted
into the tuplespace at all. But non-consuming interests are served,
too. The order on insert is as follows:

- deliver to all interested non-consuming processes
- deliver to the first interested consuming process
- if no consuming process is there, store in tuple space

Additionally worker processes put tuples (ExceptionObject, Traceback)
into the tuple space if they run into an exception. The exception
object can be matched with exception types and the traceback is
allready preprocessed. This is mostly meant for you to do some
error logging in some logger process.

What are the problems in the code
---------------------------------------

Objects passed around via tuples through the tuple space won't keep
identity due to the usage of pickle - so be aware of that, since it might
make your code work strangely if you expect objects to keep identity.

The timeout() context manager uses signals, so you can't have multiple
timeouts stacked. This is mostly used in the test cases, there is a
need for much better timeout handling in the tuplespace object itself.

Currently there is no tuplespace locking - all is just done with pipes.
That way, a massive "out"ing process could move tuples into the gap
on clients between the timeout on receives and the unregister, as the
unregister might take a moment for the manager to process the unregister.
This is mitigated by cleaning (and reinserting) tuples from a pipe
prior to registering a new interest, but that only works if the process
does regular inp/rd requests. So far I didn't come up with a good testcase
for triggering this. Of course you can allways say "don't abort
interests" and you should be fine, as the deregistration is done
on send then, and that only happens in the manager. The only concurrent
moment for deregistration to the managers activities is on aborted
interests.

Limits - or when not to use it
--------------------------------

The communication itself essentially uses pickles - that's how the
multiprocessing module works for pipes. That means tuples can only
contain pickleable data, so for example you can't eval closures, you need
to have toplevel callables. Additionally the communication is a bit on
the heavy side due to that, so this is probably not the right solution
if your problem needs loads of messages zipping around, it is more
targeted at managing worker pools where communication is needed and
there might be larger pools of tuples, but communication itself is
only a small amount of the overall work. Think "workers for compute-heavy
stuff that should make use of multicore machines with collecting
intermediate results on a central blackboard".

If you look for an actor package where you have tons of parallel (or
pseudo-parallel) work that wants to communicate with loads of messages,
better look for something else. This uses heavyweight system processes
and a comparatively heavyweight communication channel.

Values are matched with equality, so you can only pattern match with
values that actually define the equality functionality. And yes, if your
equality functionality takes lots of resources, this will blow your tuple
space matching. Best to only match on primary data types. Non-matched
parts of tuples can of course carry anything that can be pickled. But
be aware that every tuple is unpickled in the receiving process, so if
your unpickling takes lots of resources, again you won't be happy. Keep
your tuple simple and use them for coordination, massive data is best
kept in a database that is shared in all processes.

Since version 0.2 there are functional patterns - you can specify a
callable on your interest and it will match by being called on the
respective column of the tuples, so you can construct more complex
matches that way.

Additionally lindypy keeps all data in memory (allthough it's base could
maybe one day hooked to different backends and then use for example
sqlite or some other database for persistent tuple spaces), so for now
the memory is the limit - if you expect millions of tuples in the tuple
space, maybe something else might be better for now.

How to use it
--------------

Importing things is simple, just grab anything from lindypy:

>>> from lindypy import *

Your workers are just normal callables, in the simplest case they
are just functions written on global level (you can't use closures,
as they are not pickleable - the manager for the tuplespace lives
in a different process, though). So lets define a worker that waits
for any 4-item tuple and creates the sum of them and writes them
out as a tuple with first item "sum".

>>> def worker(ts):
>>>     while True:
>>>         t = ts.inp((object, object, object, object))
>>>         time.sleep(1.0) # this pretends some complex calculation
>>>         s = ts.inp(('sum', object))
>>>         ts.out(('sum', s[1]+sum(t)))

Now we need to start a tuple space, start some workers. We
need to seed the sum tuple, too.

>>> ts = tuplespace()
>>> ts.out(('sum', 0))
>>> for i in range(5):
>>>     ts.eval(worker)

Lets throw some tuples into the tuplespace:

>>> ts.out((1,2,3,4))
>>> ts.out((4,5,6,7))
>>> ts.out((3,4,5,2))

Now grab the resulting sum:

>>> print ts.inp(('sum', object))

Now we try to read something, but the tuple space is empty,
so we will either block forever or - in this case - get a
timeout exception:

>>> try:
>>>    with timeout(5):
>>>        ts.inp(('sum', object))
>>> except TimeoutError:
>>>    print "no more sums"

And now stop the tuplespace and kill the workers:

>>> ts.shutdown()

Additionally the return value of tuplespace() can be used in
a with statement as a context manager, too. That makes lots
of code easier to read and you don't need to handle the
shutdown yourself. Take a look at the provided example_script.py
for a much more idiomatic way to work with a tuplespace.

