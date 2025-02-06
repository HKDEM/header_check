import python

/**
 * Detects direct user input passed to an SQL query function (e.g., `cursor.execute`).
 */
class SQLInjection extends TaintTracking::Configuration {
  SQLInjection() { this = "SQL injection" }

  // User input source, such as from `input()` function
  predicate isUserInput(DataFlow::Node node) {
    exists(FunctionCall fc |
      fc.getCallee().getName() = "input" and
      node = fc.getArgument(0)
    )
  }

  // SQL query sink, such as `execute` function of SQLite or other database calls
  predicate isSQLQuerySink(DataFlow::Node node) {
    exists(FunctionCall fc |
      fc.getCallee().getName() = "execute" and
      node = fc.getArgument(0)
    )
  }

  // The data flow path between source (user input) and sink (SQL query execution)
  from DataFlow::Node source, DataFlow::Node sink
  where
    isUserInput(source) and
    isSQLQuerySink(sink) and
    source.getLocation() != sink.getLocation()
  select source, sink, "Possible SQL injection detected"
}
