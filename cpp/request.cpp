#include <curl/curl.h>
#include <iostream>
#include <string>

static char errorBuffer[CURL_ERROR_SIZE];
static std::string buffer;

size_t callback_writer(const char *ptr, const size_t size, const size_t nmemb, std::string *stream)
{
    if (stream == NULL) {
        return 0;
    }
    const int data_length = size * nmemb;
    stream->append(ptr, data_length);
    return data_length;
}

bool curl_get (const std::string endpoint)
{
    CURL *conn = NULL;
    conn = curl_easy_init();

    if (NULL == conn) {
        std::cout << "failed to create CURL connection" << std::endl;
        curl_easy_cleanup(conn);
        // std::exit(EXIT_FAILURE);
        return 1;
    }

    try {
        curl_easy_setopt(conn, CURLOPT_TIMEOUT, 1);
        curl_easy_setopt(conn, CURLOPT_URL, endpoint.c_str());
        curl_slist *plist = curl_slist_append(NULL, "Content-Type:application/json;charset=utf-8");
        curl_easy_setopt(conn, CURLOPT_HTTPHEADER, plist);
        curl_easy_setopt(conn, CURLOPT_WRITEFUNCTION, callback_writer);
        std::string chunk;
        curl_easy_setopt(conn, CURLOPT_WRITEDATA, &chunk);

        CURLcode res = curl_easy_perform(conn);
        if (res != CURLE_OK) {
            std::cout << "curl_easy_perform() failed:" << curl_easy_strerror(res) << std::endl;
        }

        curl_easy_cleanup(conn);
    } catch (std::exception &ex) {
        std::cout << "curl exception " << ex.what() << std::endl;
    }
    return 0;
}

static bool init(CURL *&conn, const std::string &url)
{
    CURLcode code;

    conn = curl_easy_init();

    if (conn == NULL) {
        std::cout << "Failed to create CURL connection." << std::endl;
        exit(EXIT_FAILURE);
    }

    code = curl_easy_setopt(conn, CURLOPT_ERRORBUFFER, errorBuffer);
    if (code != CURLE_OK) {
        std::cout << "Failed to set error buffer " << code << std::endl;
        return false;
    }

    code = curl_easy_setopt(conn, CURLOPT_URL, url.c_str());
    if (code != CURLE_OK) {
        std::cout << "Failed to set URL " << errorBuffer << std::endl;
        return false;
    }

    code = curl_easy_setopt(conn, CURLOPT_FOLLOWLOCATION, 1L);
    if (code != CURLE_OK) {
        std::cout << "Failed to set redirect option " << errorBuffer << std::endl;
        return false;
    }

    code = curl_easy_setopt(conn, CURLOPT_WRITEFUNCTION, callback_writer);
    if (code != CURLE_OK) {
        std::cout << "Failed to set writer " << errorBuffer << std::endl;
        return false;
    }

    code = curl_easy_setopt(conn, CURLOPT_WRITEFUNCTION, &buffer);
    if (code != CURLE_OK) {
        std::cout << "Failed to set write data " << errorBuffer << std::endl;
        return false;
    }

    return true;
}

int main(int argc, char *argv[])
{
    if (argc != 2) {
        std::cout << "Usage: " << argv[0] << " <url>" << std::endl;
        exit(EXIT_FAILURE);
    }

    curl_global_init(CURL_GLOBAL_DEFAULT);

    CURL *conn = NULL;
    std::string url = argv[1];
    if (!init(conn, url)) {
        std::cout << "Connection initialization failed." << std::endl;
        exit(EXIT_FAILURE);
    }

    CURLcode code = curl_easy_perform(conn);
    curl_easy_cleanup(conn);

    std::cout << url << std::endl;
    exit(EXIT_SUCCESS);
    if (code != CURLE_OK) {
        std::cout << "Failed to get " << url << std::endl;
        exit(EXIT_FAILURE);
    }

    return EXIT_SUCCESS;
}
