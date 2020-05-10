#include <iostream>

#include "../twirl/twirl.hpp"

int main(int argc, const char **argv)
{
  (void) argc;
  (void) argv;

  Twirl &t = Twirl::get_singleton();
  auto response = t.get("https://google.com");
}
