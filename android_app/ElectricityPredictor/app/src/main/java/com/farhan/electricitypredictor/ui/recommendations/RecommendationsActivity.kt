package com.farhan.electricitypredictor.ui.recommendations

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.farhan.electricitypredictor.ElectricityPredictorApp
import com.farhan.electricitypredictor.data.model.RecommendationItem
import com.farhan.electricitypredictor.databinding.ActivityRecommendationsBinding
import java.util.Locale

class RecommendationsActivity : AppCompatActivity() {

    private lateinit var binding: ActivityRecommendationsBinding
    private val app by lazy { application as ElectricityPredictorApp }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityRecommendationsBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.btnBackRecs.setOnClickListener { finish() }
        setupDynamicRecommendations()
    }

    private fun setupDynamicRecommendations() {
        app.applianceDao.getAllAppliances().observe(this) { appliances ->
            val tips = ArrayList<RecommendationItem>()
            val highConsumersBuilder = StringBuilder()

            var totalWattHours = 0f
            for (a in appliances) {
                totalWattHours += (a.powerRatingWatts * a.quantity * a.dailyUsageHours)
            }

            for (a in appliances) {
                val itemWattHours = (a.powerRatingWatts * a.quantity * a.dailyUsageHours)
                val percentage = if (totalWattHours > 0) (itemWattHours / totalWattHours) * 100f else 0f

                if (percentage >= 20f || a.powerRatingWatts >= 1000f) {
                    highConsumersBuilder.append(
                        String.format(
                            Locale.US,
                            "• %s: Consumes ~%.0f%% of household electricity load.\n",
                            a.name,
                            percentage
                        )
                    )
                }
            }

            if (highConsumersBuilder.isNotEmpty()) {
                binding.tvHighConsumersList.text = highConsumersBuilder.toString().trim()
            } else {
                binding.tvHighConsumersList.text = "No extreme high-load appliances detected. Load is well distributed."
            }

            // Tailored Energy Tips
            tips.add(
                RecommendationItem(
                    title = "AC Eco-Mode & Thermostat at 26°C",
                    potentialSavings = "Saves ~PKR 4,500 / month",
                    description = "Running AC at 26°C instead of 20°C reduces compressor workload significantly. Combine with a ceiling fan for maximum airflow.",
                    isHighPriority = true
                )
            )

            tips.add(
                RecommendationItem(
                    title = "Avoid Peak Hours (5 PM - 11 PM)",
                    potentialSavings = "Saves ~PKR 2,200 / month",
                    description = "Run water pumps, washing machines, and electric irons during off-peak morning hours when grid tariffs and voltage are optimal.",
                    isHighPriority = true
                )
            )

            tips.add(
                RecommendationItem(
                    title = "Defrost Refrigerator & Clean Coils",
                    potentialSavings = "Saves ~PKR 1,100 / month",
                    description = "Frost buildup of more than 5mm forces refrigerator compressors to consume 30% more electricity to maintain cooling.",
                    isHighPriority = false
                )
            )

            tips.add(
                RecommendationItem(
                    title = "Eliminate Phantom / Standby Power",
                    potentialSavings = "Saves ~PKR 850 / month",
                    description = "Turn off TV set-top boxes, microwave displays, and phone chargers at the main socket when not in use.",
                    isHighPriority = false
                )
            )

            tips.add(
                RecommendationItem(
                    title = "Stay Under Protected 300-Unit Slab",
                    potentialSavings = "Saves up to 25% on total bill",
                    description = "If your consumption crosses 300 units, the tariff tier switches to non-protected rates. Monitor consumption mid-month to stay under 300 units.",
                    isHighPriority = true
                )
            )

            binding.rvRecommendations.layoutManager = LinearLayoutManager(this)
            binding.rvRecommendations.adapter = RecommendationAdapter(tips)
        }
    }
}

