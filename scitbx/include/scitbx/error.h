/*! \file
    Declarations and macros for exception handling.
 */

#ifndef SCITBX_ERROR_H
#define SCITBX_ERROR_H

#include <stdio.h>
#include <exception>
#include <string>
#include <sstream>

#include <scitbx/smart_error.h>

#define SCITBX_CHECK_POINT\
  std::cout << __FILE__ << "(" << __LINE__ << ")" << std::endl << std::flush
#define SCITBX_EXAMINE(A)\
  std::cout << "variable " <<#A<< ": " << A << " " << std::endl << std::flush

//! Common scitbx namespace.
namespace scitbx {

  //! All scitbx exceptions are derived from this class.
  class error : public smart_error<error>
  {
    public:

      //! General scitbx error message.
      explicit
      error(std::string const& msg) throw()
        : smart_error<error>("scitbx", msg)
      {}

      //! Error message with file name and line number.
      /*! Used by the macros below.
       */
      error(const char* file, long line, std::string const& msg = "",
            bool internal = true) throw()
        : smart_error<error>("scitbx", file, line, msg, internal)
      {}
  };

  //! Special class for "Index out of range." exceptions.
  /*! These exceptions are propagated to Python as IndexError.
   */
  class error_index : public error
  {
    public:
      //! Default constructor. The message may be customized.
      explicit
      error_index(std::string const& msg = "Index out of range.") throw()
        : error(msg)
      {}
  };

} // namespace scitbx

//! For throwing an error exception with file name, line number, and message.
#define SCITBX_ERROR(msg) REPORT_ERROR(scitbx::error, msg)
//! For throwing an "Internal Error" exception.
#define SCITBX_INTERNAL_ERROR() REPORT_INTERNAL_ERROR(scitbx::error)
//! For throwing a "Not implemented" exception.
#define SCITBX_NOT_IMPLEMENTED() REPORT_NOT_IMPLEMENTED(scitbx::error)

//! Custom scitbx assertion.
#define SCITBX_ASSERT(assertion)\
  SMART_ASSERT(scitbx::error, SCITBX_ASSERT, assertion)

#endif // SCITBX_ERROR_H
