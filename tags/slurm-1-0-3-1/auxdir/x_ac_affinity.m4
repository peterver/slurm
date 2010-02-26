##*****************************************************************************
#  $Id$
##*****************************************************************************
#  AUTHOR:
#    Morris Jette <jette1@llnl.gov>
#
#  SYNOPSIS:
#    X_AC_AFFINITY
#
#  DESCRIPTION:
#    Test for various task affinity functions and set the definitions.
#
#  WARNINGS:
#    This macro must be placed after AC_PROG_CC or equivalent.
##*****************************************************************************

AC_DEFUN([X_AC_AFFINITY], [

# Test if sched_setaffinity function exists and argument count (it can vary)
  AC_CHECK_FUNCS(sched_setaffinity, [have_sched_setaffinity=yes])
  AM_CONDITIONAL(HAVE_SCHED_SETAFFINITY, test "x$have_sched_setaffinity" = "xyes")

  AC_TRY_COMPILE(
   [#define _GNU_SOURCE
    #include <sched.h>],
   [cpu_set_t mask;
    sched_getaffinity(0, sizeof(cpu_set_t), &mask);],
   [AC_DEFINE(SCHED_GETAFFINITY_THREE_ARGS, 1,
             [Define to 1 if sched_getaffinity takes three arguments.])])

  AC_TRY_COMPILE(
   [#define _GNU_SOURCE
    #include <sched.h>],
   [cpu_set_t mask;
    sched_getaffinity(0, &mask);],
   [AC_DEFINE(SCHED_GETAFFINITY_TWO_ARGS, 1,
             [Define to 1 if sched_getaffinity takes two arguments.])])

#
# Test for other affinity functions as appropriate
# TBD

])
