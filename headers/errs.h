#ifndef ERRS_H
#define ERRS_H
#include <stdio.h>

typedef enum {
    OK = 0,      // OK
    ARGS = 1,    // Usage: control2310 id info [mapper]
} Errors;

// Display error messages based on the enum provided
Errors error_msg(Errors type);

#endif

