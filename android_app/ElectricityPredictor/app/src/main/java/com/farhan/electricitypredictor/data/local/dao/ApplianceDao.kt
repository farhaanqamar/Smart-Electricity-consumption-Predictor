package com.farhan.electricitypredictor.data.local.dao

import androidx.lifecycle.LiveData
import androidx.room.*
import com.farhan.electricitypredictor.data.local.entity.ApplianceEntity

@Dao
interface ApplianceDao {
    @Query("SELECT * FROM appliances ORDER BY (powerRatingWatts * dailyUsageHours) DESC")
    fun getAllAppliances(): LiveData<List<ApplianceEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAppliance(appliance: ApplianceEntity): Long

    @Update
    suspend fun updateAppliance(appliance: ApplianceEntity)

    @Delete
    suspend fun deleteAppliance(appliance: ApplianceEntity)

    @Query("SELECT SUM(powerRatingWatts * quantity) FROM appliances")
    suspend fun getTotalConnectedWatts(): Float?

    @Query("SELECT AVG(dailyUsageHours) FROM appliances")
    suspend fun getAverageDailyHours(): Float?
}

