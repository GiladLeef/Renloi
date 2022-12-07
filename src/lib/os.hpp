#include "iostream"
#include "stdio.h"
#include "fstream"
#include "filesystem"
#include <boost/filesystem.hpp>

#if defined(_WIN32)
    #define PLATFORM_NAME "windows"
#elif defined(_WIN64)
    #define PLATFORM_NAME "windows"
#elif defined(__linux__)
    #define PLATFORM_NAME "linux"
#elif defined(__unix__) || !defined(__APPLE__) && defined(__MACH__)
    #include <sys/param.h>
    #if defined(BSD)
        #define PLATFORM_NAME "bsd"
    #endif
#elif defined(__hpux)
    #define PLATFORM_NAME "hp-ux"
#elif defined(_AIX)
    #define PLATFORM_NAME "aix"
#elif defined(__APPLE__) && defined(__MACH__)
    #include <TargetConditionals.h>
    #elif TARGET_OS_MAC == 1
        #define PLATFORM_NAME "osx" 
    #endif

class Os{
    private:
        const char *get_platform_name() {
            return (PLATFORM_NAME == NULL) ? "" : PLATFORM_NAME;
        }
        
        const char *platform = get_platform_name();

        std::string filenotfound = "renloi: FileNotFoundError: ";

    public:
        // No exceptions on failed process, just return error code
        int system(const char * cmd){
            int code = std::system(cmd);
            return code;
        } int system(std::string cmd){
            int code = std::system(cmd.c_str());
            return code;
        }

        // Throw exception if returned bool is false, else it was successful
        void remove(const char * filename){
            std::filesystem::__cxx11::path pfilename = filename;

            if (!std::filesystem::remove(pfilename)){
                // Throw std::filesystem::__cxx11::filesystem_error; not implemented
            }
            
        } void remove(std::string filename){
            std::filesystem::__cxx11::path pfilename = filename;

            if (!std::filesystem::remove(pfilename)){
                // Throw std::filesystem::__cxx11::filesystem_error; not implemented
            }
        }

        // Throws std::filesystem::__cxx11::filesystem_error automatically if file not found
        void rename(const char * old, const char * _new){
            std::filesystem::__cxx11::path oldp = old;
            std::filesystem::__cxx11::path newp = _new;
            std::filesystem::rename(oldp, newp);
            
        } void rename(std::string old, const char * _new){
            std::filesystem::__cxx11::path oldp = old;
            std::filesystem::__cxx11::path newp = _new;
            std::filesystem::rename(oldp, newp);
            
        } void rename(std::string old, std::string _new){
            std::filesystem::__cxx11::path oldp = old;
            std::filesystem::__cxx11::path newp = _new;
            std::filesystem::rename(oldp, newp);
            
        } void rename(const char * old, std::string _new){
            std::filesystem::__cxx11::path oldp = old;
            std::filesystem::__cxx11::path newp = _new;
            std::filesystem::rename(oldp, newp);
        }

        // Throws std::filesystem::__cxx11::filesystem_error automatically if file not found
        void chdir(const char * path){
            std::filesystem::current_path(path);
        } void chdir(std::string path){
            std::filesystem::current_path(path);
        }

        void mkdir(const char * path){
            std::filesystem::create_directory(path);
        } void mkdir(std::string path){
            std::filesystem::create_directory(path);
        }

        void rmdir(const char * path){
            // Not implemented
        } void rmdir(std::string path){
            // Not implemented
        }

        std::string getcwd(){
            return std::filesystem::current_path();
        }
};