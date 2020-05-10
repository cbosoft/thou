#include <iostream>

#include <curl/curl.h>

#include "twirl.hpp"

Twirl::Twirl()
{
  curl_global_init(CURL_GLOBAL_DEFAULT);
}

Twirl::~Twirl()
{
  curl_global_cleanup();
}

Twirl &Twirl::get_singleton()
{
  static Twirl t;
  return t;
}

size_t recieve_bytes(void *buffer, size_t size, size_t nmemb, Twirl *t)
{
  (void) nmemb;
  std::string s((char*)buffer);
  t->recieve(s);
  return size;
}

void Twirl::recieve(std::string s)
{
  this->buffer << s;
}

TwirlResponse Twirl::get(std::string url)
{
  auto h = curl_easy_init();
  curl_easy_setopt(h, CURLOPT_URL, url.c_str());
  curl_easy_setopt(h, CURLOPT_WRITEFUNCTION, recieve_bytes);
  curl_easy_setopt(h, CURLOPT_WRITEDATA, this);
  curl_easy_perform(h);


  std::string r = this->buffer.str();
  this->buffer.str("");

  return TwirlResponse(r);
}
