package com.farhan.electricitypredictor.ui.appliances

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.farhan.electricitypredictor.data.local.entity.ApplianceEntity
import com.farhan.electricitypredictor.databinding.ItemApplianceBinding
import java.util.Locale

class ApplianceAdapter(
    private val onEditClick: (ApplianceEntity) -> Unit,
    private val onDeleteClick: (ApplianceEntity) -> Unit
) : ListAdapter<ApplianceEntity, ApplianceAdapter.ApplianceViewHolder>(DiffCallback) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ApplianceViewHolder {
        val binding = ItemApplianceBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return ApplianceViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ApplianceViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    inner class ApplianceViewHolder(private val binding: ItemApplianceBinding) :
        RecyclerView.ViewHolder(binding.root) {

        fun bind(item: ApplianceEntity) {
            binding.tvApplianceName.text = item.name
            binding.tvApplianceSpecs.text = String.format(
                Locale.US,
                "%.0f Watts • %.1f hrs/day • Qty: %d",
                item.powerRatingWatts,
                item.dailyUsageHours,
                item.quantity
            )
            binding.tvApplianceCategory.text = item.category

            val monthlyUnits = (item.powerRatingWatts * item.quantity * item.dailyUsageHours * 30f) / 1000f
            binding.tvMonthlyKwh.text = String.format(Locale.US, "~%.1f kWh/mo", monthlyUnits)

            binding.btnEdit.setOnClickListener { onEditClick(item) }
            binding.btnDelete.setOnClickListener { onDeleteClick(item) }
        }
    }

    companion object {
        private val DiffCallback = object : DiffUtil.ItemCallback<ApplianceEntity>() {
            override fun areItemsTheSame(oldItem: ApplianceEntity, newItem: ApplianceEntity): Boolean {
                return oldItem.id == newItem.id
            }

            override fun areContentsTheSame(oldItem: ApplianceEntity, newItem: ApplianceEntity): Boolean {
                return oldItem == newItem
            }
        }
    }
}

