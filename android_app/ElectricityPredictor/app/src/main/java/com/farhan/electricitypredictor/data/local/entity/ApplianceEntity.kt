package com.farhan.electricitypredictor.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "appliances")
data class ApplianceEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val name: String,
    val powerRatingWatts: Float,
    val dailyUsageHours: Float,
    val category: String = "General",
    val quantity: Int = 1
)

