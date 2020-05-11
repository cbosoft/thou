#include "fish.hpp"

Fish::Fish()
  : root(new FishNode("root"))
{
  // do nothing
}

Fish::Fish(std::string html_source)
  : Fish()
{
  this->parse(this->root, html_source);
}

Fish::~Fish()
{
  delete this->root;
}
