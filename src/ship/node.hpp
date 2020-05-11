#pragma once

#include <iostream>
#include <string>
#include <map>
#include <list>
#include <exception>

class ShipNode {

  private:
    ShipNode *parent;
    std::string name, content;
    std::map<std::string, std::string> attributes;
    std::list<ShipNode *> children;

  public:

    ShipNode() : ShipNode(nullptr, "root") {}
    ShipNode(std::string name) : ShipNode(nullptr, name) {}
    ShipNode(ShipNode *parent, std::string name)
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

    ~ShipNode()
    {
      for (auto child : this->children) {
        delete child;
      }
    }

    void set_attr(std::string key, std::string value)
    {
      this->attributes[key] = value;
    }

    std::string get_attr(std::string key)
    {
      auto it = this->attributes.find(key);
      if (it == this->attributes.end()) {
        throw std::runtime_error("key not found");
      }

      return it->second;
    }

    ShipNode *create_child(std::string name)
    {
      ShipNode *child = new ShipNode(this, name);
      this->children.push_back(child);
      return child;
    }

    void set_content(std::string content)
    {
      this->content = content;
    }

    const std::string &get_content() const
    {
      return this->content;
    }

    ShipNode *find_child(std::string name)
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
};

