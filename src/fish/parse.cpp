#include <iostream>
#include <sstream>
#include <regex>

#include "fish.hpp"


void Fish::parse(FishNode *parent, std::string html_source)
{
  static std::regex RE_NODE = std::regex("<(\\w+)[^>]*>([\\s\\S]*)<\\/\\1>");
  static int level = 0;

  parent->set_content(html_source);

  // May 11 2020: bug in regex on large strings. try boost::regex instead.
  return;

  auto beg = std::sregex_iterator(html_source.begin(), html_source.end(), RE_NODE);
  auto end = std::sregex_iterator();

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


std::string Fish::to_plaintext()
{
  FishNode *body = this->root->find_child("body");

  if (body == nullptr)
    body = this->root;

  std::string content = body->get_content();

  static std::regex RE_SCRIPT = std::regex("<(script|SCRIPT)[^>]*>([\\s\\S]*?)<\\/\\1>");
  content = std::regex_replace(content.c_str(), RE_SCRIPT, "");

  static std::regex RE_HEAD = std::regex("<(head|HEAD)[^>]*>([\\s\\S]*?)<\\/\\1>");
  content = std::regex_replace(content.c_str(), RE_HEAD, "");

  static std::regex RE_SPACE = std::regex("\\s+");
  content = std::regex_replace(content.c_str(), RE_SPACE, " ");

  static std::regex RE_TAG = std::regex("<.*?>");
  content = std::regex_replace(content.c_str(), RE_TAG, "");

  return content;
}
