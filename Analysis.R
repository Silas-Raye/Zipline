library(readr)

# Read the CSV file
data <- read.csv("weekday_data.csv")

# Convert columns to factors
data$IsRushHr <- factor(data$IsRushHr)
data$Is352 <- factor(data$Is352)

# Filter out wait times less than 0 or greater than 120
data <- data[data$WaitTime >= 0 & data$WaitTime <= 120, ]

# Perform linear regression
model <- lm(WaitTime ~ NumOpenTickets + IsRushHr + Is352 + NumSilces + NumMed + NumLrg + NumPan + NumZone + NumMFP, data=data)

# Print the summary of the regression model
summary(model)

# --------------
library(corrplot)

# Calculate correlation matrix
correlation_matrix <- cor(data[, c("NumOpenTickets", "IsLse", "Is352", "NumSilces", "NumMed", "NumLrg", "NumPan", "NumZone")])

# Plot correlation matrix
corrplot(correlation_matrix, method="circle", type="upper", tl.col="black", tl.srt=45)

# --------------
library(glmnet)

# Convert the data frame to a matrix
X <- model.matrix(WaitTime ~ NumOpenTickets + IsRushHr + Is352 + NumSilces + NumMed + NumLrg + NumPan + NumZone + NumMFP, data=data)
y <- data$WaitTime

# Fit the Lasso regression model
lasso_model <- cv.glmnet(X, y, alpha=1)  # alpha=1 specifies Lasso regression

# Print the summary of the Lasso regression model
print(lasso_model)

# Plot the cross-validation curve to choose the best lambda
plot(lasso_model)

# Get the best lambda value chosen by cross-validation
best_lambda <- lasso_model$lambda.min
cat("Best lambda value chosen by cross-validation:", best_lambda, "\n")

# Refit the model with the best lambda
lasso_model_best_lambda <- glmnet(X, y, alpha=1, lambda=best_lambda)

# Print the coefficients of the Lasso model
print(coef(lasso_model_best_lambda))

# Generate predictions using the Lasso regression model
predictions <- predict(lasso_model_best_lambda, newx = X, s = best_lambda)

# Calculate the mean of the observed WaitTime
y_mean <- mean(y)

# Calculate the total sum of squares (TSS)
TSS <- sum((y - y_mean)^2)

# Calculate the residual sum of squares (RSS)
RSS <- sum((y - predictions)^2)

# Calculate R-squared (coefficient of determination)
R_squared <- 1 - (RSS / TSS)

cat("R-squared (coefficient of determination):", R_squared, "\n")
