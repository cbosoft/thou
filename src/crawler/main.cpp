#include <iostream>

#include "../twirl/twirl.hpp"

int main(int argc, const char **argv)
{
  (void) argc;
  (void) argv;

  Twirl &t = Twirl::get_singleton();
  //auto response = t.get("https://google.com");
  auto response = t.get("https://en.wikipedia.org/wiki/List_of_most_popular_websites");
  auto pt = response.to_plaintext();
  std::cerr << pt << std::endl;
}
