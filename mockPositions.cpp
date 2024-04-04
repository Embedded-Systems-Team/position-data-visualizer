#include <iostream>
#include <curl/curl.h>
#include <string>
#include <vector>
#include <chrono>
#include <thread>

// Define a simple struct to hold your coordinates
float x = 0.0f;
float y = 0.0f;
float z = 0.0f;

// Generate a random float between -1.0 and 1.0
float randomFloat()
{
    return (float)(rand()) / ((float)(RAND_MAX) / 3.0f) - 1.5f;
}

int main() {
    CURL *curl;
    CURLcode res;

    // Initialize a CURL session
    curl = curl_easy_init();

    if (curl) {
        std::cout << "CURL initialized successfully." << std::endl;

        while (1) {
            // Construct the JSON data from the current coordinate
            x += randomFloat();
            y += randomFloat();
            z += randomFloat();
            std::string jsonData = R"({"x": )" + std::to_string(x) +
                                   R"(, "y": )" + std::to_string(y) +
                                   R"(, "z": )" + std::to_string(z) + R"(})";

            // Set the URL for the POST request
            curl_easy_setopt(curl, CURLOPT_URL, "http://127.0.0.1:5000/api/position-data/");

            // Specify that this is a POST request
            curl_easy_setopt(curl, CURLOPT_POST, 1L);

            // Pass the JSON data to the server
            curl_easy_setopt(curl, CURLOPT_POSTFIELDS, jsonData.c_str());

            // Set the content type header
            struct curl_slist *headers = NULL;
            headers = curl_slist_append(headers, "Content-Type: application/json");
            curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

            // Perform the request, and check for errors
            res = curl_easy_perform(curl);
            if (res != CURLE_OK) {
                std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
            }

            std::cout << "Data sent: " << jsonData << std::endl;

            // Wait for 1 second before sending the next request
            std::this_thread::sleep_for(std::chrono::seconds(1));

            // Clean up the headers for the next iteration
            curl_slist_free_all(headers);
        }

        // Final cleanup
        curl_easy_cleanup(curl);
    } else {
        std::cerr << "Failed to initialize CURL." << std::endl;
    }

    return 0;
}
