#include <random>
#include <ctime>

class Rnd{
    public:
        long long int randint(long long int min, long long int max) {
            srand (time(0));
            return (rand() % max) + min;

        }

};
