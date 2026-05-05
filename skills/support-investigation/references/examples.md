# Support Investigation: Examples & Methodology

## Phase 3: Five Whys Examples

### Connectivity Error
- **Surface error:** "Payment processing failed — internal error"
- **Why?** External service call timed out after 30s
- **Why?** Connection to payment gateway refused
- **Why?** Firewall blocks outbound port 443 from the app server
- **Why?** Network team changed the security group last week
- **Actionable:** Customer IT to restore the outbound firewall rule

### Data Consistency Error
- **Surface error:** "NullPointerException in CalculationEngine"
- **Why?** `tax_rate` variable returned null
- **Why?** `TaxRegion` lookup failed for region 'XYZ'
- **Why?** Region 'XYZ' is missing from the `TAX_CONFIG` table
- **Why?** New region added in source system but not synced to app
- **Actionable:** Data fix to add region 'XYZ' to `TAX_CONFIG`

## Phase 4: Error Category Decision Tree

| If logs show... | Category | Focus |
|---|---|---|
| Timeout, refused, unknown host | **Connectivity** | Reachability, hostnames, network, credentials |
| Null pointer, "not found", empty set | **Data/Config** | Missing records, reference data, relationships |
| Business rule failure, validation error | **Business Logic** | Values vs rules, ranges, required fields |
| Permission, 401, 403, "Access Denied" | **Security** | Roles, credentials, API tokens |
| OutOfMemory, slow query, high CPU | **Performance** | Execution time, data volume, index usage |
| Unexpected state, wrong status | **Workflow** | Entity status, recent updates, concurrency |
| No log error, "works as designed" | **Expectation** | Doc confirmation, user education, feature request |
