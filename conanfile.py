from conans import ConanFile, tools, CMake
from conans.util import files
import os


class ZlibConan(ConanFile):
    name = 'zlib'
    version = '1.2.11'
    ZIP_FOLDER_NAME = 'zlib-%s' % version
    generators = 'cmake'
    settings = 'os', 'arch', 'compiler', 'build_type'
    options = {'shared': [True, False]}
    default_options = 'shared=False'
    exports_sources = ['CMakeLists.txt']
    url = 'http://github.com/henry4k/conan-zlib'
    license = 'http://www.zlib.net/zlib_license.html'
    description = 'A Massively Spiffy Yet Delicately Unobtrusive Compression Library ' \
                  '(Also Free, Not to Mention Unencumbered by Patents)'

    def source(self):
        z_name = 'zlib-%s.tar.gz' % self.version
        tools.download('https://zlib.net/zlib-%s.tar.gz' % self.version, z_name)
        tools.unzip(z_name)
        os.unlink(z_name)
        files.rmdir('%s/contrib' % self.ZIP_FOLDER_NAME)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        source_folder = os.path.join(self.build_folder, self.ZIP_FOLDER_NAME)

        # Extract the License/s from the header to a file
        with tools.chdir(source_folder):
            tmp = tools.load('zlib.h')
            license_contents = tmp[2:tmp.find('*/', 1)]
            tools.save('LICENSE', license_contents)
        self.copy('LICENSE', src=source_folder)

    def package_info(self):
        if self.settings.os == 'Windows':
            self.cpp_info.libs = ['zlib']
        else:
            self.cpp_info.libs = ['z']
