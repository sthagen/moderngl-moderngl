# Demonstrate rendering primitives to different layers of a TextureArray using
# a layered framebuffer binding and a geometry shader to set `gl_Layer`.
# Displays many triangles, each from a different perspective. May not be the
# optimal way to perform this particular task, but it demonstrates and
# validates the functionality. Adapted from 03_camera.py .

# https://www.khronos.org/opengl/wiki/Framebuffer_Object#Layered_Images
# https://www.khronos.org/opengl/wiki/Geometry_Shader#Layered_rendering

import math
import os
import sys

import glm
import moderngl
import pygame

os.environ['SDL_WINDOWS_DPI_AWARENESS'] = 'permonitorv2'

WIN_DIM = 800
AXIS_INSTANCES = 8 # squared is total instances
INSTANCES = AXIS_INSTANCES**2

assert WIN_DIM % AXIS_INSTANCES == 0

pygame.init()
pygame.display.set_mode((WIN_DIM, WIN_DIM), flags=pygame.OPENGL | pygame.DOUBLEBUF, vsync=True)

class Scene:
    def __init__(self):
        self.ctx = moderngl.get_context()

        self.program = self.ctx.program(
            vertex_shader='''
                #version 330 core
            ''' + f"const int AXIS_INSTANCES = {AXIS_INSTANCES};" + '''

                // functions stolen from glm

                // RH, ZO
                mat4 perspective(float fovy, float aspect, float zNear, float zFar) {
                    float tanHalfFovy = tan(fovy / 2.0);

                    mat4 m = mat4(0.0);
                    m[0][0] = 1.0 / (aspect * tanHalfFovy);
                    m[1][1] = 1.0 / tanHalfFovy;
                    m[2][2] = - (zFar + zNear) / (zFar - zNear);
                    m[2][3] = -1.0;
                    m[3][2] = - (2.0 * zFar * zNear) / (zFar - zNear);

                    return m;
                }

                // RH
                mat4 lookAt(vec3 eye, vec3 center, vec3 up) {
                    vec3 f = normalize(center - eye);
                    vec3 s = normalize(cross(f, up));
                    vec3 u = cross(s, f);

                    mat4 m = mat4(1.0);
                    m[0][0] = s.x;
                    m[1][0] = s.y;
                    m[2][0] = s.z;
                    m[0][1] = u.x;
                    m[1][1] = u.y;
                    m[2][1] = u.z;
                    m[0][2] =-f.x;
                    m[1][2] =-f.y;
                    m[2][2] =-f.z;
                    m[3][0] =-dot(s, eye);
                    m[3][1] =-dot(u, eye);
                    m[3][2] = dot(f, eye);

                    return m;
                }

                vec3 vertices[3] = vec3[](
                    vec3(0.0, 0.4, 0.0),
                    vec3(-0.4, -0.3, 0.0),
                    vec3(0.4, -0.3, 0.0)
                );

                uniform float now;

                flat out int instance;
                out vec3 color_gs;

                void main() {
                    // illustrate now til 5 in the future across instances
                    float inow = now + 5*(float(gl_InstanceID) / (AXIS_INSTANCES*AXIS_INSTANCES));

                    mat4 proj = perspective(radians(60.0), 1.0, 0.1, 1000.0);
                    vec3 eye = vec3(cos(inow), sin(inow), 0.5);
                    mat4 look = lookAt(eye, vec3(0.0, 0.0, 0.0), vec3(0.0, 0.0, 1.0));

                    gl_Position = (proj * look) * vec4(vertices[gl_VertexID], 1.0);
                    instance = gl_InstanceID;

                    color_gs = vec3(float(gl_VertexID == 0),
                                    float(gl_VertexID == 1),
                                    float(gl_VertexID == 2));
                }
            ''',
            geometry_shader='''
                #version 330 core

                // one triangle in and out
                layout (triangles) in;
                layout (triangle_strip, max_vertices = 3) out;

                flat in int instance[3];
                in vec3 color_gs[3];

                out vec3 color_fs;

                void main() {
                    gl_Layer = instance[0]; // set triangle layer
                    for (int i=0; i<3; i++) {
                        // copy relevant vertex attributes
                        color_fs = color_gs[i];
                        gl_Position = gl_in[i].gl_Position;
                        EmitVertex();
                    }
                    EndPrimitive();
                }
            ''',
            fragment_shader='''
                #version 330 core

                in vec3 color_fs;

                layout (location = 0) out vec4 out_color;

                void main() {
                    out_color = vec4(color_fs, 1.0);
                }
            ''',
        )

        self.r_program = self.ctx.program(
            vertex_shader='''
                #version 330 core

                // full screen quad
                vec2 vertices[6] = vec2[](
                    vec2(-1, -1),
                    vec2( 1, -1),
                    vec2(-1,  1),

                    vec2(-1,  1),
                    vec2( 1, -1),
                    vec2( 1,  1)
                );

                void main() {
                    gl_Position = vec4(vertices[gl_VertexID], 1, 1);
                }
            ''',
            fragment_shader='''
                #version 330 core
            ''' + f"const int AXIS_INSTANCES = {AXIS_INSTANCES};" + '''
            ''' + f"const int WIN_DIM = {WIN_DIM};" + '''

                uniform sampler2DArray tex;

                out vec3 out_color;

                void main() {
                    int tile_size = WIN_DIM/AXIS_INSTANCES;
                    // gl_FragCoord is in pixel coordinates!
                    ivec2 coord = ivec2(gl_FragCoord.xy);
                    ivec2 tile = coord / tile_size;
                    ivec2 tile_coord = coord % tile_size;
                    int tile_idx = tile.y*AXIS_INSTANCES + tile.x;
                    ivec3 tex_coord = ivec3(tile_coord, tile_idx);

                    out_color = texelFetch(tex, tex_coord, 0).rgb;
                }
            ''',
        )

        # program to render triangle instances to different texture array layers
        self.vao = self.ctx.vertex_array(self.program, [])
        self.vao.vertices = 3

        # texture array containing render results
        tile_size = WIN_DIM//AXIS_INSTANCES
        self.tex = self.ctx.texture_array((tile_size, tile_size, INSTANCES), 3)
        # framebuffer used as render destination
        self.fb = self.ctx.framebuffer([self.tex])

        # program to render array to the screen showing each layer in a grid
        self.r_vao = self.ctx.vertex_array(self.r_program, [])
        self.r_vao.vertices = 6
        self.r_vao.mode = moderngl.TRIANGLES

    def render(self):
        # render scene to texture array
        self.fb.use()
        self.ctx.clear()
        self.program['now'] = pygame.time.get_ticks() / 1000.0
        self.vao.render(instances=INSTANCES) # one instance per layer in example

        # render texture array to screen
        self.ctx.screen.use()
        self.ctx.clear()
        self.tex.use()
        self.r_vao.render()


scene = Scene()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    scene.render()

    pygame.display.flip()
