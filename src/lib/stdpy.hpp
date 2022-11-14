#include <iostream>
#include <cmath>
#include <cassert>
#include <sstream>
#include <cctype>
#include <algorithm>
#include "boost/multiprecision/cpp_int.hpp"

typedef boost::multiprecision::cpp_int bigint;

void print(std::string str){
    std::cout << str << char(10);
}

void print(const char *cstr){
    std::cout << cstr << char(10);
}

void print(int istr){
    std::cout << istr << char(10);
}
void print(float fstr){
    std::cout << fstr << char(10);
}
void print(long long int llistr){
    std::cout << llistr << char(10);
}

void print(long double ldstr){
    std::cout << ldstr << char(10);
}

void print(long lstr){
    std::cout << lstr << char(10);
}

void print(double dstr){
    std::cout << dstr << char(10);
}

void print(bigint bigintstr){
    std::cout << bigintstr << char(10);
}

void print(bool bstr){
    std::cout << bstr << char(10);
}

bigint len(std::string str){
    return str.length();
}
bigint len(std::vector<bigint> container){
    return container.size();
}
bigint len(std::vector<std::string> container){
    return container.size();
}
bigint len(std::vector<float> container){
    return container.size();
}
std::string input(std::string prompt){
    std::cout << prompt; std::string x; std::cin >> x; return x;
}

// This class is not mine, it was posted here https://www.daniweb.com/programming/software-development/code/252294/string-class-inherited-from-basic-string
class pystring : public std::basic_string<char>
{
    public:
        typedef std::basic_string<char> string_type;
    public:	
        pystring() : string_type() {}
        pystring(const char * str) : string_type(str){}
        pystring(const char * str, size_t n) : string_type(str,n) {}
        pystring(size_t n , char c ) : string_type(n,c) {}
    public:
        //added functionalities
        pystring  upper()const      { return _apply(std::toupper);  }
        pystring  lower()const      { return _apply(std::tolower);  }
        
        bool    isDigit()const     { return _isAllDigits();	}
        bool    islower()const      { return _checkIf(std::islower);}
        bool    isupper()const      { return _checkIf(std::isupper);}
        bool    isalpha()const      { return _checkIf(std::isalpha);}

        int     toInt()	const       { return _convertTo<int>(*this);}		
        long    toLong()const       { return _convertTo<long>(*this);}	
        float   toFloat()const      { return _convertTo<float>(*this);}
        double  toDouble()const     { return _convertTo<double>(*this);}		
        size_t  toSizeT()const      { return _convertTo<size_t>(*this);}

        void    reset()             { *this = pystring();	}

        bool    startswith(const pystring& preFix)const {
                    return substr(0,preFix.size()) == preFix; 
                }
        bool    endswith(const pystring& suffix)const	{
                    return substr(size()-suffix.size()) == suffix; 
                }
        
        void    shuffleIt() {
                    std::random_shuffle( begin(), end()); 
                }
        
        pystring  shuffled()const{
                    pystring tmp = *this;
                    tmp.shuffleIt();
                    return tmp; 
                }
        //conversion function
        operator const char*(){
            return c_str();
        }
    private:
        //helpers
        typedef int(*ApplyFunc)(int); 	
        //converts a string to a valid data type
        template<typename ReturnType>
        ReturnType _convertTo(const pystring& str)const{			
            _assertValidSize();
            std::stringstream convert;
            convert << str ;
            ReturnType data;
            assert(!(convert >> data).fail() ); //make sure conversion was succesful
            return data;
        }

        //takes in a function and returns a string with that function applied to the whole string
        pystring _apply(const ApplyFunc& Applier )const{
            _assertValidSize();
            pystring str;
            std::transform( begin(),end(), //from start to end
                            std::back_insert_iterator<string_type>(str), //adjust str size
                            Applier); //while applying a function to it
            return str;
        }	

        bool _checkIf(const ApplyFunc& Applier)const{
            for(size_t indx = 0; indx != size(); ++indx){			
                if(!Applier((*this)[indx]) )return false;
            }
            return true;
        }

        bool _isAllDigits()const{
            size_t start = 0;
            if((*this)[0] == '-' ) 
                start = 1;
            for(; start < size(); ++start){
                char value = (*this)[start];
                if(!isdigit( value ) && value != '.' )
                    return false;
            }
            return true;
        }
        void _assertValidSize()const{
            assert(size());
        }	
};