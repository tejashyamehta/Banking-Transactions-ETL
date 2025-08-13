-- Example analytics
.headers on
.mode column

SELECT merchant_category, COUNT(*) AS txn_count, ROUND(AVG(amount_inr),2) AS avg_amount
FROM transactions_clean
GROUP BY 1
ORDER BY txn_count DESC
LIMIT 10;

SELECT COUNT(*) AS high_value_txns
FROM transactions_clean
WHERE is_high_value = 1;

SELECT reason, COUNT(*) AS n
FROM transaction_anomalies
GROUP BY 1
ORDER BY n DESC;
