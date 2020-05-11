#include <iostream>
#include <cstring>

#include <curl/curl.h>

#include "net.hpp"

Net::Net()
  : buffer(nullptr), buffer_len(0)
{
  curl_global_init(CURL_GLOBAL_DEFAULT);
}

Net::~Net()
{
  if (this->buffer) {
    free(this->buffer);
  }
  curl_global_cleanup();
}

Net &Net::get_singleton()
{
  static Net t;
  return t;
}

size_t recieve_bytes(char *data, size_t size, size_t nmemb, Net *t)
{
  (void) size; // from the man: "size is always 1." ...
  t->recieve(data, nmemb);
  return nmemb;
}

void Net::recieve(char *data, int len)
{
  this->buffer_len += len;
  std::cerr << buffer_len << std::endl;
  this->buffer = (char*)realloc(this->buffer, this->buffer_len+1);
  for (int i = 0, j = this->buffer_len-len; i < len; i++, j++) {
    this->buffer[j] = data[i];
  }
  this->buffer[this->buffer_len] = 0;
}

Fish Net::get(std::string url)
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
  return Fish(r);
}
