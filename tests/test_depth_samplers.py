"""

"""
import numpy as np
import moderngl
import moderngl as mgl
from scipy import ndimage


def _build_fbo_with_rasterised_triangle(ctx, prog, vbo, size=(4, 4), 
                                        depth_clear=1.0):
    """

    :param ctx:
    :param prog:
    :param vbo:
    :param size:
    :return:
    """
    tex_depth = ctx.depth_texture(size)  # implicit -> dtype='f4', components=1
    fbo_depth = ctx.framebuffer(depth_attachment=tex_depth)
    fbo_depth.use()
    fbo_depth.clear(depth=depth_clear)

    # vertex array object of triangle with depth pass prog
    vao_triangle = ctx.simple_vertex_array(prog, vbo, 'in_vert')
    # Now we render a triangle in there
    vao_triangle.render()

    return fbo_depth, tex_depth


def test_depth_sampler(standalone_context, prog_render_depth_pass, 
                       prog_draw_depth, vbo_triangle, vbo_quad):
    """

    :param standalone_context:
    :param prog_render_depth_pass:
    :param prog_draw_depth:
    :param vbo_triangle:
    :param vbo_quad:
    :return:
    """
    ctx = standalone_context
    ctx.enable(mgl.DEPTH_TEST)

    size = (16,) * 2
    fbo_depth, tex_depth = _build_fbo_with_rasterised_triangle(ctx, prog_render_depth_pass, vbo_triangle, size)

    ############################################################################
    # EXPECTED DATAS                                                                                                   #
    # It should have 0.5's where the triangle lies.                                                                    #
    ############################################################################
    depth_from_dbo = np.frombuffer(tex_depth.read(), dtype=np.dtype('f4')).reshape(size[::-1])
    depth_value_from_triangle_vertices = 0.0
    # Map [-1, +1] -> [0, 1]
    depth_value_in_depthbuffer = (depth_value_from_triangle_vertices + 1) * 0.5
    np_triangle_raster = np.array(
        [
            [depth_value_in_depthbuffer] * (size[0] - (j + 1)) + [1.0] * (j + 1)
            for j in range(size[1])
        ]
    )
    ############################################################################

    depth_tex_filter = (moderngl.NEAREST, moderngl.NEAREST)
    compare_func = ''

    def _do_test():
        # some stuff should be 1s and 0.5 where the triangle lies.
        np.testing.assert_array_almost_equal(depth_from_dbo, np_triangle_raster)

        fbo_draw_depth = ctx.framebuffer(color_attachments=[ctx.renderbuffer(size, components=1, dtype='f4')])
        fbo_draw_depth.use()

        tex_depth.use(location=0)

        # vertex array object of (fullscreen) quad with render depth prog
        vao_quad = ctx.simple_vertex_array(prog_draw_depth, vbo_quad, 'in_vert')
        vao_quad.render(moderngl.TRIANGLE_STRIP)

        data = np.frombuffer(fbo_draw_depth.read(components=1, dtype='f4'), dtype=np.dtype('f4')).reshape(size[::-1])
        np.testing.assert_array_almost_equal(data, np_triangle_raster)

    def _with_sampler():
        # from: https://github.com/Contraz/demosys-py/blob/master/demosys/opengl/texture.py
        depth_sampler = ctx.sampler(filter=depth_tex_filter, compare_func=compare_func)  # disable depth func
        depth_sampler.use(location=0)
        _do_test()

    def _with_texture_parameters():
        tex_depth.filter = depth_tex_filter
        tex_depth.compare_func = compare_func
        _do_test()

    _with_sampler()
    _with_texture_parameters()


