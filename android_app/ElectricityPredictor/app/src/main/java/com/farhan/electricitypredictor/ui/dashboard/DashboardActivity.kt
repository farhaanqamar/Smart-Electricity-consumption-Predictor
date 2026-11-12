package com.farhan.electricitypredictor.ui.dashboard

import android.app.Dialog
import android.content.Intent
import android.graphics.Color
import android.graphics.drawable.ColorDrawable
import android.os.Bundle
import android.view.Window
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.farhan.electricitypredictor.ElectricityPredictorApp
import com.farhan.electricitypredictor.R
import com.farhan.electricitypredictor.databinding.ActivityDashboardBinding
import com.farhan.electricitypredictor.ml.ElectricityPredictorClient
import com.farhan.electricitypredictor.tariff.ElectricityTariffEngine
import com.farhan.electricitypredictor.ui.appliances.AppliancesActivity
import com.farhan.electricitypredictor.ui.history.HistoryActivity
import com.farhan.electricitypredictor.ui.recommendations.RecommendationsActivity
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.util.Locale

class DashboardActivity : AppCompatActivity() {

    private lateinit var binding: ActivityDashboardBinding
    private lateinit var predictorClient: ElectricityPredictorClient
    private val app by lazy { application as ElectricityPredictorApp }

    private var currentPredictedUnits: Float = 0f
    private var currentEstimatedBill: Float = 0f

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityDashboardBinding.inflate(layoutInflater)
        setContentView(binding.root)

        predictorClient = ElectricityPredictorClient(this)

        setupListeners()
        observeAndPredict()
    }

    private fun setupListeners() {
        binding.cardManageAppliances.setOnClickListener {
            startActivity(Intent(this, AppliancesActivity::class.java))
        }

        binding.cardHistoricalData.setOnClickListener {
            startActivity(Intent(this, HistoryActivity::class.java))
        }

        binding.btnViewBreakdown.setOnClickListener {
            showTariffBreakdownDialog()
        }

        binding.tvHeroSmartAlert.setOnClickListener {
            startActivity(Intent(this, RecommendationsActivity::class.java))
        }

        binding.ivNotifications.setOnClickListener {
            startActivity(Intent(this, RecommendationsActivity::class.java))
        }
    }

    private fun observeAndPredict() {
        app.applianceDao.getAllAppliances().observe(this) { appliances ->
            var totalWatts = 0f
            var totalWeightedHours = 0f
            var totalCount = 0

            for (a in appliances) {
                val itemWatts = a.powerRatingWatts * a.quantity
                totalWatts += itemWatts
                totalWeightedHours += (a.dailyUsageHours * itemWatts)
                totalCount += a.quantity
            }

            val avgDailyHours = if (totalWatts > 0f) totalWeightedHours / totalWatts else 6.0f
            binding.tvAppliancesCount.text = "$totalCount Connected"

            lifecycleScope.launch(Dispatchers.IO) {
                val lastMonthUnits = app.historicalBillDao.getLastMonthUnits() ?: 350f
                val past3mAvg = app.historicalBillDao.getAverageUnitsPast3Months() ?: 340f

                // Run Machine Learning inference on phone via TensorFlow Lite (.tflite)
                val predictedKwh = predictorClient.predictConsumption(
                    totalWatts = if (totalWatts > 0f) totalWatts else 4500f,
                    dailyHours = avgDailyHours,
                    pastMonthUnits = lastMonthUnits,
                    past3MonthAvgUnits = past3mAvg,
                    seasonFactor = 3.0f, // Peak Season
                    householdMembers = 5.0f
                )

                // Run Tariff Engine to calculate bill & slabs
                val breakdown = ElectricityTariffEngine.calculateBill(predictedKwh)

                withContext(Dispatchers.Main) {
                    currentPredictedUnits = predictedKwh
                    currentEstimatedBill = breakdown.totalEstimatedBill

                    binding.tvPredictedUnits.text = String.format(Locale.US, "%.1f kWh", predictedKwh)
                    binding.tvPastUnits.text = String.format(Locale.US, "%.0f kWh", lastMonthUnits)
                    binding.tvPredictedBillPkr.text = String.format(Locale.US, "PKR %,.0f", breakdown.totalEstimatedBill)

                    binding.tvTariffCategory.text = "Current Category: ${breakdown.tariffSlabName}"

                    if (predictedKwh > 300f) {
                        binding.tvHeroSmartAlert.text = "Alert: Usage exceeds 300 units slab. Tap here for savings tips."
                    } else {
                        binding.tvHeroSmartAlert.text = "Excellent: Your usage is within the protected lifeline tier."
                    }
                }
            }
        }
    }

    private fun showTariffBreakdownDialog() {
        val breakdown = ElectricityTariffEngine.calculateBill(currentPredictedUnits)
        val dialog = Dialog(this)
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE)
        dialog.setContentView(R.layout.dialog_add_appliance) // Reuse window style or build simple layout
        dialog.window?.setBackgroundDrawable(ColorDrawable(Color.TRANSPARENT))

        val textView = TextView(this).apply {
            setPadding(40, 40, 40, 40)
            setTextColor(Color.WHITE)
            setBackgroundResource(R.drawable.bg_card_rounded)
            backgroundTintList = getColorStateList(R.color.bg_surface_elevated)
            textSize = 14f
            text = """
                📊 TARIFF & BILL BREAKDOWN
                -----------------------------------
                Predicted Units: ${String.format(Locale.US, "%.1f kWh", breakdown.totalUnits)}
                Tariff Tier: ${breakdown.tariffSlabName}
                
                • Base Energy Cost: PKR ${String.format(Locale.US, "%,.0f", breakdown.baseEnergyCost)}
                • Fuel Adjustment (FPA): PKR ${String.format(Locale.US, "%,.0f", breakdown.fuelAdjustmentCost)}
                • Govt Duty & Taxes (18%): PKR ${String.format(Locale.US, "%,.0f", breakdown.govtTaxes)}
                -----------------------------------
                TOTAL ESTIMATED: PKR ${String.format(Locale.US, "%,.0f", breakdown.totalEstimatedBill)}
            """.trimIndent()
        }
        dialog.setContentView(textView)
        dialog.show()
    }

    override fun onDestroy() {
        super.onDestroy()
        predictorClient.close()
    }
}

