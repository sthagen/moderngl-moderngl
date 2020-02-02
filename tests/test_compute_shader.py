import struct
import unittest

from common import get_context


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ctx = get_context(require=430)
        if not cls.ctx:
            raise unittest.SkipTest('compute shaders not supported')

    def test_1(self):
        compute_shader = self.ctx.compute_shader('''
            #version 430

            layout (local_size_x = 1, local_size_y = 1) in;

            layout (std430, binding = 1) buffer Input {
                float v1[4];
            };

            layout (std430, binding = 2) buffer Output {
                float v2[4];
            };

            void main() {
                v2[0] = v1[3];
                v2[1] = v1[2];
                v2[2] = v1[1];
                v2[3] = v1[0];
            }
        ''')

        buf1 = self.ctx.buffer(struct.pack('4f', 1.0, 2.0, 3.0, 4.0))
        buf2 = self.ctx.buffer(struct.pack('4f', 0.0, 0.0, 0.0, 0.0))

        buf1.bind_to_storage_buffer(1)
        buf2.bind_to_storage_buffer(2)

        compute_shader.run()

        a, b, c, d = struct.unpack('4f', buf2.read())

        self.assertAlmostEqual(a, 4.0)
        self.assertAlmostEqual(b, 3.0)
        self.assertAlmostEqual(c, 2.0)
        self.assertAlmostEqual(d, 1.0)

    def test_image(self):
        texture = self.ctx.texture((100, 100), 4)
        texture.bind_to_image(0, read=True, write=True)
        self.assertEqual(self.ctx.error, 'GL_NO_ERROR')
        texture.release()

    def test_image_float(self):
        texture = self.ctx.texture((100, 100), 4, dtype='f4')
        texture.bind_to_image(0, read=True, write=True)
        self.assertEqual(self.ctx.error, 'GL_NO_ERROR')
        texture.release()

    def test_image_wrong_format(self):
        texture = self.ctx.texture((100, 100), 4)
        texture.bind_to_image(0, read=True, write=True, format=13371337)
        self.assertEqual(self.ctx.error, 'GL_INVALID_VALUE')
        texture.release()


if __name__ == '__main__':
    unittest.main()
