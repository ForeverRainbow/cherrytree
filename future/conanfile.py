from conans import ConanFile, CMake, tools
from conans.tools import os_info


class CherrytreeConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "pkg_config"
    requires = 'spdlog/[>=1.4.1]'

    _ubuntu_deps = ('build-essential','libxml2-utils','cmake','libgtkmm-3.0-dev',
                            'libgtksourceviewmm-3.0-dev','libxml++2.6-dev','libsqlite3-dev',
                            'libcpputest-dev','gettext','python3-lxml','libgspell-1-dev',
                            'libcurl4-openssl-dev',
                            )
    _fedora_deps = ('gcc-c++','libtool','autoconf','gtkmm30-devel','gtksourceviewmm3-devel','libxml++-devel',
                    'libsq3-devel','gettext-devel','gettext','intltool','python3-lxml','libxml2',
                    'gspell-devel',
                    )

    _arch_deps = ('gtksourceviewmm', 'libxml++2.6', 'python-lxml', 'gspell',
                    )

    _mac_deps = ('python3','cmake','pkg-config','gtksourceviewmm3','gnome-icon-theme','gspell','libxml++',
                    'cpputest',
                    )
    _msys_deps = ('mingw-w64-x86_64-toolchain', 'mingw-w64-x86_64-cmake', 'mingw-w64-x86_64-gtkmm3',
                    'mingw-w64-x86_64-gtksourceviewmm3','mingw-w64-x86_64-libxml++2.6',
                    'mingw-w64-x86_64-sqlite3','mingw-w64-x86_64-gspell','mingw-w64-x86_64-curl',
                    'mingw-w64-x86_64-python3-lxml' 'mingw-w64-x86_64-gettext',
                    'tar nano git', 'mingw-w64-x86_64-meld3',
                    )

    def source(self):
        self.run("git clone https://github.com/giuspen/cherrytree")
        
    def build_requirements(self):
        if not tools.os_info.is_macos and not tools.os_info.linux_distro == "ubuntu":
            # On non mac or ubuntu there is no package for cpputest and afaik conan does not support pacman build
            self.build_requires('CppUTest/master@0xg/stable')

    def _get_system_pkgs(self):
        pkgs = ()
        if os_info.detect_windows_subsystem() == "MSYS2":
            pkgs = self._msys_deps
        elif os_info.is_macos:
            pkgs = self._mac_deps
        elif os_info.is_linux:
            distro = os_info.linux_distro
            if distro == "fedora":
                pkgs = self._fedora_deps
            elif distro == "arch":
                pkgs = self._arch_deps
            elif distro == "ubuntu":
                pkgs = self._ubuntu_deps
        return pkgs

    def _install_system_pkgs(self, pkgs):
        pkg_tool = tools.SystemPackageTool()
        for pkg in pkgs:
            pkg_tool.install(pkg)

    def system_requirements(self):
        pkgs = self._get_system_pkgs()
        if pkgs:
            self._install_system_pkgs(pkgs)
        else:
            raise RuntimeError("System not supported")


    def test(self): 
        self.run("./tests/run_tests")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        self.test()


        