package com.farhan.electricitypredictor.ui.recommendations

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.farhan.electricitypredictor.data.model.RecommendationItem
import com.farhan.electricitypredictor.databinding.ItemRecommendationBinding

class RecommendationAdapter(
    private val items: List<RecommendationItem>
) : RecyclerView.Adapter<RecommendationAdapter.ViewHolder>() {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val binding = ItemRecommendationBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return ViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.bind(items[position])
    }

    override fun getItemCount(): Int = items.size

    inner class ViewHolder(private val binding: ItemRecommendationBinding) :
        RecyclerView.ViewHolder(binding.root) {

        fun bind(item: RecommendationItem) {
            binding.tvTipTitle.text = item.title
            binding.tvTipSavings.text = item.potentialSavings
            binding.tvTipDescription.text = item.description
        }
    }
}

