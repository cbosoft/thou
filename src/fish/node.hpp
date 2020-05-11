#pragma once

#include <iostream>
#include <string>
#include <map>
#include <list>
#include <exception>

class FishNode {

  private:
    FishNode *parent;
    std::string name, content;
    std::map<std::string, std::string> attributes;
    std::list<FishNode *> children;

  public:

    FishNode();
    FishNode(std::string name);
    FishNode(FishNode *parent, std::string name);

    ~FishNode();

    void set_attr(std::string key, std::string value);
    std::string get_attr(std::string key);
    FishNode *create_child(std::string name);
    void set_content(std::string content);
    const std::string &get_content() const;
    FishNode *find_child(std::string name);
};

