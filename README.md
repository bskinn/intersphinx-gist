# Link-check for `intersphinx_mappings` gist

In 2016, I was trying to get
[`intersphinx`](https://www.sphinx-doc.org/en/master/usage/quickstart.html?highlight=intersphinx#intersphinx)
to work, and tossed a handful of
[`intersphinx_mapping`](https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#confval-intersphinx_mapping)
entries into a [Gist](https://gist.github.com/bskinn/0e164963428d4b51017cebdb6cda5209), for future reference.

Fast-forward to 2021, when I have [pointed out to me](https://gist.github.com/bskinn/0e164963428d4b51017cebdb6cda5209#gistcomment-3633740)
that this Gist shows up quite high in Google search results for things like
"[`matplotlib intersphinx`](https://www.google.com/search?q=matplotlib+intersphinx&oq=matplotlib+intersphinx)" and
"[`numpy intersphinx`](https://www.google.com/search?q=numpy+intersphinx&oq=numpy+intersphinx)."

Soooo, I figured it probably would be a good idea to curate the Gist a bit more carefully.
This repo houses a Github Action that runs a small pytest suite, which checks that:

 1. The docs root links all point to live sites, and

 2. The `objects.inv` locations defined by the mappings point to valid inventory files,
    as checked by [`sphobjinv`](https://github.com/bskinn/sphobjinv).

The log file from the most recent workflow execution lives
[here](https://github.com/bskinn/intersphinx-gist/blob/master/gist-check.log).


----

FWIW, if anyone reading this is having any trouble with the mappings in the Gist,
feel free to open an issue here and I'll be glad to help if I can.


----

Copyright (c) Brian Skinn 2021

License: The MIT License. See [`LICENSE.txt`](https://github.com/bskinn/intersphinx-gist/blob/master/LICENSE.txt)
for full license terms.
