Buffer
======

.. py:module:: moderngl
.. py:currentmodule:: moderngl

.. autoclass:: moderngl.Buffer

Create
------

.. automethod:: Context.buffer(data=None, reserve=0, dynamic=False) -> Buffer
    :noindex:

Methods
-------

.. automethod:: Buffer.assign(index)
.. automethod:: Buffer.bind(*attribs, layout=None)
.. automethod:: Buffer.write(data, offset=0)
.. automethod:: Buffer.write_chunks(data, start, step, count)
.. automethod:: Buffer.read(size=-1, offset=0) -> bytes
.. automethod:: Buffer.read_into(buffer, size=-1, offset=0, write_offset=0)
.. automethod:: Buffer.read_chunks(chunk_size, start, step, count) -> bytes
.. automethod:: Buffer.read_chunks_into(buffer, chunk_size, start, step, count, write_offset=0)
.. automethod:: Buffer.clear(size=-1, offset=0, chunk=None)
.. automethod:: Buffer.bind_to_uniform_block(binding=0, offset=0, size=-1)
.. automethod:: Buffer.bind_to_storage_buffer(binding=0, offset=0, size=-1)
.. automethod:: Buffer.orphan(size=-1)
.. automethod:: Buffer.release()


Attributes
----------

.. autoattribute:: Buffer.size
.. autoattribute:: Buffer.dynamic
.. autoattribute:: Buffer.glo
.. autoattribute:: Buffer.mglo
.. autoattribute:: Buffer.extra
.. autoattribute:: Buffer.ctx

.. toctree::
    :maxdepth: 2
