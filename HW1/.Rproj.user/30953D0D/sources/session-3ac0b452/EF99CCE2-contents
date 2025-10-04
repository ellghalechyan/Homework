library(readxl)
library(diffusion)
library(ggplot2)


bike <- read_excel("data/EU_sales.xlsx", sheet = "Data", skip = 4, col_names = FALSE)
colnames(bike) <- c("Year", "Sales")

sales <- bike$Sales
years <- bike$Year
t <- 1:length(sales)  

# Bass Model parameters 

bass_m <- nls(
  sales ~ m * (((p+q)^2/p) * exp(-(p+q)*t) / (1 + (q/p) * exp(-(p+q)*t))^2),
  data = bike,
  start = list(m = sum(sales), p = 0.03, q = 0.38)
)

params <- coef(bass_m)
m <- params["m"]  # Market potential
p <- params["p"]  # Coefficient of innovation
q <- params["q"]  # Coefficient of imitation

cat("Estimated Bass Model parameters\n")
cat(sprintf("m (market potential) = %.2f million\np = %.4f\nq = %.4f\n", m, p, q))

# Diffusion of innovation

years_future <- 2015:2030
t_future <- 1:length(years_future)


predicted_sales <- m * (((p+q)^2/p) * exp(-(p+q)*t_future) /
                          (1 + (q/p) * exp(-(p+q)*t_future))^2)


cumulative_adopters <- m * (1 - exp(-(p+q)*t_future)) /
  (1 + (q/p) * exp(-(p+q)*t_future))


forecast_df <- data.frame(
  year = years_future,
  annual_sales_pred = predicted_sales,
  cumulative_adopters = cumulative_adopters
)

forecast_df$annual_sales_real <- NA
forecast_df$annual_sales_real[1:length(sales)] <- sales

# Estimate annual adopters 

annual_adopters <- diff(c(0, cumulative_adopters))  
forecast_df$annual_adopters <- annual_adopters


write.csv(forecast_df, "data/bimotal_forecast.csv", row.names = FALSE)
params_df <- data.frame(param = names(params), estimate = as.numeric(params))
write.csv(params_df, "data/bass_params.csv", row.names = FALSE)


ggplot(forecast_df, aes(x = year)) +
  geom_line(aes(y = annual_sales_pred), color = "red", size = 1, linetype="dashed") +
  geom_point(aes(y = annual_sales_real), color = "blue", size = 2) +
  labs(title = "Bass Model vs Observed Sales",
       x = "Year", y = "Annual Sales (millions)",
       caption = "Red dashed = Bass forecast; Blue points = Observed data") +
  theme_minimal()


ggplot(forecast_df, aes(x = year, y = annual_adopters)) +
  geom_line(color = "red", size = 1) +
  labs(title = "Annual Bimotal Adoption Forecast",
       x = "Year", y = "Annual Adopters") +
  theme_minimal()


