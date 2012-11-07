import os
import sys
import fnmatch
import subprocess


def getsyspath(path):
    return path.replace('/', os.sep)


def get_executable_suffix():
    return os.path.splitext(sys.executable)[1]


sphinx = ARGUMENTS.get('SPHINX', 'sphinx-build')
sphinx_flags = ARGUMENTS.get('SPHINX_FLAGS', '-Nq')
sphinx_builder = ARGUMENTS.get('SPHINX_BUILDER', 'html')
built_doc_dir = ARGUMENTS.get('BUILT_DOC_DIR', getsyspath('build/docs'))

sphinx_cmd = '%s %s -b %s %s %s $SOURCE' % (sphinx, sphinx_flags, sphinx_builder, getsyspath('doc/source'), '/'.join([built_doc_dir, sphinx_builder]))
sphinx = Builder(action = sphinx_cmd, src_suffix = '.rst', suffix = '.html')

pytest = ARGUMENTS.get('PY_TEST', 'py.test')
pytest_flags = ARGUMENTS.get('PY_TEST_FLAGS', '-q')
pytest_cmd = '%s %s' % (pytest, pytest_flags)

vars = Variables('build-setup.conf', ARGUMENTS)
vars.Add('PYINSTALLER_DIR', '', 'pyinstaller-1.5.1')
vars.Add('PYINSTALLER_CONFIGURE', '', 'Configure.py')
vars.Add('PYINSTALLER_MAKESPEC', '', 'Makespec.py')
vars.Add('PYINSTALLER_BUILD', '', 'Build.py')

env = Environment()


def RunPyInstaller(target, source, env):

    python_executable = sys.executable
    pyinstaller = os.path.join(env['PYINSTALLER_DIR'], env['PYINSTALLER_BUILD'])
    spec_file = str(source[0])
    options = ('-y -o %s' % (getsyspath('build/bin-temp/TARGET_PLATFORM/SPECNAME'))).split()

    pyinstaller_status = subprocess.call([python_executable, pyinstaller] +
                                         options +
                                         [spec_file])

    return pyinstaller_status


env.Append(BUILDERS = {'Sphinx' : sphinx,
                       'PyInstaller' : Builder(action = RunPyInstaller)})
vars.Update(env)


def CheckPyModule(context, module):

    context.Message('Checking for Python module %s...' % module)

    result = True

    try:
        __import__(module)
    except ImportError:
        result = False

    context.Result(result)
    return result


def CheckPyInstaller(context):

    context.Message('Checking for PyInstaller...')

    result = False

    pyinstaller_directory = find_pyinstaller()
    if pyinstaller_directory is not None:

        env['PYINSTALLER_DIR'] = pyinstaller_directory
        result = True

    context.Result(result)
    return result


def find_pyinstaller():

    directories = os.listdir(os.curdir)

    for directory in directories:

        if os.path.isdir(directory) is False:
            continue

        if fnmatch.fnmatch(directory, 'pyinstaller-1.[56].[012]'):
            return directory

    return None


conf = Configure(env, custom_tests = {'CheckPyModule' : CheckPyModule,
                                      'CheckPyInstaller' : CheckPyInstaller})

def configure():

    EnsurePythonVersion(2, 6)

    if not conf.CheckPyModule('panda3d'):

        print 'Could not find Panda3D!'
        Exit(1)

    if not conf.CheckPyModule('lupa'):

        print 'Could not find Lupa!'
        Exit(1)

    if not conf.CheckPyInstaller():

        print 'Could not find PyInstaller!'
        Exit(1)

    print 'Configuration finished successfully!'
    vars.Save('build-setup.conf', env)
    Exit(0)


def RecursiveGlob(startdir, pattern):

    files = Glob(startdir + pattern)

    if files:
        files += RecursiveGlob(startdir, '*/' + pattern)

    return files


Help("""
Type 'scons configure' followed by 'scons build' to build OpenBlox.

Command-line arguments:

    * SPHINX - specifies the path to the Sphinx executable (optional; normally found automatically)
    * SPHINX_FLAGS - specifies what flags to pass to Sphinx. The default flags are "-Nq"
    * SPHINX_BUILDER - specifies which Sphinx builder (valid values are "html" and "text") to use for building OpenBlox's documentation
    * BUILT_DOC_DIR - specifies the output directory for OpenBlox's documentation
    * PY_TEST - specifies the location of the py.test executable (optional; normally found automatically)
    * PY_TEST_FLAGS - specifies what flags to pass to py.test. The default flags are "-q"
    
Build targets:

    * configure - configures the build system
    * build - builds a set of standalone OpenBlox binaries
    * docs - builds OpenBlox's documentation in HTML or text form
    * test - runs OpenBlox's unit test suite
    
Configuration variables:
""" + vars.GenerateHelpText(env))

sphinx_builder_conv = {
'html' : '.html',
'text' : '.txt'
}

for node in RecursiveGlob(getsyspath('doc/source/'), '*.rst'):

    target = str(node).replace('.rst', sphinx_builder_conv[sphinx_builder]).replace(getsyspath('doc/source'), '/'.join([built_doc_dir, sphinx_builder]))
    builder = env.Sphinx(target, node)

    env.Alias('docs', builder)
    env.Alias(getsyspath('build/docs'), builder)
    Clean(builder, getsyspath('build/docs/'))


if 'configure' in COMMAND_LINE_TARGETS:

    configure()
    env.Ignore('configure', None)


Tool('distzip')(env)

env.Append(
    DISTZIP_EXCLUDEEXTS = ['.pyc']
)

docs_zip = env.DistZip(getsyspath('build/dist/docs/OpenBlox Documentation.zip'), env.Dir(getsyspath('build/docs')))
runtime_zip = env.DistZip(getsyspath('build/obruntime.zip'), env.Dir('obengine'))
env.Alias('distdoc', docs_zip)
env.Alias('runtime', runtime_zip)
Depends('distdoc', 'docs')
Clean(zip, getsyspath('build/dist/docs'))

env.Alias('test', env.Command('py.test', 'pytest.ini', pytest_cmd))

env.Alias('build', env.PyInstaller(getsyspath('build/bin/obplay/obplay') + get_executable_suffix(),
                                   getsyspath('build-scripts/obplay.spec')))
