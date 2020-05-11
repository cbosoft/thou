#pragma once

#include <string>

#include "node.hpp"

class Fish {

  private:

    FishNode *root;
    void parse(FishNode *parent, std::string html_source);

  public:

    Fish();
    Fish(std::string html_source);
    ~Fish();

    std::string title();
    std::list<std::string> abundant_interesting_words();
    std::string to_plaintext();


};
