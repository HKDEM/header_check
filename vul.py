import python

/**
 * Find cases where user input is directly used in SQL queries without sanitization.
 */
class UnsafeSQLQuery extends TaintTracking::Configuration {
  UnsafeSQLQuery() {
    this = "Vulnerable SQL query pattern"
  }

  predicate isUserInput(Expression e) {
    exists(FunctionCall fc |
      fc.getCallee().getName() = "input" and
      e = fc.getArgument(0)
    )
  }

  override predicate isSource(DataFlow::Node source) {
    isUserInput(source)
  }

  override predicate isSink(DataFlow::Node sink) {
    exists(FunctionCall fc |
      fc.getCallee().getName() = "execute" and
      fc.getArgument(0) = sink
    )
  }

  from DataFlow::Node source, DataFlow::Node sink
  where
    isSource(source) and
    isSink(sink) and
    source.getLocation() != sink.getLocation()
  select source, sink, "Possible SQL injection"
}