def test_sampler_shadow(standalone_context, prog_render_depth_pass, prog_shadow_test, vbo_triangle, vbo_quad):
    """

    :param standalone_context:
    :param prog_render_depth_pass:
    :param prog_shadow_test:
    :param vbo_triangle:
    :param vbo_quad:
    :return:
    """
    ctx = standalone_context
    ctx.enable(mgl.DEPTH_TEST)

    size = (3,) * 2
    fbo_depth, tex_depth = _build_fbo_with_rasterised_triangle(ctx, prog_render_depth_pass, vbo_triangle, size)

    ############################################################################
    # EXPECTED DATAS                                                                                                   #
    # It should have 1's where the triangle lies.                                                                      #
    ############################################################################
    texel_shadowed = 1
    np_triangle_raster_visbility = np.array(
        [
            [texel_shadowed] * (size[0] - (j + 1)) + [1 - texel_shadowed] * (j + 1)
            for j in range(size[1])
        ]
    )
    ############################################################################

    # No offset - fetch the center pixel (NEAREST)
    prog_shadow_test['u_shadow_coord_offset'].value = (0,) * 2

    depth_tex_filter = (moderngl.NEAREST, moderngl.NEAREST)
    compare_func = '>='

    def _do_test():
        fbo_draw_depth = ctx.framebuffer(color_attachments=[ctx.renderbuffer(size, components=1, dtype='f4')])
        fbo_draw_depth.use()

        tex_depth.use(location=0)

        # https://www.khronos.org/opengl/wiki/Sampler_(GLSL)#Shadow_samplers
        vao_fs_shadow = ctx.simple_vertex_array(prog_shadow_test, vbo_quad, 'in_vert')
        vao_fs_shadow.render(moderngl.TRIANGLE_STRIP)

        data = np.frombuffer(fbo_draw_depth.read(components=1, dtype='f4'), dtype=np.dtype('f4')).reshape(size[::-1])
        np.testing.assert_array_almost_equal(data, np_triangle_raster_visbility)

    def _with_sampler():
        # https://github.com/Contraz/demosys-py/blob/01f285cd3a132012e14a51bf0ae9d7aa5a489b55/demosys/opengl/texture.py#L151
        shadow_sampler = ctx.sampler(filter=depth_tex_filter, compare_func=compare_func)  # enable depth func
        shadow_sampler.use(location=0)
        _do_test()

    def _with_texture_paramters():
        tex_depth.filter = depth_tex_filter
        tex_depth.compare_func = compare_func
        _do_test()

    _with_sampler()
    _with_texture_paramters()


def test_sampler_shadow_with_bilinear_interpolation(
        standalone_context,
        prog_render_depth_pass,
        prog_shadow_test,
        vbo_triangle,
        vbo_quad
):
    """

    :param standalone_context:
    :param prog_render_depth_pass:
    :param prog_shadow_test:
    :param vbo_triangle:
    :param vbo_quad:
    :return:
    """
    ctx = standalone_context
    ctx.enable(mgl.DEPTH_TEST)

    size = (7,) * 2

    fbo_depth, tex_depth = _build_fbo_with_rasterised_triangle(ctx, prog_render_depth_pass, vbo_triangle, size)

    ############################################################################
    # EXPECTED DATAS                                                           #
    ############################################################################
    # Box filter (2x2) on triangle visibility rasterisation
    # is similar to bilinear interpolation with samplerShadow
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.uniform_filter.html#scipy.ndimage.uniform_filter
    np_triangle_raster_visbility = np.array(
        [
            [1.0] * (size[0] - (j + 1)) + [0.0] * (j + 1)
            for j in range(size[1])
        ]
    )
    box_filter_on_triangle_raster_visibility = ndimage.uniform_filter(
        np_triangle_raster_visbility,
        size=2, mode='constant', cval=0, origin=-1)
    ############################################################################

    half_pixel_size = (1.0/size[0]*0.5, 1.0/size[1]*0.5)
    prog_shadow_test['u_shadow_coord_offset'].value = tuple(half_pixel_size)

    def _do_test():
        fbo_draw_depth = ctx.framebuffer(
            color_attachments=[ctx.renderbuffer(size,
                                                components=1, dtype='f4')])
        fbo_draw_depth.use()

        tex_depth.use(location=0)

        # https://www.khronos.org/opengl/wiki/Sampler_(GLSL)#Shadow_samplers
        vao_fs_shadow = ctx.simple_vertex_array(prog_shadow_test, vbo_quad,
                                                'in_vert')
        vao_fs_shadow.render(moderngl.TRIANGLE_STRIP)

        #
        data = np.frombuffer(fbo_draw_depth.read(components=1, dtype='f4'),
                             dtype=np.dtype('f4')).reshape(size[::-1])
        np.testing.assert_array_almost_equal(
            data, box_filter_on_triangle_raster_visibility)

    depth_tex_filter = (moderngl.LINEAR, moderngl.LINEAR)
    compare_func = '>='

    def _with_sampler():
        # https://github.com/Contraz/demosys-py/blob/01f285cd3a132012e14a51bf0ae9d7aa5a489b55/demosys/opengl/texture.py#L151
        shadow_sampler = ctx.sampler(
            filter=depth_tex_filter,
            compare_func=compare_func,  # enable depth func
            # from context.py:
            #   border_color (tuple): The (r, g, b, a) color for the texture border.
            #   When this value is set the ``repeat_`` values are overriden
            #   setting the texture wrap to return the border color when outside ``[0, 1]`` range.
            # border_color=(0, 0, 0, 0),    # seems not to work well ...
            repeat_x=False, repeat_y=False,
        )
        shadow_sampler.use(location=0)
        _do_test()

    def _with_texture_paremeters():
        tex_depth.filter = depth_tex_filter
        tex_depth.compare_func = compare_func
        _do_test()

    _with_sampler()
    _with_texture_paremeters()
