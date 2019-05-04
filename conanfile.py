from conans import ConanFile, tools
import os


class JavaInstallerConan(ConanFile):
    name = "java_installer"
    version = "8.0.144"
    url = "https://github.com/bincrafters/conan-java_installer"
    description = "Java installer distributed via Conan"
    license = "https://www.azul.com/products/zulu-and-zulu-enterprise/zulu-terms-of-use/"
    settings = "os", "arch", "os_build", "arch_build"
    options = {"jni": [True, False]}
    default_options = "jni=False"

    @property
    def jni_folder(self):
        folder = {"Linux": "linux", "Macos": "darwin", "Windows": "win32"}.get(self.settings.os_build)
        return os.path.join("include", folder)

    @property
    def is_cross_build(self):
        return self.settings.arch_build != self.settings.arch or self.settings.os_build != self.settings.os
    
    @property
    def c_arch(self):
        if self.is_cross_build:
            return self.settings.arch_build
        return self.settings.arch
    
    @property
    def c_os(self):
        if self.is_cross_build:
            return self.settings.os_build
        return self.settings.os

    def config_options(self):
        if self.c_arch != "x86_64":
            raise Exception("Unsupported Architecture.  This package currently only supports x86_64.")
        if self.c_os not in ["Windows", "Macos", "Linux"]:
            raise Exception("Unsupported System. This package currently only support Linux/Darwin/Windows")

    def build(self):
        source_file = "zulu8.23.0.3-jdk{0}-{1}_x64"

        if self.c_os == "Windows":
            source_file = source_file.format(self.version, "win")
            ext = "zip"
            checksum = "85044428c21350a1c2b1aa93d3002c8f"
        elif self.c_os == "Linux":
            source_file = source_file.format(self.version, "linux")
            ext = "tar.gz"
            checksum = "6ecd67688407b9f7e45c2736f003398b"
        elif self.c_os == "Macos":
            source_file = source_file.format(self.version, "macosx")
            ext = "tar.gz"
            checksum = "a82e78c9cd32deade2d6b44c2bdea133"

        bin_filename = "{0}.{1}".format(source_file, ext)
        download_url = "http://cdn.azul.com/zulu/bin/{0}".format(bin_filename)
        self.output.info("Downloading : {0}".format(download_url))
        tools.get(download_url, md5=checksum)
        os.rename(source_file, "sources")

    def package(self):
        self.copy(pattern="*", dst=".", src="sources")
        
    def package_id(self):
        self.info.settings.os = self.c_os
        self.info.settings.arch = self.c_arch
        self.info.discard_build_settings()

    def package_info(self):

        if self.options.jni:
            self.cpp_info.includedirs.append(self.jni_folder)
        else:
            self.cpp_info.includedirs = []
            self.cpp_info.libdirs = []
            self.cpp_info.resdirs = []
            self.cpp_info.bindirs = []

        java_home = os.path.join(self.package_folder)
        bin_path = os.path.join(java_home, "bin")

        self.output.info("Creating JAVA_HOME environment variable with : {0}".format(java_home))
        self.env_info.JAVA_HOME = java_home
        
        self.output.info("Appending PATH environment variable with : {0}".format(bin_path))
        self.env_info.path.append(bin_path)
        
