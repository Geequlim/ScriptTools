import SCons.Action
import SCons.Builder
import SCons.Util

__VALA_OBJECT_SUFFIX = ".vala.o"


class ToolValalWarning(SCons.Warnings.Warning):
    pass


class ValaCompilerNotFound(ToolValalWarning):
    pass

SCons.Warnings.enableWarningClass(ToolValalWarning)


def _detect(env):
    """ Try to detect the vala compiler """
    try:
        return env['valac']
    except KeyError:
        pass

    valac = env.WhereIs('valac')
    if valac:
        return valac

    raise SCons.Errors.StopError(ValaCompilerNotFound,
                                 "Could not detect Vala compiler")
    return None

#
# Builder emitters
#


def _object_emitter(target, source, env):
    vala_suffix = ".vala"
    target = []
    for s in source:
        vala_stem = str(s)
        if vala_stem.endswith(vala_suffix):
            vala_stem = vala_stem[:-len(vala_suffix)]
        vala_stem += __VALA_OBJECT_SUFFIX
        target.append(vala_stem)
    return target, source


def _csource_emitter(target, source, env):
    vala_suffix = ".vala"
    target = []
    for s in source:
        vala_stem = str(s)
        if vala_stem.endswith(vala_suffix):
            vala_stem = vala_stem[:-len(vala_suffix)]
        vala_stem += ".c"
        target.append(vala_stem)
    return target, source


def _libray_emitter(target, source, env):
    target = 'lib' + str(target[0])
    return target, source

#
# Vala Builders
#
_vala_object = SCons.Builder.Builder(
    action="$VALAC $VALAC_OPTIONS -c $SOURCES",
    suffix=__VALA_OBJECT_SUFFIX,
    src_suffix='vala',
    emitter=_object_emitter)

_vala_c_source = SCons.Builder.Builder(
    action="$VALAC $VALAC_OPTIONS -C $SOURCES",
    suffix='c',
    src_suffix='vala',
    emitter=_csource_emitter)

_vala_library = SCons.Builder.Builder(
    action="$VALAC --library=$TARGET $SOURCES  -X -fPIC -X -shared -o $TARGET $VALAC_OPTIONS",
    suffix='so',
    src_suffix='vala',
    emitter=_libray_emitter)

_valac = SCons.Builder.Builder(
    action="$VALAC $VALAC_OPTIONS $SOURCES -o $TARGET",
    suffix='',
    src_suffix='vala')


def generate(env):
    """Add Builders and construction variables to the Environment."""

    env['VALAC'] = _detect(env)
    env.SetDefault(VALAC_OPTIONS='')

    env['BUILDERS']['ValaObject'] = _vala_object
    env['BUILDERS']['ValaCSource'] = _vala_c_source
    env['BUILDERS']['ValaSharedLibrary'] = _vala_library
    env['BUILDERS']['Vala'] = _valac


def exists(env):
    return _detect(env)
