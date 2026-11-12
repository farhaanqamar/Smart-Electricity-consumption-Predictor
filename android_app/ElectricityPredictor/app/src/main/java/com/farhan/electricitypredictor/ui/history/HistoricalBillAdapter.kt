package com.farhan.electricitypredictor.ui.history

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.farhan.electricitypredictor.data.local.entity.HistoricalBillEntity
import com.farhan.electricitypredictor.databinding.ItemHistoryBillBinding
import java.util.Locale

class HistoricalBillAdapter(
    private val onDeleteClick: (HistoricalBillEntity) -> Unit
) : ListAdapter<HistoricalBillEntity, HistoricalBillAdapter.BillViewHolder>(DiffCallback) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): BillViewHolder {
        val binding = ItemHistoryBillBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return BillViewHolder(binding)
    }

    override fun onBindViewHolder(holder: BillViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    inner class BillViewHolder(private val binding: ItemHistoryBillBinding) :
        RecyclerView.ViewHolder(binding.root) {

        fun bind(item: HistoricalBillEntity) {
            binding.tvMonthName.text = item.monthName
            binding.tvUnitsConsumed.text = String.format(Locale.US, "%.0f kWh Units", item.unitsConsumed)
            binding.tvBillAmountPkr.text = String.format(Locale.US, "PKR %,.0f", item.billAmountPkr)
            binding.btnDeleteBill.setOnClickListener { onDeleteClick(item) }
        }
    }

    companion object {
        private val DiffCallback = object : DiffUtil.ItemCallback<HistoricalBillEntity>() {
            override fun areItemsTheSame(oldItem: HistoricalBillEntity, newItem: HistoricalBillEntity): Boolean {
                return oldItem.id == newItem.id
            }

            override fun areContentsTheSame(oldItem: HistoricalBillEntity, newItem: HistoricalBillEntity): Boolean {
                return oldItem == newItem
            }
        }
    }
}

