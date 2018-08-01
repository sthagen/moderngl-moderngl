'''
    ModernGL: PyOpenGL alternative
'''

import os

if os.environ.get('READTHEDOCS') == 'True':
    import sys
    from .mock import mgl
    sys.modules['moderngl.mgl'] = mgl

from .buffer import *
from .compute_shader import *
from .conditional_render import *
from .context import *
from .framebuffer import *
from .mock import *
from .program import *
from .program_members import *
from .query import *
from .renderbuffer import *
from .scope import *
from .texture import *
from .texture_3d import *
from .texture_array import *
from .texture_cube import *
from .vertex_array import *
from .sampler import *

__version__ = '5.4.2'
