import struct
import pytest
import moderngl

v_types = [
    {
        'version': 330,
        'type': 'int',
        'input': [-1],
        'output': [-2],
    },
    {
        'version': 330,
        'type': 'ivec2',
        'input': [-1, -1],
        'output': [-2, -2],
    },
    {
        'version': 330,
        'type': 'ivec3',
        'input': [-1, -1, -1],
        'output': [-2, -2, -2],
    },
    {
        'version': 330,
        'type': 'ivec4',
        'input': [-1, -1, -1, -1],
        'output': [-2, -2, -2, -2],
    },
    {
        'version': 330,
        'type': 'uint',
        'input': [1],
        'output': [2],
    },
    {
        'version': 330,
        'type': 'uvec2',
        'input': [1, 1],
        'output': [2, 2],
    },
    {
        'version': 330,
        'type': 'uvec3',
        'input': [1, 1, 1],
        'output': [2, 2, 2],
    },
    {
        'version': 330,
        'type': 'uvec4',
        'input': [1, 1, 1, 1],
        'output': [2, 2, 2, 2],
    },
    {
        'version': 330,
        'type': 'float',
        'input': [1.0],
        'output': [2.0],
    },
    {
        'version': 330,
        'type': 'vec2',
        'input': [1.0, 1.0],
        'output': [2.0, 2.0],
    },
    {
        'version': 330,
        'type': 'vec3',
        'input': [1.0, 1.0, 1.0],
        'output': [2.0, 2.0, 2.0],
    },
    {
        'version': 330,
        'type': 'vec4',
        'input': [1.0, 1.0, 1.0, 1.0],
        'output': [2.0, 2.0, 2.0, 2.0],
    },
    {
        'version': 330,
        'type': 'mat2',
        'input': [1.0, 1.0, 1.0, 1.0],
        'output': [2.0, 2.0, 2.0, 2.0],
    },
    {
        'version': 330,
        'type': 'mat2x3',
        'input': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        'output': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
    },
    {
        'version': 330,
        'type': 'mat2x4',
        'input': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        'output': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
    },
    {
        'version': 330,
        'type': 'mat3x2',
        'input': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        'output': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
    },
    {
        'version': 330,
        'type': 'mat3',
        'input': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        'output': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
    },
    {
        'version': 330,
        'type': 'mat3x4',
        'input': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        'output': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
    },
    {
        'version': 330,
        'type': 'mat4x2',
        'input': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        'output': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
    },
    {
        'version': 330,
        'type': 'mat4x3',
        'input': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        'output': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
    },
    {
        'version': 330,
        'type': 'mat4',
        'input': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        'output': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
    },
]


@pytest.mark.parametrize('v_type', v_types)
def test_simple(ctx, v_type):
    vert_src = '''
        #version %(version)s

        in %(type)s v_in;
        out %(type)s v_out;

        void main() {
            v_out = v_in + v_in;
        }
    '''

    if ctx.version_code < v_type['version']:
        pytest.skip('skipping version %s' % v_type['version'])

    prog = ctx.program(vertex_shader=vert_src % v_type, varyings=['v_out'])

    if prog.get('v_in', None) is None:
        pytest.skip('skipping %s' % v_type['type'])

    fmt = moderngl.detect_format(prog, ['v_in'], mode='struct')
    vbo1 = ctx.buffer(struct.pack(fmt, *v_type['input']))
    vbo2 = ctx.buffer(b'\xAA' * struct.calcsize(fmt))
    vao = ctx.simple_vertex_array(prog, vbo1, 'v_in')
    vao.transform(vbo2, moderngl.POINTS, 1)

    for a, b in zip(struct.unpack(fmt, vbo2.read()), v_type['output']):
        assert pytest.approx(a) == b


@pytest.mark.parametrize('v_type', v_types)
def test_arrays(ctx, v_type):
    vert_src = '''
        #version %(version)s

        in %(type)s v_in[2];
        out %(type)s v_out[2];

        void main() {
            v_out[0] = v_in[0] + v_in[0];
            v_out[1] = v_in[1] + v_in[1];
        }
    '''

    if ctx.version_code < v_type['version']:
        pytest.skip('skipping version %s' % v_type['version'])

    prog = ctx.program(vertex_shader=vert_src % v_type, varyings=['v_out'])

    if prog.get('v_in', None) is None:
        pytest.skip('skipping %s' % v_type['type'])

    fmt = moderngl.detect_format(prog, ['v_in'], mode='struct')
    vbo1 = ctx.buffer(struct.pack(fmt, *(v_type['input'] * 2)))
    vbo2 = ctx.buffer(b'\xAA' * struct.calcsize(fmt))
    vao = ctx.simple_vertex_array(prog, vbo1, 'v_in')
    vao.transform(vbo2, moderngl.POINTS, 1)

    for a, b in zip(struct.unpack(fmt, vbo2.read()), v_type['output'] * 2):
        assert pytest.approx(a) == b
