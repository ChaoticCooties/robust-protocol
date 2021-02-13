#include <pthread.h>
#include <stdbool.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h> 
#include <sys/socket.h> 
#include <arpa/inet.h> 
#include <netinet/in.h>

#include "errs.h"

// Socket port
#define PORT 8888

// Max buffer size per chunk
#define MAXCHUNK 256

// Max Threads
#define MAXTHREADS 1000

// Sender threads
void* senderThread(void *arg) {
    struct sockaddr_in servAddr;
    socklen_t addrSize;
    int sockfd;

   // Create the socket
    if((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("Failed to open socket");
        pthread_exit(NULL);
    }

   // Server Information
   memset(&servAddr, 0, sizeof(servAddr));
   servAddr.sin_family = AF_INET;
   servAddr.sin_port = htons(PORT);
   servAddr.sin_addr.s_addr = INADDR_ANY;

   int n, len;
   pthread_exit(NULL);
}

// Format: receiver/sender ipaddress
int main(int argc, char** argv) { 
    // Args check
    if (argc != 2) {
        return error_msg(ARGS);
    }

    pthread_t tid[MAXTHREADS];
    for (int i = 0; i < MAXTHREADS; ++i) {
        if (pthread_create(&tid[i], NULL, senderThread, NULL) != 0) {
            perror("Failed to create thread\n");
        }
    }
} 
