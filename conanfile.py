from conans import ConanFile, tools, VisualStudioBuildEnvironment
import os

class S3harkConan(ConanFile):
    name = "s3hark"
    version = "1.1.2"
    license = "BSD"
    author = "Charles Wang (c_w@berkeley.edu)"
    url = "https://github.com/NHERI-SimCenter/s3hark"
    description = "A Tool For Site Response Analysis"
    settings = "os", "compiler", "build_type", "arch"
    generators = "qmake", "cmake"
    requires = "lapack/3.7.1@conan/stable", "SimCenterCommonQt/0.1.7@simcenter/stable"
    build_policy = "missing"
    
    options = {
        "withQt":[True, False]
    }


    default_options = {"withQt": False}

    scm = {
         "type": "git",
         "url": "auto",
         "revision": "auto"
      }
    

    def configure(self):
        if self.settings.os == "Windows":
            self.options["libcurl"].with_winssl = True
            self.options["libcurl"].with_openssl = False
            self.options["lapack"].visual_studio = True
            self.options["lapack"].shared = True

        if self.options.withQt:
            self.options["qt"].qtcharts = True
            self.options["qt"].qt3d = True
            self.options["qt"].qtwebengine = True
            self.options["qt"].qtwebchannel = True
            self.options["qt"].qtdeclarative = True

    def build_requirements(self):
        if self.settings.os == "Windows":
            self.build_requires("jom_installer/1.1.2@bincrafters/stable")
        
        if self.options.withQt:
            self.build_requires("qt/5.12.2@bincrafters/stable")


    def package_id(self):
        del self.info.options.withQt


    def build(self):
        if self.settings.os == "Windows":
            env_build = VisualStudioBuildEnvironment(self)
            with tools.environment_append(env_build.vars):
                vcvars = tools.vcvars_command(self.settings)
            
            qmake = "%s && qmake" % (vcvars)
            makeCommand = "%s && jom" % (vcvars)
        else:
            qmake = 'qmake'
            makeCommand = 'make'

        qmakeCommand = '%s "CONFIG+=%s" %s/s3harkLib.pro' % (qmake, self.settings.build_type, self.source_folder)

        self.run(qmakeCommand, run_environment=True) 
        self.run(makeCommand, run_environment=True) 
        


    def package(self):
        self.copy("*", src="include", dst="include", keep_path=True)
        self.copy("*.h", src="FEM", dst="include", keep_path=False)
        self.copy("*.h", src="UI", dst="include", keep_path=False)
        self.copy("*.h", src="SiteResponse", dst="include", keep_path=False)
        self.copy("*.h", src=".", dst="include", keep_path=False)

        self.copy("*s3hark.lib", dst="lib", keep_path=False)
        self.copy("*s3hark.a", dst="lib", keep_path=False)
		
        self.copy("*", src="resources", dst="resources", keep_path=True)


    def package_info(self):
        self.cpp_info.libs = ["s3hark"]

    def imports(self):
        if self.settings.os == "Windows":
            output = './%s' % self.settings.build_type
            self.copy("lib*.dll", dst=output, src="bin")

