from os import path
from glob import glob
from conan import ConanFile
from conan.tools.scm import Git
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import copy 


class couchbaseliteRecipe(ConanFile):
    name = "couchbaselite"
    version = "8f6fec8440ce7eef2db98f5e9814f03c5b77aef6"

    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "*.diff"

    def configure(self):
        if self.settings.build_type == "Release":
            self.settings.build_type = "MinSizeRel"

    def source(self):
        git = Git(self, self.source_folder)
        git.clone(url="https://github.com/couchbase/couchbase-lite-C.git", target=".")
        git.checkout("8f6fec8440ce7eef2db98f5e9814f03c5b77aef6")
        git.run("submodule update --init --recursive")
        for patch in glob(path.join(self.source_folder, "..", "*.diff")):
            git.run(f"apply {patch}")
    
    def layout(self):
        cmake_layout(self, src_folder="src")

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        copy(self, "LICENSE", src=self.source_folder, dst=path.join(self.package_folder, "licenses"))


    def package_info(self):
        self.cpp_info.libs = ["cblite"]