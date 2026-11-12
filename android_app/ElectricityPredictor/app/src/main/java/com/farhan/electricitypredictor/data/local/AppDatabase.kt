package com.farhan.electricitypredictor.data.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import androidx.sqlite.db.SupportSQLiteDatabase
import com.farhan.electricitypredictor.data.local.dao.ApplianceDao
import com.farhan.electricitypredictor.data.local.dao.HistoricalBillDao
import com.farhan.electricitypredictor.data.local.entity.ApplianceEntity
import com.farhan.electricitypredictor.data.local.entity.HistoricalBillEntity
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

@Database(
    entities = [ApplianceEntity::class, HistoricalBillEntity::class],
    version = 1,
    exportSchema = false
)
abstract class AppDatabase : RoomDatabase() {

    abstract fun applianceDao(): ApplianceDao
    abstract fun historicalBillDao(): HistoricalBillDao

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun getDatabase(context: Context, scope: CoroutineScope): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "electricity_predictor_db"
                )
                    .addCallback(DatabaseCallback(scope))
                    .build()
                INSTANCE = instance
                instance
            }
        }

        private class DatabaseCallback(
            private val scope: CoroutineScope
        ) : RoomDatabase.Callback() {
            override fun onCreate(db: SupportSQLiteDatabase) {
                super.onCreate(db)
                INSTANCE?.let { database ->
                    scope.launch(Dispatchers.IO) {
                        populateInitialData(database.applianceDao(), database.historicalBillDao())
                    }
                }
            }

            suspend fun populateInitialData(applianceDao: ApplianceDao, billDao: HistoricalBillDao) {
                // Pre-populate standard realistic appliances
                val defaultAppliances = listOf(
                    ApplianceEntity(name = "1.5 Ton Inverter AC", powerRatingWatts = 1800f, dailyUsageHours = 8f, category = "Cooling", quantity = 1),
                    ApplianceEntity(name = "Refrigerator (Medium)", powerRatingWatts = 300f, dailyUsageHours = 24f, category = "Kitchen", quantity = 1),
                    ApplianceEntity(name = "Ceiling Fans", powerRatingWatts = 80f, dailyUsageHours = 12f, category = "General", quantity = 4),
                    ApplianceEntity(name = "LED Energy Saver Lights", powerRatingWatts = 18f, dailyUsageHours = 7f, category = "Lighting", quantity = 8),
                    ApplianceEntity(name = "Water Pump / Motor (1 HP)", powerRatingWatts = 750f, dailyUsageHours = 1.5f, category = "Heavy Load", quantity = 1),
                    ApplianceEntity(name = "Electric Iron", powerRatingWatts = 1000f, dailyUsageHours = 0.8f, category = "General", quantity = 1),
                    ApplianceEntity(name = "Smart LED TV (50-inch)", powerRatingWatts = 120f, dailyUsageHours = 5f, category = "Entertainment", quantity = 1),
                    ApplianceEntity(name = "Washing Machine", powerRatingWatts = 500f, dailyUsageHours = 1f, category = "General", quantity = 1)
                )

                for (item in defaultAppliances) {
                    applianceDao.insertAppliance(item)
                }

                // Pre-populate past 3 months bills
                val defaultBills = listOf(
                    HistoricalBillEntity(monthName = "October 2026", unitsConsumed = 380f, billAmountPkr = 19500f),
                    HistoricalBillEntity(monthName = "September 2026", unitsConsumed = 440f, billAmountPkr = 23200f),
                    HistoricalBillEntity(monthName = "August 2026", unitsConsumed = 510f, billAmountPkr = 28700f)
                )

                for (bill in defaultBills) {
                    billDao.insertBill(bill)
                }
            }
        }
    }
}

