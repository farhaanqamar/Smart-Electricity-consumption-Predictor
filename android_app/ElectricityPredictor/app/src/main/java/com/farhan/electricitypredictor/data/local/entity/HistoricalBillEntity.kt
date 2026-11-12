package com.farhan.electricitypredictor.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "historical_bills")
data class HistoricalBillEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val monthName: String,
    val unitsConsumed: Float,
    val billAmountPkr: Float,
    val recordTimestamp: Long = System.currentTimeMillis()
)

