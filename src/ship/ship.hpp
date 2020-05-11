#pragma once

#include <string>

#include "node.hpp"

class Ship {

  private:

    ShipNode *root;
    void parse(ShipNode *parent, std::string html_source);

  public:

    Ship();
    Ship(std::string html_source);
    ~Ship();

    std::string title();
    std::list<std::string> abundant_interesting_words();
    std::string to_plaintext();


};
