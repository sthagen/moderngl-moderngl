import time

import moderngl
import pyprojector

wnd = pyprojector.window((1280, 720))
ctx = moderngl.context()

prog = ctx.program(
    vertex_shader='''
        #version 330

        in vec2 in_vert;

        void main() {
            gl_Position = vec4(in_vert, 0.0, 1.0);
            gl_Position.y *= -1.0;
        }
    ''',
    fragment_shader='''
        #version 330

        out vec4 f_color;

        void main() {
            f_color = vec4(0.3, 0.5, 1.0, 1.0);
        }
    ''',
)

vertex_data = moderngl.pack([
    0.0, 0.8,
    -0.6, -0.8,
    0.6, -0.8,
])

vbo = ctx.buffer(vertex_data)
vao = ctx.vertex_array(prog, [
    vbo.bind('in_vert'),
])

size = (1280, 720)
fbo = ctx.framebuffer(ctx.renderbuffer(size, 3))
vao.scope = ctx.scope(framebuffer=fbo)

while True:
    fbo.clear((1.0, 1.0, 1.0))
    vao.render()
    wnd.update(fbo.glo)
    time.sleep(1.0)