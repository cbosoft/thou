#include "ship.hpp"

Ship::Ship()
  : root(new ShipNode("root"))
{
  // do nothing
}

Ship::Ship(std::string html_source)
  : Ship()
{
  this->parse(this->root, html_source);
}

Ship::~Ship()
{
  delete this->root;
}
