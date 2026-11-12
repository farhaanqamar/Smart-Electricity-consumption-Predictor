package com.farhan.electricitypredictor.ui.history

import android.app.Dialog
import android.graphics.Color
import android.graphics.drawable.ColorDrawable
import android.os.Bundle
import android.view.Window
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import com.farhan.electricitypredictor.ElectricityPredictorApp
import com.farhan.electricitypredictor.R
import com.farhan.electricitypredictor.data.local.entity.HistoricalBillEntity
import com.farhan.electricitypredictor.databinding.ActivityHistoryBinding
import com.farhan.electricitypredictor.databinding.DialogAddHistoryBinding
import com.github.mikephil.charting.components.XAxis
import com.github.mikephil.charting.data.BarData
import com.github.mikephil.charting.data.BarDataSet
import com.github.mikephil.charting.data.BarEntry
import com.github.mikephil.charting.formatter.IndexAxisValueFormatter
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.util.Locale

class HistoryActivity : AppCompatActivity() {

    private lateinit var binding: ActivityHistoryBinding
    private lateinit var adapter: HistoricalBillAdapter
    private val app by lazy { application as ElectricityPredictorApp }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityHistoryBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupRecyclerView()
        setupListeners()
        observeData()
    }

    private fun setupRecyclerView() {
        adapter = HistoricalBillAdapter(
            onDeleteClick = { bill -> deleteBill(bill) }
        )
        binding.rvHistoryBills.layoutManager = LinearLayoutManager(this)
        binding.rvHistoryBills.adapter = adapter
    }

    private fun setupListeners() {
        binding.btnBackHistory.setOnClickListener { finish() }
        binding.btnAddHistoryTop.setOnClickListener { showAddBillDialog() }
        binding.btnAddPastBill.setOnClickListener { showAddBillDialog() }
    }

    private fun observeData() {
        app.historicalBillDao.getAllBills().observe(this) { bills ->
            adapter.submitList(bills)

            if (bills.isNotEmpty()) {
                val lastMonth = bills.first().unitsConsumed
                binding.tvLastMonthUnits.text = String.format(Locale.US, "%.0f kWh", lastMonth)

                val recentThree = bills.take(3)
                val avgThree = recentThree.map { it.unitsConsumed }.average().toFloat()
                binding.tvPast3MonthsAvg.text = String.format(Locale.US, "%.0f kWh", avgThree)

                updateChart(bills)
            } else {
                binding.tvLastMonthUnits.text = "0 kWh"
                binding.tvPast3MonthsAvg.text = "0 kWh"
                binding.barChartHistory.clear()
            }
        }
    }

    private fun updateChart(bills: List<HistoricalBillEntity>) {
        val chart = binding.barChartHistory
        val reversed = bills.take(6).reversed()

        val entries = ArrayList<BarEntry>()
        val labels = ArrayList<String>()

        for ((index, bill) in reversed.withIndex()) {
            entries.add(BarEntry(index.toFloat(), bill.unitsConsumed))
            val shortLabel = bill.monthName.split(" ").firstOrNull() ?: "M$index"
            labels.add(shortLabel)
        }

        val dataSet = BarDataSet(entries, "Monthly Units (kWh)")
        dataSet.color = ContextCompat.getColor(this, R.color.ke_orange_accent)
        dataSet.valueTextColor = ContextCompat.getColor(this, R.color.text_title)
        dataSet.valueTextSize = 10f

        val barData = BarData(dataSet)
        barData.barWidth = 0.5f

        chart.data = barData
        chart.description.isEnabled = false
        chart.legend.textColor = ContextCompat.getColor(this, R.color.text_muted)
        chart.setDrawGridBackground(false)
        chart.setFitBars(true)

        val xAxis = chart.xAxis
        xAxis.position = XAxis.XAxisPosition.BOTTOM
        xAxis.valueFormatter = IndexAxisValueFormatter(labels)
        xAxis.textColor = ContextCompat.getColor(this, R.color.text_muted)
        xAxis.setDrawGridLines(false)
        xAxis.granularity = 1f

        chart.axisLeft.textColor = ContextCompat.getColor(this, R.color.text_muted)
        chart.axisRight.isEnabled = false
        chart.animateY(800)
        chart.invalidate()
    }

    private fun showAddBillDialog() {
        val dialog = Dialog(this)
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE)
        val dBinding = DialogAddHistoryBinding.inflate(layoutInflater)
        dialog.setContentView(dBinding.root)
        dialog.window?.setBackgroundDrawable(ColorDrawable(Color.TRANSPARENT))
        dialog.window?.setLayout(
            (resources.displayMetrics.widthPixels * 0.90).toInt(),
            android.view.ViewGroup.LayoutParams.WRAP_CONTENT
        )

        dBinding.btnCancelHistory.setOnClickListener { dialog.dismiss() }

        dBinding.btnSaveHistory.setOnClickListener {
            val month = dBinding.etBillingMonth.text.toString().trim()
            val unitsStr = dBinding.etUnitsConsumed.text.toString().trim()
            val billStr = dBinding.etBillPaidPkr.text.toString().trim()

            if (month.isEmpty() || unitsStr.isEmpty() || billStr.isEmpty()) {
                Toast.makeText(this, "Please fill in all fields", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            val units = unitsStr.toFloatOrNull()
            val billPkr = billStr.toFloatOrNull()

            if (units == null || units <= 0f) {
                Toast.makeText(this, "Enter valid positive units", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            if (billPkr == null || billPkr <= 0f) {
                Toast.makeText(this, "Enter valid bill amount", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            lifecycleScope.launch(Dispatchers.IO) {
                val newBill = HistoricalBillEntity(
                    monthName = month,
                    unitsConsumed = units,
                    billAmountPkr = billPkr
                )
                app.historicalBillDao.insertBill(newBill)

                withContext(Dispatchers.Main) {
                    dialog.dismiss()
                    Toast.makeText(this@HistoryActivity, "Monthly bill record saved", Toast.LENGTH_SHORT).show()
                }
            }
        }

        dialog.show()
    }

    private fun deleteBill(bill: HistoricalBillEntity) {
        lifecycleScope.launch(Dispatchers.IO) {
            app.historicalBillDao.deleteBill(bill)
            withContext(Dispatchers.Main) {
                Toast.makeText(this@HistoryActivity, "Removed ${bill.monthName}", Toast.LENGTH_SHORT).show()
            }
        }
    }
}

