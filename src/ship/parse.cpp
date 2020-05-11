#include <iostream>
#include <sstream>
#include <regex>

#include "ship.hpp"


void Ship::parse(ShipNode *parent, std::string html_source)
{
  static std::regex RE_NODE = std::regex("<(\\w+)[^>]*>([\\s\\S]*)<\\/\\1>");
  static int level = 0;

  parent->set_content(html_source);

  std::cerr << "HERE" << std::endl;

  auto beg = std::sregex_iterator(html_source.begin(), html_source.end(), RE_NODE);
  auto end = std::sregex_iterator();
  
  std::cerr << "AFTER ITERATOR" << std::endl;

  for (auto it = beg; it != end; it++) {
    std::smatch match = *it;

    std::string name = match[1], inner_html = match[2];

    for (int i = 0; i < level; i++)
      std::cerr << " ";
    std::cerr << name << std::endl;

    auto child = parent->create_child(name);
    level++;
    this->parse(child, inner_html);
    level --;
  }
}


std::string Ship::to_plaintext()
{
  ShipNode *body = this->root->find_child("body");

  if (body == nullptr)
    body = this->root;

  std::string content = body->get_content();
  std::cerr << content << std::endl;

  static std::regex RE_TAG = std::regex("<.*?>");

  std::stringstream ss;
  auto beg = std::sregex_iterator(content.begin(), content.end(), RE_TAG);
  auto end = std::sregex_iterator();
  auto cdata = content.data();
  int i = 0;
  int len = content.size();
  for (auto it = beg; it != end; it++) {
    auto match = *it;

    for (; i < match.position(); i++)
      ss << cdata[i];

    i += match.length();

  }

  for (;i < len; i++)
      ss << cdata[i];

  return ss.str();
}
