package com.farhan.electricitypredictor.data.model

data class RecommendationItem(
    val title: String,
    val potentialSavings: String,
    val description: String,
    val isHighPriority: Boolean = false
)

