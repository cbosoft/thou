#pragma once

#include <iostream>
#include <string>
#include <sstream>

#include "../fish/fish.hpp"

class Net {

  private:

    char *buffer;
    int buffer_len;

    Net();
    ~Net();

  public:

    static Net &get_singleton();
    void recieve(char *data, int len);
    Fish get(std::string url);

};
