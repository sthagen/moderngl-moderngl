"""
Compute shader renders a 32 x 32 grid to a 512, 512 texture
"""
import moderngl as mgl
from ported._example import Example
from moderngl_window import geometry


class RenderTextureCompute(Example):
    title = "Render Texture Using Compute Shader"
    gl_version = (4, 3)
    aspect_ratio = 1.0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # reference compute shader: http://wili.cc/blog/opengl-cs.html
        self.compute = self.ctx.compute_shader('''
            #version 430

            layout (local_size_x = 16, local_size_y = 16) in;
            layout(rg32f, location=0) writeonly uniform image2D destTex;

            uniform float time;

            void main() {
                ivec2 ij = ivec2(gl_GlobalInvocationID.xy);
                float localCoef = length(vec2(ivec2(gl_LocalInvocationID.xy) - 8) / 8.0);
                float globalCoef = sin(float(gl_WorkGroupID.x+gl_WorkGroupID.y) * 0.1 + time) * 0.5;
                imageStore(destTex, ij, vec4(1.0 - globalCoef * localCoef, 0.0, 0.0, 0.0));
            }
        ''')
        self.compute['destTex'] = 0

        # For rendering a simple textured quad
        self.quad_program = self.ctx.program(
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
            out vec4 fragColor;
            in vec2 uv;

            void main() {
                fragColor = texture(texture0, uv);
            }
            """,
        )

        # GL_R32F texture
        self.texture = self.ctx.texture((256, 256), 1, dtype='f4')
        self.texture.filter = mgl.LINEAR, mgl.LINEAR
        self.quad_fs = geometry.quad_fs()

    def render(self, time, frame_time):
        self.ctx.clear(0.3, 0.3, 0.3)

        w, h = self.texture.size
        gw, gh = 16, 16
        nx, ny, nz = int(w/gw), int(h/gh), 1

        self.compute['time'] = time
        # Automatically binds as a GL_R32F / r32f (read from the texture)
        self.texture.bind_to_image(0, read=False, write=True)
        self.compute.run(nx, ny, nz)

        # Render texture
        self.texture.use(location=0)
        self.quad_fs.render(self.quad_program)


if __name__ == '__main__':
    RenderTextureCompute.run()
