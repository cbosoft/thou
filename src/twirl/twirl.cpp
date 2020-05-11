#include <iostream>
#include <cstring>

#include <curl/curl.h>

#include "twirl.hpp"

Twirl::Twirl()
  : buffer(nullptr), buffer_len(0)
{
  curl_global_init(CURL_GLOBAL_DEFAULT);
}

Twirl::~Twirl()
{
  if (this->buffer) {
    free(this->buffer);
  }
  curl_global_cleanup();
}

Twirl &Twirl::get_singleton()
{
  static Twirl t;
  return t;
}

size_t recieve_bytes(char *data, size_t size, size_t nmemb, Twirl *t)
{
  (void) size; // from the man: "size is always 1." ...
  t->recieve(data, nmemb);
  return nmemb;
}

void Twirl::recieve(char *data, int len)
{
  this->buffer_len += len;
  std::cerr << buffer_len << std::endl;
  this->buffer = (char*)realloc(this->buffer, this->buffer_len+1);
  for (int i = 0, j = this->buffer_len-len; i < len; i++, j++) {
    this->buffer[j] = data[i];
  }
  this->buffer[this->buffer_len] = 0;
}

Ship Twirl::get(std::string url)
{
  if (this->buffer) {
    free(this->buffer);
    this->buffer = nullptr;
    this->buffer_len = 0;
  }

  auto h = curl_easy_init();
  curl_easy_setopt(h, CURLOPT_URL, url.c_str());
  curl_easy_setopt(h, CURLOPT_WRITEFUNCTION, recieve_bytes);
  curl_easy_setopt(h, CURLOPT_WRITEDATA, this);
  curl_easy_perform(h);


  std::string r = std::string(this->buffer);
  return Ship(r);
}
