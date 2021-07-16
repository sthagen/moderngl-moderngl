VertexArray
===========

.. py:module:: moderngl
.. py:currentmodule:: moderngl

.. autoclass:: moderngl.VertexArray

    .. note::
        Compared to OpenGL, :py:class:`VertexArray` objects have some additional responsibilities:

        - Binding a :py:class:`Program` when :py:meth:`VertexArray.render` or :py:meth:`VertexArray.transform` is called.
        - Subroutines can be assigned. Please see the example below.

Create
------

.. automethod:: Context.simple_vertex_array(program, buffer, *attributes, index_buffer=None, index_element_size=4, mode=None) -> VertexArray
    :noindex:

.. automethod:: Context.vertex_array(*args, **kwargs) -> VertexArray
    :noindex:

Methods
-------

.. automethod:: VertexArray.render(mode=None, vertices=-1, first=0, instances=-1)
.. automethod:: VertexArray.render_indirect(buffer, mode=None, count=-1, first=0)
.. automethod:: VertexArray.transform(buffer, mode=None, vertices=-1, first=0, instances=-1, buffer_offset=0)
.. automethod:: VertexArray.bind(attribute, cls, buffer, fmt, offset=0, stride=0, divisor=0, normalize=False)
.. automethod:: VertexArray.release()

Attributes
----------

.. autoattribute:: VertexArray.mode
.. autoattribute:: VertexArray.program
.. autoattribute:: VertexArray.index_buffer
.. autoattribute:: VertexArray.index_element_size
.. autoattribute:: VertexArray.scope
.. autoattribute:: VertexArray.vertices
.. autoattribute:: VertexArray.instances
.. autoattribute:: VertexArray.subroutines
.. autoattribute:: VertexArray.glo
.. autoattribute:: VertexArray.mglo
.. autoattribute:: VertexArray.extra
.. autoattribute:: VertexArray.ctx

.. toctree::
    :maxdepth: 2
