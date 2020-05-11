#include "node.hpp"


FishNode::FishNode()
  :
    FishNode(nullptr, "root")
{
}


FishNode::FishNode(std::string name)
  :
    FishNode(nullptr, name)
{
}


FishNode::FishNode(FishNode *parent, std::string name)
  : parent(parent)
{
  auto data = name.data();
  int len = name.size();

  for (int i = 0; i < len; i++) {
    int c = (int)data[i];
    if ((c <= 90) and (c >= 65)) {
      data[i] += 32;
    }
  }

  this->name = std::string(data);
}


FishNode::~FishNode()
{
  for (auto child : this->children) {
    delete child;
  }
}


void FishNode::set_attr(std::string key, std::string value)
{
  this->attributes[key] = value;
}


std::string FishNode::get_attr(std::string key)
{
  auto it = this->attributes.find(key);
  if (it == this->attributes.end()) {
    throw std::runtime_error("key not found");
  }

  return it->second;
}


FishNode *FishNode::create_child(std::string name)
{
  FishNode *child = new FishNode(this, name);
  this->children.push_back(child);
  return child;
}


void FishNode::set_content(std::string content)
{
  this->content = content;
}


const std::string &FishNode::get_content() const
{
  return this->content;
}


FishNode *FishNode::find_child(std::string name)
{
  for (auto node: this->children) {
    if (node->name.compare(name) == 0) {
      return node;
    }
  }

  for (auto node: this->children) {
    return node->find_child(name);
  }

  return nullptr;
}
