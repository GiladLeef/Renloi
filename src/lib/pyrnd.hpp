#include <algorithm>
#include <iostream>
#include <random>
#include <vector>

class Rnd{
    public:
        long long int randint(long long int min, long long int max){
            std::random_device rd;
            std::mt19937 gen(rd()); 
            std::uniform_int_distribution<> distr(min, max);

            return distr(gen);
        }

        long double random(){
            return static_cast <long double> (rand()) / static_cast <long double> (RAND_MAX);
        }

        long long int choice(const std::vector<long long int> in){
            std::vector<int> out;
            std::sample(in.begin(), in.end(), std::back_inserter(out), 1, std::mt19937{std::random_device{}()});

            return out[0];
        }

        std::string choice(const std::vector<std::string> in){
            std::vector<std::string> out;
            std::sample(in.begin(), in.end(), std::back_inserter(out), 1, std::mt19937{std::random_device{}()});

            return out[0];
        }

        long double choice(const std::vector<long double> in){
            std::vector<long double> out;
            std::sample(in.begin(), in.end(), std::back_inserter(out), 1, std::mt19937{std::random_device{}()});

            return out[0];
        }
};