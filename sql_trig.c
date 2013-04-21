/* sql_trig.c */

/* Dynamic lib compilation and linking:
 *
 * $ gcc -c -fPIC sql_trig.c
 * $ ld -shared -o sql_trig.so sql_trig.o -lm
 */

#include "sqlite3ext.h"
SQLITE_EXTENSION_INIT1;
#include <stdlib.h>

/* this bit is required to get M_PI out of MS headers */
#if defined( _WIN32 )
#define _USE_MATH_DEFINES
#endif /* _WIN32 */

#include <math.h>

#define RADIANS(d) (( d / 180.0 ) * M_PI)

static void sql_trig_sin( sqlite3_context *ctx, int num_values, sqlite3_value **values )
{
	double a = RADIANS(sqlite3_value_double( values[0] ));
	sqlite3_result_double( ctx, sin( a ) );
}

static void sql_trig_cos( sqlite3_context *ctx, int num_values, sqlite3_value **values )
{
	double a = RADIANS(sqlite3_value_double( values[0] ));
	sqlite3_result_double( ctx, cos( a ) );
}

static void sql_trig_acos( sqlite3_context *ctx, int num_values, sqlite3_value **values )
{
	double a = sqlite3_value_double( values[0] );
	sqlite3_result_double( ctx, acos( a ) );
}

static void sql_trig_radians( sqlite3_context *ctx, int num_values, sqlite3_value **values )
{
	sqlite3_result_double( ctx, RADIANS(sqlite3_value_double( values[0] ) ));
}


int sqlite3_extension_init( sqlite3 *db, char **error, const sqlite3_api_routines *api )
{
	SQLITE_EXTENSION_INIT2(api);

	sqlite3_create_function( db, "sin",1,
		SQLITE_UTF8, NULL, &sql_trig_sin, NULL, NULL );
	sqlite3_create_function( db, "cos",1,
		SQLITE_UTF8, NULL, &sql_trig_cos, NULL, NULL );
	sqlite3_create_function( db, "acos",1,
		SQLITE_UTF8, NULL, &sql_trig_acos, NULL, NULL );

	return SQLITE_OK;
}

