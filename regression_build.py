##### Run a regression model #####
X = df[["Beds", "Baths","Area"]]
y = df["Price"]

# Note the difference in argument order
model = sm.OLS(y, X).fit()

# make the predictions by the model
predictions = model.predict(X) 

# Print out the statistics
model.summary()


from statsmodels.formula.api import ols

fit = ols('Price ~ C(Type) + C(BER) + C(Town) + C(County) + Baths + Beds + Area', data=df).fit() 

fit.summary()