#pragma once

#include <iostream>
#include <string>
#include <sstream>

#include "../ship/ship.hpp"

class Twirl {

  private:

    char *buffer;
    int buffer_len;

    Twirl();
    ~Twirl();

  public:

    static Twirl &get_singleton();
    void recieve(char *data, int len);
    Ship get(std::string url);

};
