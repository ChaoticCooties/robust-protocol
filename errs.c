#include "errs.h"

// Display error messages based on the enum provided
Errors error_msg(Errors type) {
    const char* msg = "";
    switch (type) {
        case OK:
            return OK;
        case ARGS:
            msg = "Usage: [sender/receiver] ip";
            break;
    }
    fprintf(stderr, "%s\n", msg);
    return type;
}

