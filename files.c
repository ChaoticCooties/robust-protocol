#include <sys/types.h>
#include <sys/socket.h>
#include <string.h>

#include "headers/op.h"
#include "headers/array.h"
#include "headers/encode.h"
#include "headers/decode.h"

int split_file(char* filePath, int bufferSize, char** list) {
    FILE *file = NULL;
    uint8_t buffer[bufferSize];
    size_t bytesRead = 0;
    
    file = fopen(filePath, "rb");
    
    if (file != NULL) {
        // Loop chunking until EOF
        while ((bytesRead = fread(buffer, 1, sizeof(buffer), file)) > 0) {
           // Reed-Solomon 
        }
    }

    return 1;
}

int join_file(char* filePath, int bufferSize) {
    FILE *file = NULL;
    uint8_t buffer[bufferSize];
    size_t bytesRead;
}

struct Array* encode_data(char* my_msg) {
    struct gf_tables *gf_table = malloc(sizeof(struct gf_tables));
	gf_table->gf_exp = malloc(sizeof(struct Array));
	gf_table->gf_log = malloc(sizeof(struct Array));
	initArray(gf_table->gf_exp, 512);
	initArray(gf_table->gf_log, 256);
	gf_table = init_tables();

    struct Array *msg_in = malloc(sizeof(struct Array));
    initArray(msg_in, 50);

	for (size_t i = 0; i < strlen(my_msg); i++) {
		msg_in->array[i] = (int)my_msg[i];
		insertArray(msg_in);
	}

    struct Array *msg = malloc(sizeof(struct Array));
	initArray(msg, 170);
    msg = rs_encode_msg(msg_in, 14, gf_table);

    freeArray(gf_table->gf_exp);
	freeArray(gf_table->gf_log);
	freeArray(msg_in);

    return msg;
}

uint8_t decode_data(struct Array* msg) {
    struct gf_tables *gf_table = malloc(sizeof(struct gf_tables));
	gf_table->gf_exp = malloc(sizeof(struct Array));
	gf_table->gf_log = malloc(sizeof(struct Array));
	initArray(gf_table->gf_exp, 512);
	initArray(gf_table->gf_log, 256);
	gf_table = init_tables();

	struct Array *synd = malloc(sizeof(struct Array));
	struct Array *err_loc = malloc(sizeof(struct Array));
	struct Array *pos = malloc(sizeof(struct Array));
	struct Array *rev_pos = malloc(sizeof(struct Array));
    
    synd = rs_calc_syndromes(msg, 14, gf_table);
    err_loc = rs_find_error_locator(synd, 14, 0, gf_table);
    pos = rs_find_errors(reverse_arr(err_loc), msg->used, gf_table);

    rev_pos = reverse_arr(pos);

    struct Array *err_pos = malloc(sizeof(struct Array));
	initArray(err_pos, 3);
	err_pos->array[0] = 0;

    msg = rs_correct_msg(msg, 14, err_pos, gf_table);
    
    freeArray(gf_table->gf_exp);
	freeArray(gf_table->gf_log);
	freeArray(msg);
	freeArray(synd);
	freeArray(pos);
	freeArray(rev_pos);

    return *msg->array;
}
