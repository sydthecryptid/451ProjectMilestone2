(6%) Calculate and update the “numCheckins”, “reviewcount”, and “reviewrating” attributes for each
business.
 “numCheckins” value for a business should be updated to the sum of all check-in counts for that
business. Similarly, “reviewcount” should be updated to the number of reviews provided for that
business (Note that you will overwrite the values extracted from the JSON data). “reviewrating” is
the average of the review star ratings provided for each business. You should query the review table
to calculate the number of reviews and avg review rating for each business. Similarly, you should
query the check-in table to calculate the total number of check-ins. In grading, points will be
deducted if you don’t update these values.