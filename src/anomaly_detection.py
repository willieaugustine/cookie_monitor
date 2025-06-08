from pyspark.sql import functions as F

# Normal order = 1-5 cookies
# Bad order = 100+ cookies!
bad_orders = orders.filter(F.col("cookies") > 100)
