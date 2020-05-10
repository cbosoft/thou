#pragma once

#include <iostream>
#include <string>
#include <sstream>

#include "twirl_response.hpp"

class Twirl {

  private:

    std::stringstream buffer;

    Twirl();
    ~Twirl();

  public:

    static Twirl &get_singleton();
    void recieve(std::string data);
    TwirlResponse get(std::string url);

};
