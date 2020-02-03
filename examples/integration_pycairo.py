"""Using pycairo with moderngl"""
import math

import cairo
from moderngl_window import geometry
from ported._example import Example


class CairoExample(Example):
    title = "Cairo Integration"
    aspect_ratio = 1.0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.texture = self.render_cairo_to_texture(512, 512)
        self.quad_fs = geometry.quad_fs()
        self.prog = self.ctx.program(
            vertex_shader="""
            #version 330
            in vec3 in_position;
            in vec2 in_texcoord_0;
            out vec2 uv;
            void main() {
                gl_Position = vec4(in_position, 1.0);
                uv = in_texcoord_0;
            }
            """,
            fragment_shader="""
            #version 330
            uniform sampler2D texture0;
            in vec2 uv;
            out vec4 outColor;
            void main() {
                outColor = texture(texture0, uv);
            }
            """,
        )

    def render(self, time, frame_time):
        self.texture.use(location=0)
        self.quad_fs.render(self.prog)

    def render_cairo_to_texture(self, width, height):
        # Draw with cairo to surface
        x, y, radius = (250, 250, 200)
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(surface)
        ctx.set_line_width(15)
        ctx.arc(x, y, radius, 0, 2.0 * math.pi)
        ctx.set_source_rgb(0.8, 0.8, 0.8)
        ctx.fill_preserve()
        ctx.set_source_rgb(1, 1, 1)
        ctx.stroke()
        # Copy surface to texture
        return self.ctx.texture((width, height), 4, data=surface.get_data())


if __name__ == "__main__":
    CairoExample.run()
