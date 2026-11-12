package com.farhan.electricitypredictor.tariff

data class BillBreakdown(
    val totalUnits: Float,
    val baseEnergyCost: Float,
    val fuelAdjustmentCost: Float,
    val govtTaxes: Float,
    val totalEstimatedBill: Float,
    val tariffSlabName: String
)

object ElectricityTariffEngine {

    /**
     * Pakistan DISCOs Standard Slabs Calculation (IESCO, LESCO, KE, etc.)
     * Protected and Unprotected Residential Categories
     */
    fun calculateBill(units: Float): BillBreakdown {
        var remainingUnits = units
        var baseCost = 0f
        val slabName: String

        when {
            units <= 100 -> {
                slabName = "Lifeline / Protected (0 - 100 Units)"
                baseCost = units * 16.50f
            }
            units <= 200 -> {
                slabName = "Protected (101 - 200 Units)"
                baseCost = (100 * 16.50f) + ((units - 100) * 22.95f)
            }
            units <= 300 -> {
                slabName = "Non-Protected (201 - 300 Units)"
                baseCost = (100 * 16.50f) + (100 * 22.95f) + ((units - 200) * 34.25f)
            }
            units <= 700 -> {
                slabName = "Medium Load (301 - 700 Units)"
                baseCost = (100 * 16.50f) + (100 * 22.95f) + (100 * 34.25f) + ((units - 300) * 42.80f)
            }
            else -> {
                slabName = "High Consumption Load (> 700 Units)"
                baseCost = (100 * 16.50f) + (100 * 22.95f) + (100 * 34.25f) + (400 * 42.80f) + ((units - 700) * 48.50f)
            }
        }

        // Fuel Price Adjustment (FPA) ~ Rs 4.50 per unit average
        val fuelAdjustment = units * 4.50f

        // Taxes (Electricity Duty + General Sales Tax ~ 18%)
        val govtTaxes = (baseCost + fuelAdjustment) * 0.18f

        val totalBill = baseCost + fuelAdjustment + govtTaxes

        return BillBreakdown(
            totalUnits = units,
            baseEnergyCost = baseCost,
            fuelAdjustmentCost = fuelAdjustment,
            govtTaxes = govtTaxes,
            totalEstimatedBill = totalBill,
            tariffSlabName = slabName
        )
    }

    /**
     * Calculates appliance-wise monthly cost breakdown
     */
    fun calculateApplianceCost(wattage: Float, dailyHours: Float, totalMonthlyBill: Float, totalPredictedUnits: Float): Float {
        if (totalPredictedUnits <= 0f) return 0f
        val monthlyUnits = (wattage * dailyHours * 30f) / 1000f
        val perUnitAvgRate = totalMonthlyBill / totalPredictedUnits
        return monthlyUnits * perUnitAvgRate
    }
}

