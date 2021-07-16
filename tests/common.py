import moderngl

# NOTE: According to the spec we need a framebuffer bound at all times
#       to not break tests. Making sure a context always has a framebuffer
#       bound ensures tests works across platforms.
# OpenGL 4.4 Core Specification - 9.4.4 Effects of Framebuffer Completeness on Framebuffer Operations
# 
# A GL_INVALID_FRAMEBUFFER_OPERATION error is generated by attempts to
# render to or read from a framebuffer which is not framebuffer complete.
# This error is generated regardless of whether fragments are actually
# read from or written to the framebuffer. For example, it is generated
# when a rendering command is called and the framebuffer is incomplete,
# even if GL_RASTERIZER_DISCARD is enabled.

# structure {
#     'context_330': {
#         'ctx': Context
#         'fbo': Framebuffer
#     },
# }
_static = {}


def get_context(require=330) -> moderngl.Context:
    """Gets a context, cache it and activate it"""
    key = 'context_{}'.format(require)

    entry = _static.get(key)

    if entry is None:
        try:
            ctx = moderngl.create_context(require=require, standalone=True)
            entry = {'ctx': ctx, 'fbo': ctx.simple_framebuffer((100, 100), 4)}
            _static[key] = entry
        except Exception as ex:
            print(ex)
            return None

    entry['fbo'].use()
    entry['fbo'].clear()
    entry['ctx'].__enter__()
    return entry['ctx']
 