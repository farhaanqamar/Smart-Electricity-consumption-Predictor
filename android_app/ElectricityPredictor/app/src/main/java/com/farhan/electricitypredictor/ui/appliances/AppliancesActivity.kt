package com.farhan.electricitypredictor.ui.appliances

import android.app.Dialog
import android.graphics.Color
import android.graphics.drawable.ColorDrawable
import android.os.Bundle
import android.view.Window
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import com.farhan.electricitypredictor.ElectricityPredictorApp
import com.farhan.electricitypredictor.data.local.entity.ApplianceEntity
import com.farhan.electricitypredictor.databinding.ActivityAppliancesBinding
import com.farhan.electricitypredictor.databinding.DialogAddApplianceBinding
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.util.Locale

class AppliancesActivity : AppCompatActivity() {

    private lateinit var binding: ActivityAppliancesBinding
    private lateinit var adapter: ApplianceAdapter
    private val app by lazy { application as ElectricityPredictorApp }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityAppliancesBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupRecyclerView()
        setupListeners()
        observeData()
    }

    private fun setupRecyclerView() {
        adapter = ApplianceAdapter(
            onEditClick = { appliance -> showApplianceDialog(appliance) },
            onDeleteClick = { appliance -> deleteAppliance(appliance) }
        )
        binding.rvAppliances.layoutManager = LinearLayoutManager(this)
        binding.rvAppliances.adapter = adapter
    }

    private fun setupListeners() {
        binding.btnBack.setOnClickListener { finish() }
        binding.btnAddApplianceTop.setOnClickListener { showApplianceDialog(null) }
        binding.btnAddNewAppliance.setOnClickListener { showApplianceDialog(null) }
    }

    private fun observeData() {
        app.applianceDao.getAllAppliances().observe(this) { list ->
            adapter.submitList(list)

            var totalWatts = 0f
            var totalItems = 0
            for (item in list) {
                totalWatts += (item.powerRatingWatts * item.quantity)
                totalItems += item.quantity
            }

            binding.tvTotalWatts.text = String.format(Locale.US, "%.0f W (%.2f kW)", totalWatts, totalWatts / 1000f)
            binding.tvApplianceTotalCount.text = String.format(Locale.US, "%d Items", totalItems)
        }
    }

    private fun showApplianceDialog(existing: ApplianceEntity?) {
        val dialog = Dialog(this)
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE)
        val dBinding = DialogAddApplianceBinding.inflate(layoutInflater)
        dialog.setContentView(dBinding.root)
        dialog.window?.setBackgroundDrawable(ColorDrawable(Color.TRANSPARENT))
        dialog.window?.setLayout(
            (resources.displayMetrics.widthPixels * 0.90).toInt(),
            android.view.ViewGroup.LayoutParams.WRAP_CONTENT
        )

        if (existing != null) {
            dBinding.tvDialogTitle.text = "Edit Appliance"
            dBinding.etApplianceName.setText(existing.name)
            dBinding.etPowerWatts.setText(existing.powerRatingWatts.toString())
            dBinding.etDailyHours.setText(existing.dailyUsageHours.toString())
            dBinding.etQuantity.setText(existing.quantity.toString())
            dBinding.etCategory.setText(existing.category)
            dBinding.btnSaveAppliance.text = "Update Appliance"
        }

        dBinding.btnCancel.setOnClickListener { dialog.dismiss() }

        dBinding.btnSaveAppliance.setOnClickListener {
            val name = dBinding.etApplianceName.text.toString().trim()
            val wattsStr = dBinding.etPowerWatts.text.toString().trim()
            val hoursStr = dBinding.etDailyHours.text.toString().trim()
            val qtyStr = dBinding.etQuantity.text.toString().trim()
            val category = dBinding.etCategory.text.toString().trim().ifEmpty { "General" }

            if (name.isEmpty() || wattsStr.isEmpty() || hoursStr.isEmpty()) {
                Toast.makeText(this, "Please fill in all required fields", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            val watts = wattsStr.toFloatOrNull()
            val hours = hoursStr.toFloatOrNull()
            val qty = qtyStr.toIntOrNull() ?: 1

            if (watts == null || watts <= 0f) {
                Toast.makeText(this, "Enter valid positive wattage (Watts)", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            if (hours == null || hours < 0.1f || hours > 24f) {
                Toast.makeText(this, "Daily hours must be between 0.1 and 24 hours", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            lifecycleScope.launch(Dispatchers.IO) {
                if (existing == null) {
                    val newEntity = ApplianceEntity(
                        name = name,
                        powerRatingWatts = watts,
                        dailyUsageHours = hours,
                        category = category,
                        quantity = qty
                    )
                    app.applianceDao.insertAppliance(newEntity)
                } else {
                    val updatedEntity = existing.copy(
                        name = name,
                        powerRatingWatts = watts,
                        dailyUsageHours = hours,
                        category = category,
                        quantity = qty
                    )
                    app.applianceDao.updateAppliance(updatedEntity)
                }

                withContext(Dispatchers.Main) {
                    dialog.dismiss()
                    Toast.makeText(
                        this@AppliancesActivity,
                        if (existing == null) "Appliance added" else "Appliance updated",
                        Toast.LENGTH_SHORT
                    ).show()
                }
            }
        }

        dialog.show()
    }

    private fun deleteAppliance(appliance: ApplianceEntity) {
        lifecycleScope.launch(Dispatchers.IO) {
            app.applianceDao.deleteAppliance(appliance)
            withContext(Dispatchers.Main) {
                Toast.makeText(this@AppliancesActivity, "Removed ${appliance.name}", Toast.LENGTH_SHORT).show()
            }
        }
    }
}

