package com.farhan.electricitypredictor

import android.app.Application
import com.farhan.electricitypredictor.data.local.AppDatabase
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.SupervisorJob

class ElectricityPredictorApp : Application() {

    val applicationScope = CoroutineScope(SupervisorJob())

    val database by lazy { AppDatabase.getDatabase(this, applicationScope) }
    val applianceDao by lazy { database.applianceDao() }
    val historicalBillDao by lazy { database.historicalBillDao() }
}

