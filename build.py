from conan.packager import ConanMultiPackager
from subprocess import check_output
import os

if __name__ == "__main__":

    os.system("conan profile new ./ci-profile")
    if 'CONAN_BASE_PROFILE_OS' in os.environ:
        os.system("conan profile update settings.os=\"%s\" ./ci-profile" % os.environ['CONAN_BASE_PROFILE_OS'])

    if 'CONAN_BASE_PROFILE_OS_API' in os.environ:
        os.system("conan profile update settings.os.api_level=\"%s\" ./ci-profile" % os.environ['CONAN_BASE_PROFILE_OS_API'])

    if 'CONAN_BASE_PROFILE_OSBUILD' in os.environ:
        os.system("conan profile update settings.os_build=\"%s\" ./ci-profile" % os.environ['CONAN_BASE_PROFILE_OSBUILD'])

    if 'CONAN_BASE_PROFILE_ARCH' in os.environ:
        os.system("conan profile update settings.arch=\"%s\" ./ci-profile" % os.environ['CONAN_BASE_PROFILE_ARCH'])

    if 'CONAN_BASE_PROFILE_ARCHBUILD' in os.environ:
        os.system("conan profile update settings.arch_build=\"%s\" ./ci-profile" % os.environ['CONAN_BASE_PROFILE_ARCHBUILD'])

    if 'CONAN_BASE_PROFILE_COMPILER' in os.environ:
        os.system("conan profile update settings.compiler=\"%s\" ./ci-profile" % os.environ['CONAN_BASE_PROFILE_COMPILER'])

    if 'CONAN_BASE_PROFILE_COMPILER_VERSION' in os.environ:
        os.system("conan profile update settings.compiler.version=\"%s\" ./ci-profile" % os.environ['CONAN_BASE_PROFILE_COMPILER_VERSION'])

    if 'CONAN_BASE_PROFILE_COMPILER_LIBCXX' in os.environ:
        os.system("conan profile update settings.compiler.libcxx=\"%s\" ./ci-profile" % os.environ['CONAN_BASE_PROFILE_COMPILER_LIBCXX'])

    if 'CONAN_BASE_PROFILE_BUILDTYPE' in os.environ:
        os.system("conan profile update settings.build_type=\"%s\" ./ci-profile" % os.environ['CONAN_BASE_PROFILE_BUILDTYPE'])

    if 'CONAN_OPTIONS' in os.environ:
        for option in os.environ['CONAN_OPTIONS'].split(','):
            os.system("conan profile update options.%s ./ci-profile" % option)

    user_name = "user"
    user_channel = "testing"
    if 'CONAN_USERNAME' in os.environ:
        user_name = os.environ['CONAN_USERNAME']

    if 'CONAN_CHANNEL' in os.environ:
        user_channel = os.environ['CONAN_CHANNEL']
    
    builder = ConanMultiPackager()
    builder.add()
    builder.run(os.path.abspath("./ci-profile"))
