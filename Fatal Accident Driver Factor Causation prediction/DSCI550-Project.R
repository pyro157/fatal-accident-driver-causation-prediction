#Import Packages
library(dplyr)
library(ggplot2)
library(readr)
library(tidyverse)
library(RCurl)

vehicle <- read.csv("vehicle.csv")
accident <- read.csv("accident.csv")
person <- read.csv("person.csv")
driveerrf <- read.csv("driverrf.csv")

options(scipen = 999)

#Death per month
deathPerMonth <- aggregate(vehicle$DEATHS, by = list(vehicle$MONTH), sum)
names(deathPerMonth)[names(deathPerMonth) == "Group.1"] <- "Month"
names(deathPerMonth)[names(deathPerMonth) == "x"] <- "Death"
deathPerMonth <- tapply(vehicle$DEATHS, list(vehicle$MONTH), sum)

barplot(deathPerMonth, beside = TRUE, legend.text = rownames("Month"), xlab = "Months", ylab = " total death"
        , col = c( "orange"), main = "Total death per month")

#total death per Make per Country
deathCar <- aggregate(vehicle$DEATHS, by = list(vehicle$MAKENAME), sum)
names(deathCar)[names(deathCar) == "Group.1"] <- "Make"
names(deathCar)[names(deathCar) == "x"] <- "Death"

deathCar <- deathCar %>%
  mutate(country_brand = case_when(
    Make %in% c("Buick / Opel", "Cadillac", "Dodge", "Chrysler", "Ford", "Chevrolet", "GMC", "Jeep / Kaiser-Jeep / Willys-Jeep", "Lincoln", "Harley-Davidson", "Pontiac") ~ "USA",
    Make %in% c("Acura", "Honda", "Toyota", "Infiniti", "Lexus", "Mazda", "Nissan/Datsun", "Mitsubishi", "Subaru", "Yamaha") ~ "Japan",
    Make %in% c("Audi", "BMW", "Mercedes-Benz", "Porsche", "Volkswagen", "Ducati") ~ "Germany",
    Make %in% c("Alfa Romeo", "Fiat", "Volvo", "Jaguar", "Land Rover") ~ "Europe",
    Make %in% c("Hyundai", "Kia") ~ "South Korea",
    Make %in% c("Other Make", "Unknown Make") ~ "Others"
  ))
deathCar <- na.omit(deathCar)
deathCar <- tapply(deathCar$Death, list(deathCar$country_brand), sum)
barplot(deathCar, beside = TRUE, legend.text = rownames("Car Brand"), xlab = "Makes", ylab = " total death"
        , col = c( "lightblue"), main = "Total death per Car Brand")

#DUI vs Death
drunk <- aggregate(accident$FATALS, by = list(accident$DRUNK_DR, accident$MONTH), sum)
names(drunk)[names(drunk) == "Group.1"] <- "drunk_dr"
names(drunk)[names(drunk) == "Group.2"] <- "Month"
names(drunk)[names(drunk) == "x"] <- "Fatal"
drunk <- drunk %>%
  mutate(is_drunk = case_when(
    drunk_dr %in% "0" ~ "Not drunk",
    drunk_dr %in% c("1","2", "3","4") ~ "Drunk"))

drunk <- tapply(drunk$Fatal, list(drunk$is_drunk, drunk$Month), sum)
bar1 <- barplot(drunk, beside = TRUE, legend.text = rownames("DUI"), xlab = "Month", ylab = " total death"
        , col = c("orange", "lightblue"), main = "Total death with DUI")

avg_drunk <- rowMeans(drunk)

for (i in seq_along(avg_drunk)) {
  axis(1, at = bar1[i, ], labels = FALSE, tick = FALSE, lty = "solid", lwd = 2, col = c("red", "blue")[i])
  lines(c(bar1[i, 1], bar1[i, ncol(drunk)]), rep(avg_drunk[i], 2), col = c("red", "blue")[i], lwd = 2)
}

legend("topright", legend = c("Avg Not Drunk", "Avg Drunk"), col = c("red", "blue"), lwd = 2)


# Driverrf

par(mfrow = c(1, 2))

road <- sum(driveerrf$DRIVERRF == c("81", "82", "83", "87"))
traffic <- sum(driveerrf$DRIVERRF == c("37", "16", "84", "95", "96", "86", "97"))
internalPerson <- sum(driveerrf$DRIVERRF == c("8", "10", "12", "13", "36"))
externalPerson <- sum(driveerrf$DRIVERRF == c("4", "60", "73", "74", "94", "19", "53", "91"))
weather <- sum(driveerrf$DRIVERRF == c("77", "78", "79"))
carIssue <- sum(driveerrf$DRIVERRF == c("21", "22", "57", "80", "85", "88"))
Operation <- sum(driveerrf$DRIVERRF == c("6", "15", "20", "23", "24", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "38", "39", "40", "41", "42", "45", "48", "50", "51", "54", "56", "58", "59", "89", "52", "18"))
driverRF <- data.frame(road, traffic, internalPerson, externalPerson, weather, carIssue, Operation)
driverRF <- as.matrix(driverRF)
barplot(driverRF, beside = TRUE, legend.text = colnames(driverRF), xlab = "Factors", ylab = "total"
        , col = c( "yellow", "green", "lightblue", "red", "purple", "orange", "pink"), main = "Driver Related Factors")

total <- sum(driverRF)

# Calculate the proportions
proportions <- driverRF / total

# Create percentage labels
percentage_labels <- paste(round(proportions * 100, 1), "%", sep = "")

# Create a pie chart with the percentage labels
pie(driverRF, labels = percentage_labels, main = "Driver Related Factors", col = c( "yellow", "green", "lightblue", "red", "purple", "orange", "pink"))
legend("topright", legend.text = colnames(driverRF), bty = "n", cex = 0.8)
