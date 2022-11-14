#include <cmath>
#include <boost/multiprecision/cpp_int.hpp>

class Math{
    public:
        long double e = 2.718281828459045;
        long double pi = 3.141592653589793;

        boost::multiprecision::cpp_int factorial(int n){
            boost::multiprecision::cpp_int f = 1;

            for(int i = 1; i <= n; ++i) {
                f *= i;
            }

            return f;
        }

        int factorial(short n){
            int f = 1;

            for(int i = 1; i <= n; ++i) {
                f *= i;
            }

            return f;
        }

        long double sqrt(long double root){
            return sqrtf(root);
        }

        long double exp(long double x){
            return pow(e, x);

        } long double exp(long long int x){
            return pow(e, x);
        }

        long double cos(long double x){
            return cosf(x);
        }
        
        long double sin(long double x){
            return sinf(x);
        }

        long double tan(long double x){
            return tanf(x);
        }

        long double acos(long double x){
            return acosf(x);
        }
        
        long double asin(long double x){
            return asinf(x);
        }

        long double atan(long double x){
            return atanf(x);
        }

        long double hcos(long double x){
            return hcos(x);
        }
        
        long double hsin(long double x){
            return asinf(x);
        }

        long double htan(long double x){
            return atanf(x);
        }

        long double radians(long double deg){
            return deg * (pi / 180);
        }

        long double degrees(long double rad){
            return rad * (180 / pi);
        }

        int floor(long double x){
            return floorf(x);
        }

        int ceil(long double x){
            return ceilf(x);
        }
};