package com.farhan.electricitypredictor.ml

import android.content.Context
import org.tensorflow.lite.Interpreter
import java.io.FileInputStream
import java.nio.ByteBuffer
import java.nio.ByteOrder
import java.nio.channels.FileChannel

class ElectricityPredictorClient(private val context: Context) {

    private var interpreter: Interpreter? = null

    init {
        try {
            val modelBuffer = loadModelFile("electricity_predictor.tflite")
            val options = Interpreter.Options()
            interpreter = Interpreter(modelBuffer, options)
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun loadModelFile(modelName: String): ByteBuffer {
        val fileDescriptor = context.assets.openFd(modelName)
        val inputStream = FileInputStream(fileDescriptor.fileDescriptor)
        val fileChannel = inputStream.channel
        val startOffset = fileDescriptor.startOffset
        val declaredLength = fileDescriptor.declaredLength
        return fileChannel.map(FileChannel.MapMode.READ_ONLY, startOffset, declaredLength)
    }

    /**
     * Runs TensorFlow Lite inference to predict next month's consumption in kWh.
     * Features: [watts, hours, past_month_units, past_3month_avg_units, season_factor, members]
     */
    fun predictConsumption(
        totalWatts: Float,
        dailyHours: Float,
        pastMonthUnits: Float,
        past3MonthAvgUnits: Float,
        seasonFactor: Float = 3.0f, // 1=Winter, 2=Moderate, 3=Summer
        householdMembers: Float = 5.0f
    ): Float {
        val input = Array(1) {
            floatArrayOf(
                totalWatts,
                dailyHours,
                pastMonthUnits,
                past3MonthAvgUnits,
                seasonFactor,
                householdMembers
            )
        }
        val output = Array(1) { FloatArray(1) }

        return try {
            interpreter?.let {
                it.run(input, output)
                val predicted = output[0][0]
                if (predicted > 0) predicted else fallbackEstimate(totalWatts, dailyHours, pastMonthUnits)
            } ?: fallbackEstimate(totalWatts, dailyHours, pastMonthUnits)
        } catch (e: Exception) {
            e.printStackTrace()
            fallbackEstimate(totalWatts, dailyHours, pastMonthUnits)
        }
    }

    private fun fallbackEstimate(watts: Float, hours: Float, pastUnits: Float): Float {
        val calculatedMonthly = (watts * hours * 0.40f * 30f) / 1000f
        return if (pastUnits > 0) {
            (calculatedMonthly * 0.5f) + (pastUnits * 0.5f)
        } else {
            calculatedMonthly
        }
    }

    fun close() {
        interpreter?.close()
        interpreter = null
    }
}

