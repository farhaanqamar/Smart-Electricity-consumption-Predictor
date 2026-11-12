package com.farhan.electricitypredictor.data.local.dao

import androidx.lifecycle.LiveData
import androidx.room.*
import com.farhan.electricitypredictor.data.local.entity.HistoricalBillEntity

@Dao
interface HistoricalBillDao {
    @Query("SELECT * FROM historical_bills ORDER BY recordTimestamp DESC")
    fun getAllBills(): LiveData<List<HistoricalBillEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertBill(bill: HistoricalBillEntity): Long

    @Delete
    suspend fun deleteBill(bill: HistoricalBillEntity)

    @Query("SELECT unitsConsumed FROM historical_bills ORDER BY recordTimestamp DESC LIMIT 1")
    suspend fun getLastMonthUnits(): Float?

    @Query("SELECT AVG(unitsConsumed) FROM (SELECT unitsConsumed FROM historical_bills ORDER BY recordTimestamp DESC LIMIT 3)")
    suspend fun getAverageUnitsPast3Months(): Float?

    @Query("SELECT COUNT(*) FROM historical_bills")
    suspend fun getCount(): Int
}

