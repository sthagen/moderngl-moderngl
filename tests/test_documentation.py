import inspect
import os
import re
import unittest

import moderngl


class TestCase(unittest.TestCase):

    def validate(self, filename, classname, ignore, include=None):
        root = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.normpath(os.path.join(root, 'docs', 'reference', filename))) as f:
            docs = f.read()
        methods = re.findall(r'^\.\. automethod:: ([^\(\n]+)([^\n]+)', docs, flags=re.M)
        attributes = re.findall(r'^\.\. autoattribute:: ([^\n]+)', docs, flags=re.M)
        documented = set(filter(lambda x: x.startswith(classname), [a for a, b in methods] + attributes))
        implemented = set(classname + '.' + x for x in dir(getattr(moderngl, classname)) if not x.startswith('_'))
        include = set('{}.{}'.format(classname, e) for e in include or [])
        ignored = set(classname + '.' + x for x in ignore)
        self.assertSetEqual(implemented - documented - ignored, set(), msg='Implemented but not Documented')
        self.assertSetEqual(documented - implemented - include, set(), msg='Documented but not Implemented')

        attribute_access = re.compile(r"[a-zA-Z]\w*\.(\w+)")
        for method, docsig in methods:
            classname, methodname = method.split('.')
            sig = str(inspect.signature(getattr(getattr(moderngl, classname), methodname)))
            sig = sig.replace('self, ', '').replace(' -> None', '')
            for _ in range(2):
                sig = re.sub(attribute_access, r'\1', sig)
            sig = sig.replace('(self)', '()').replace(', *,', ',').replace('(*, ', '(')
            sig = re.sub(r'-> \'(\w+)\'', r'-> \1', sig)
            self.assertEqual(docsig, sig, msg=filename + '::' + method)

    def test_context_docs(self):
        self.validate('context.rst', 'Context', ['core_profile_check'], ['__enter__', '__exit__'])

    def test_program_docs(self):
        self.validate('program.rst', 'Program', [], ['__getitem__', '__setitem__', '__eq__', '__iter__'])

    def test_vertex_array_docs(self):
        self.validate('vertex_array.rst', 'VertexArray', [])

    def test_buffer_docs(self):
        self.validate('buffer.rst', 'Buffer', [])

    def test_texture_docs(self):
        self.validate('texture.rst', 'Texture', [])

    def test_texture_array_docs(self):
        self.validate('texture_array.rst', 'TextureArray', [])

    def test_texture3d_docs(self):
        self.validate('texture3d.rst', 'Texture3D', [])

    def test_texture_cube_docs(self):
        self.validate('texture_cube.rst', 'TextureCube', [])

    def test_framebuffer_docs(self):
        self.validate('framebuffer.rst', 'Framebuffer', [])

    def test_renderbuffer_docs(self):
        self.validate('renderbuffer.rst', 'Renderbuffer', [])

    def test_query_docs(self):
        self.validate('query.rst', 'Query', [])

    def test_scope_docs(self):
        self.validate('scope.rst', 'Scope', [])

    def test_compute_shader_docs(self):
        self.validate('compute_shader.rst', 'ComputeShader', [], ['__getitem__', '__setitem__', '__eq__', '__iter__'])

    def test_subroutine_docs(self):
        self.validate('subroutine.rst', 'Subroutine', [])

    def test_uniform_docs(self):
        self.validate('uniform.rst', 'Uniform', [])

    def test_uniform_block_docs(self):
        self.validate('uniform_block.rst', 'UniformBlock', [])

    def test_varying_docs(self):
        self.validate('varying.rst', 'Varying', [])

    def test_conditional_render_docs(self):
        self.validate('conditional_render.rst', 'ConditionalRender', [])

    def test_sampler_docs(self):
        self.validate('sampler.rst', 'Sampler', [])


if __name__ == '__main__':
    unittest.main()
